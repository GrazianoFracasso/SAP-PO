#from flask import Flask, jsonify
from fastapi import FastAPI, HTTPException
from loguru import logger
import pendulum
from prettyprinter  import pprint,pformat
import asyncio
from utilities import myself
from config import *
from models import *
from status_store import get_status, set_status,StatusModel
import uvicorn
from models import (
    IntegratedConfigurationsList,
    CommunicationChannelList,
    SenderAgreementList,
    ReceiverAgreementList,
    ValueMappingList,
)
from models.generic_sappo_logics import extract_and_store

# --- Flask App Initialization ---
app = FastAPI()
status_locks = {}
tags_metadata = []


def resolve_environment(environment: str) -> str:
    try:
        return get_environment_config(environment).name
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

# --- SOAP API Endpoints ---

  
# --- FastAPI Routes ---

@app.get("/")
async def root():
    return {"message": "OK"}

@app.get("/extract/{environment}/all")
@app.get("/extract/all")
async def extract_all(environment: str = DEFAULT_ENVIRONMENT):
    """Endpoint to trigger extraction for all defined object types."""
    environment = resolve_environment(environment)
    logger.info(f"Starting extraction for all object types on environment '{environment}'...")

    result_keys = [
        "integrated_configurations_list",
        "communication_channels_list",
        "sender_agreements_list",
        "receiver_agreements_list",
        "value_mappings_list",
    ]
    result_values = await asyncio.gather(
        extract_integrated_configurations_list(environment),
        extract_communication_channels_list(environment),
        extract_sender_agreements_list(environment),
        extract_receiver_agreements_list(environment),
        extract_value_mappings_list(environment),
    )

    results = dict(zip(result_keys, result_values))
    logger.info(f"Finished extracting all object types on environment '{environment}'.")
    return {"status": "completed", "environment": environment, "results": results}

 
@app.get("/extract/{environment}/integrated_configurations_list")
@app.get("/extract/integrated_configurations_list")
async def extract_integrated_configurations_list(environment: str = DEFAULT_ENVIRONMENT):
    """Extracts Integrated Configuration objects."""
    environment = resolve_environment(environment)
    def build_row(item):
        return IntegratedConfigurationsList(
            SenderPartyID=item.find("SenderPartyID").get_text(strip=True) if item.find("SenderPartyID") else "",
            SenderComponentID=item.find("SenderComponentID").get_text(strip=True) if item.find("SenderComponentID") else "",
            InterfaceName=item.find("InterfaceName").get_text(strip=True) if item.find("InterfaceName") else "",
            InterfaceNamespace=item.find("InterfaceNamespace").get_text(strip=True) if item.find("InterfaceNamespace") else "",
            ReceiverPartyID=item.find("ReceiverPartyID").get_text(strip=True) if item.find("ReceiverPartyID") else "",
            ReceiverComponentID=item.find("ReceiverComponentID").get_text(strip=True) if item.find("ReceiverComponentID") else ""
        )
    return extract_and_store(
        "IntegratedConfigurationsList",
        "IntegratedConfigurationQueryRequest",
        "IntegratedConfigurationID",
        IntegratedConfigurationsList,
        build_row,
        environment=environment
    )

