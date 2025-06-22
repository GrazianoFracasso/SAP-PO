#from flask import Flask, jsonify
from fastapi import FastAPI
from loguru import logger
import pendulum
from prettyprinter  import pprint,pformat
import asyncio
from utilities import myself
from config import *
from models import *
from status_store import get_status, set_status,StatusModel
from pydantic import BaseModel
from typing import Optional
import uvicorn
from utilities import (
    xml_to_dict,

)
from models import (
    IntegratedConfiguration,
    IntegratedConfigurationsList,
    CommunicationChannel,
    CommunicationChannelList,
    SenderAgreementList,
    ReceiverAgreementList,
    ValueMapping,
    ValueMappingList,
)
from store_data import engine, SessionLocal
from models.generic_sappo_logics import extract_and_store
from models.communication_channels import get_total_communication_channels

# --- Flask App Initialization ---
app = FastAPI()
status_locks = {}
# --- SOAP API Endpoints ---

  
    # --- FastAPI Routes ---

@app.get("/")
async def root():
    return {"message": "OK"}

@app.get("/extract/all")
async def extract_all():
    """Endpoint to trigger extraction for all defined object types."""
    logger.info("Starting extraction for all object types...")
    results = {}
    results["integrated_configurations"] = extract_integrated_configurations().get_json()
    results["communication_channels"] = extract_communication_channels().get_json()
    results["sender_agreements"] = extract_sender_agreements().get_json()
    results["receiver_agreements"] = extract_receiver_agreements().get_json()
    results["value_mappings"] = extract_value_mappings().get_json()
    logger.info("Finished extracting all object types.")
    return jsonify({"status": "completed", "results": results})


@app.get("/extract/integrated_configurations")
async def extract_integrated_configurations():
    """Extracts Integrated Configuration objects."""
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
        build_row
    )



# Stato globale per la progressione e il caching
extract_status = {
    "running": False,
    "completed_at": None,
    "processed": 0,
    "total": 0,
    "result": None
}
 


@app.get("/extract/communication_channels/{type}")
async def extract_communication_channels(type:str):
    """Asynchronous extraction of Communication Channel objects with progress tracking."""
    procedure_name = myself()
    logger.info(f"🔍 Richiesta di estrazione ricevuta per procedura: {procedure_name}/{type}" )
    from models.communication_channels import extraction_task

    lock = status_locks.setdefault(procedure_name, asyncio.Lock())
    
    async with lock:
        status = await get_status(procedure_name)
        now = pendulum.now()

        if type == 'status' or type == 'complete':
            percent = (status.processed / status.total  * 100) if status.total  else 0
            logger.info("⏳ Estrazione in corso: {}/{} ({:.2f}%)", status.processed, status.total, percent)
            return {
                "status": "running",
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
                    "processed": status.processed,
                    "total": status.total 
                }
            # Se già in esecuzione, ritorna lo stato di avanzamento
            if status.running:
                percent = (status.processed / status.total  * 100) if status.total  else 0
                logger.info("⏳ Estrazione in corso: {}/{} ({:.2f}%)", status.processed, status.total, percent)
                return {
                    "status": "running",
                    "percent_complete": round(percent, 2),
                    "processed": status.processed,
                    "total": status.total 
                }
        # Altrimenti, avvia l'estrazione
        logger.info("🚀 Avvio nuova estrazione asincrona per '{}'", procedure_name)
        new_status = {
            "running": True,
            "processed": 0,
            "total": 0,
            "result": None,
            "completed_at": None
        }
        nmw = StatusModel(**new_status)
        await set_status(procedure_name, nmw)
        
    

    asyncio.create_task(extraction_task(procedure_name, lock))
    # Avvia il task in un thread separato
    #threading.Thread(target=extraction_task, daemon=True).start()

    return {
        "status": "started",
        "processed": 0,
        "total": get_total_communication_channels()
    }


@app.get("/extract/communication_channels_list")
async def extract_communication_channels_list():
    """Extracts Communication Channel objects."""
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
        build_row
    )
 


@app.get("/extract/sender_agreements")
async def extract_sender_agreements():
    """Extracts Sender Agreement objects."""
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
        build_row
    ) 

@app.get("/extract/value_mappings")
async def extract_receiver_agreements():
    """Extracts Receiver Agreement objects."""
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
        build_row
    ) 

@app.get("/extract/value_mappings")
async def extract_value_mappings():
    """Extracts Value Mapping objects."""
    def build_row(item):
        # Note: The PDF indicates ValueMappingID and GroupName are part of the response.
        return ValueMapping(
            GroupID=item.find("ValueMappingID").get_text(strip=True) if item.find("ValueMappingID") else "",
            Description=item.find("GroupName").get_text(strip=True) if item.find("GroupName") else ""
        )
    return extract_and_store(
        "ValueMapping",
        "ValueMappingQueryRequest",
        "ValueMapping",
        ValueMapping,
        build_row
    )

@app.get("/extract/value_mappings_list")
async def extract_value_mappings_list():
    """Extracts Value Mapping objects."""
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
        build_row
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