tags_metadata.append({
    "name": "/extract/full/",
    "description": """
    http://127.0.0.1:5001/extract/full/communication_channels/status
    http://127.0.0.1:5001/extract/full/pod/communication_channels/status
    http://127.0.0.1:5001/extract/full/communication_channels/complete
    ttp://127.0.0.1:5001/extract/full/communication_channels/refreshh
    http://127.0.0.1:5001/extract/full/integration_configurations/refresh
    http://127.0.0.1:5001/extract/full/value_mappings/refresh
    http://127.0.0.1:5001/extract/full/sender_agreements/refresh
    http://127.0.0.1:5001/extract/full/receiver_agreements/refresh
""",
})
@app.get("/extract/full/{environment}/{entity}/{action_type}")
@app.get("/extract/full/{entity}/{action_type}")
async def extract_full_entities(entity:str,action_type:str, environment: str = DEFAULT_ENVIRONMENT):
    """Asynchronous extraction of Integrated Configuration objects with progress tracking."""
    environment = resolve_environment(environment)
    procedure_name = f"{myself()}_{environment}_{entity}"
    logger.info(f"🔍 Richiesta di estrazione ricevuta per procedura: {procedure_name}/{action_type}" )
    import models
 
    def dyn_import_module(submodule_name):
        from importlib import import_module
        import models
        import sys
        """Ottiene una classe usando getattr"""
        try:
            r = import_module(f"models.{submodule_name}")
            if r is None:
                raise ValueError(f"❗️Modulo '{submodule_name}' non trovata")  
            return r
        except AttributeError:
            raise ValueError(f"❗️Modulo '{submodule_name}' non trovata")  

    # METODO 1: Usando getattr()
    def get_class_with_getattr(class_name):
        import models
        """Ottiene una classe usando getattr"""
        try:
            return getattr(models, class_name)
        except AttributeError:
            raise ValueError(f"❗️Classe '{class_name}' non trovata")
    
    entity_mdl = dyn_import_module(entity)

    lock = status_locks.setdefault(procedure_name, asyncio.Lock())
    
    async with lock:
        status = await get_status(procedure_name)
        now = pendulum.now()

        if action_type == 'status' or action_type == 'complete':
            if not status:
                return {
                    "status": "not_found",
                    "environment": environment,
                    "processed": 0,
                    "total": 0
                }
            percent = (status.processed / status.total  * 100) if status.total  else 0
            logger.info("⏳ Estrazione in corso: {}/{} ({:.2f}%)", status.processed, status.total, percent)
            return {
                "status": "running",
                "environment": environment,
                "percent_complete": round(percent, 2),
                "processed": status.processed,
                "total": status.total 
            }
        
        # Se completato da meno di 1 ora, ritorna solo lo stato completato
        if status:
            if status.completed_at and (now - pendulum.parse(status.completed_at)) < pendulum.duration(days=1):
                logger.info("🕒 Estrazione già completata di recente (meno di 1 giorno fa).")
                return {
                    "status": "completed",
                    "environment": environment,
                    "processed": status.processed,
                    "total": status.total 
                }
            # Se già in esecuzione, ritorna lo stato di avanzamento
            if status.running:
                percent = (status.processed / status.total  * 100) if status.total  else 0
                logger.info("⏳ Estrazione in corso: {}/{} ({:.2f}%)", status.processed, status.total, percent)
                return {
                    "status": "running",
                    "environment": environment,
                    "percent_complete": round(percent, 2),
                    "processed": status.processed,
                    "total": status.total 
                }
        # Altrimenti, avvia l'estrazione
        logger.info("🚀 Avvio nuova estrazione asincrona per '{}'", procedure_name)
        new_status = {
            "running": True,
            "environment": environment,
            "processed": 0,
            "total": 0,
            "result": None,
            "completed_at": None
        }
        nmw = StatusModel(**new_status)
        await set_status(procedure_name, nmw)
        
    

    asyncio.create_task(entity_mdl.extraction_task(procedure_name, lock, environment))
    # Avvia il task in un thread separato
    #threading.Thread(target=extraction_task, daemon=True).start()

    return {
        "status": "started",
        "environment": environment,
        "processed": 0,
        "total": entity_mdl.get_total()
    }

@app.get("/extract/{environment}/communication_channels_list")
@app.get("/extract/communication_channels_list")
async def extract_communication_channels_list(environment: str = DEFAULT_ENVIRONMENT):
    """Extracts Communication Channel objects."""
    environment = resolve_environment(environment)
    def build_row(item):
        # For CommunicationChannel, we need to read the full object to get all details
        # This is a simplified version; a full implementation might read each channel individually.
        return CommunicationChannelList(
            PartyID=item.find("PartyID").get_text(strip=True) if item.find("PartyID") else "",
            ComponentID=item.find("ComponentID").get_text(strip=True) if item.find("ComponentID") else "",
            ChannelID=item.find("ChannelID").get_text(strip=True) if item.find("ChannelID") else "",
            # These fields might not be in the Query response, but in the Read response.
            # This is a placeholder to show the structure.
        )
    return extract_and_store(
        "CommunicationChannelList",
        "CommunicationChannelQueryRequest",
        "CommunicationChannelID",
        CommunicationChannelList,
        build_row,
        environment=environment
    )
 
@app.get("/extract/{environment}/sender_agreements")
@app.get("/extract/sender_agreements")
async def extract_sender_agreements_list(environment: str = DEFAULT_ENVIRONMENT):
    """Extracts Sender Agreement objects."""
    environment = resolve_environment(environment)
    def build_row(item):
        return SenderAgreementList(
            SenderPartyID=item.find("SenderPartyID").get_text(strip=True) if item.find("SenderPartyID") else "",
            SenderComponentID=item.find("SenderComponentID").get_text(strip=True) if item.find("SenderComponentID") else "",
            InterfaceName=item.find("InterfaceName").get_text(strip=True) if item.find("InterfaceName") else "",
            InterfaceNamespace=item.find("InterfaceNamespace").get_text(strip=True) if item.find("InterfaceNamespace") else "",
            ReceiverPartyID=item.find("ReceiverPartyID").get_text(strip=True) if item.find("ReceiverPartyID") else "",
            ReceiverComponentID=item.find("ReceiverComponentID").get_text(strip=True) if item.find("ReceiverComponentID") else ""
        )
    # CORRECTED: The result tag for a QueryResponse is 'SenderAgreementID', not 'SenderAgreement'.
    return  extract_and_store(
        "SenderAgreementList",
        "SenderAgreementQueryRequest",
        "SenderAgreementID",
        SenderAgreementList,
        build_row,
        environment=environment
    ) 

@app.get("/extract/{environment}/receiver_agreements")
@app.get("/extract/receiver_agreements")
async def extract_receiver_agreements_list(environment: str = DEFAULT_ENVIRONMENT):
    """Extracts Receiver Agreement objects."""
    environment = resolve_environment(environment)
    def build_row(item):
        return ReceiverAgreementList(
            SenderPartyID=item.find("SenderPartyID").get_text(strip=True) if item.find("SenderPartyID") else "",
            SenderComponentID=item.find("SenderComponentID").get_text(strip=True) if item.find("SenderComponentID") else "",
            InterfaceName=item.find("InterfaceName").get_text(strip=True) if item.find("InterfaceName") else "",
            InterfaceNamespace=item.find("InterfaceNamespace").get_text(strip=True) if item.find("InterfaceNamespace") else "",
            ReceiverPartyID=item.find("ReceiverPartyID").get_text(strip=True) if item.find("ReceiverPartyID") else "",
            ReceiverComponentID=item.find("ReceiverComponentID").get_text(strip=True) if item.find("ReceiverComponentID") else ""
        )
    return extract_and_store(
        "ReceiverAgreementList",
        "ReceiverAgreementQueryRequest",
        "ReceiverAgreementID",
        ReceiverAgreementList,
        build_row,
        environment=environment
    ) 

@app.get("/extract/{environment}/value_mappings_list")
@app.get("/extract/value_mappings_list")
async def extract_value_mappings_list(environment: str = DEFAULT_ENVIRONMENT):
    """Extracts Value Mapping objects."""
    environment = resolve_environment(environment)
    def build_row(item):
        #ilog = item.get_text(strip=True) if item else ""
        #logger.info(f"{build_row.__name__} called with item: {item} - {pformat(ilog)}")
        # Note: The PDF indicates ValueMappingID and GroupName are part of the response.
        return ValueMappingList(
            ValueMappingID=item.get_text(strip=True) if item else "",
        )
    
    ret = extract_and_store(
        "ValueMappingList",
        "ValueMappingQueryRequest",
        "ValueMappingID",
        ValueMappingList,
        build_row,
        environment=environment
    )
    logger.info(f"✅ Successfully runned {myself()} with result: {pformat(ret)}")
    return ret

# --- Server Start ---
if __name__ == "__main__":
    # Setup basic logger
    logger.add("file_{time}.log")
    
    # Check for credentials
    if USERNAME == "YOUR_USERNAME" or PASSWORD == "YOUR_PASSWORD":
        logger.warning("Using default credentials. Please set SAP_PO_USER and SAP_PO_PASSWORD environment variables.")
        
    logger.info(f"Starting FastAPI server on port 5001. Connecting to SAP PO at {HOST}")

    uvicorn.run("main:app",port=5001,reload=True)
    #app.run(debug=True, port=5001)

