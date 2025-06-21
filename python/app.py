from flask import Flask, jsonify
import requests
from requests.auth import HTTPBasicAuth
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from loguru import logger
from tqdm import tqdm
from bs4 import BeautifulSoup
import uuid
import os
import pandas as pd
from tabulate import tabulate
import pendulum
import traceback
from prettyprinter  import pprint,pformat
import hashlib
import inspect
import json
myself = lambda: inspect.stack()[1][3]
# --- Configuration ---
# It's recommended to use environment variables for sensitive data
# and host configuration for better security and flexibility.
USERNAME = os.environ.get("SAP_PO_USER", "SUP.FRACASSG")
PASSWORD = os.environ.get("SAP_PO_PASSWORD", "ini00ini")
HOST = os.environ.get("SAP_PO_HOST", "http://sappod.menarini.net:54000")

# --- Flask App Initialization ---
app = Flask(__name__)

# --- SOAP API Endpoints ---
SOAP_ENDPOINTS = {
    "IntegratedConfigurationsList": f"{HOST}/IntegratedConfigurationInService/IntegratedConfigurationInImplBean",
    "IntegratedConfiguration": f"{HOST}/IntegratedConfigurationInService/IntegratedConfigurationInImplBean",
    "CommunicationChannelList": f"{HOST}/CommunicationChannelInService/CommunicationChannelInImplBean",
    "CommunicationChannel": f"{HOST}/CommunicationChannelInService/CommunicationChannelInImplBean",
    "SenderAgreementList": f"{HOST}/SenderAgreementInService/SenderAgreementInImplBean",
    "SenderAgreement": f"{HOST}/SenderAgreementInService/SenderAgreementInImplBean",
    "ReceiverAgreementList": f"{HOST}/ReceiverAgreementInService/ReceiverAgreementInImplBean",
    "ReceiverAgreement": f"{HOST}/ReceiverAgreementInService/ReceiverAgreementInImplBean",
    "ValueMappingList": f"{HOST}/ValueMappingInService/ValueMappingInImplBean",
    "ValueMapping": f"{HOST}/ValueMappingInService/ValueMappingInImplBean"
}
 

# --- Database Setup ---
DB_FILE = "sap_po_data.db"
engine = create_engine(f"sqlite:///{DB_FILE}")
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- SQLAlchemy Models ---
# These models define the database schema for storing the extracted SAP PO data.

class IntegratedConfiguration(Base):
    __tablename__ = 'IntegratedConfigurations'
    SenderComponentID = Column(String, primary_key=True)
    InterfaceName = Column(String, primary_key=True)
    InterfaceNamespace = Column(String, primary_key=True)
    # Using a generic Text column to store the full XML for future analysi
    FullObjectXML = Column(Text)

class IntegratedConfigurationsList(Base):
    __tablename__ = 'IntegratedConfigurationsList'
    SenderPartyID = Column(String, primary_key=True)
    SenderComponentID = Column(String, primary_key=True)
    InterfaceName = Column(String, primary_key=True)
    InterfaceNamespace = Column(String, primary_key=True)
    ReceiverPartyID = Column(String, primary_key=True)
    ReceiverComponentID = Column(String, primary_key=True)

class CommunicationChannel(Base):
    __tablename__ = 'CommunicationChannels'
    UUID = Column(String, primary_key=True)
    FullObjectXML = Column(Text)
    FullObjectJSON = Column(Text)
    FullObject = Column(Text)  # This can be used to store the full object in a different format if needed


class CommunicationChannelList(Base):
    __tablename__ = 'CommunicationChannelList'
    ComponentID = Column(String, primary_key=True)
    ChannelID = Column(String, primary_key=True)
    PartyID = Column(String, primary_key=True)

class SenderAgreementList(Base):
    __tablename__ = 'SenderAgreementsList'
    SenderPartyID = Column(String, primary_key=True)
    SenderComponentID = Column(String, primary_key=True)
    InterfaceName = Column(String, primary_key=True)
    InterfaceNamespace = Column(String, primary_key=True)
    ReceiverPartyID = Column(String, primary_key=True)
    ReceiverComponentID = Column(String, primary_key=True)

class ReceiverAgreementList(Base):
    __tablename__ = 'ReceiverAgreementList'
    SenderPartyID = Column(String, primary_key=True)
    SenderComponentID = Column(String, primary_key=True)
    InterfaceName = Column(String, primary_key=True)
    InterfaceNamespace = Column(String, primary_key=True)
    ReceiverPartyID = Column(String, primary_key=True)
    ReceiverComponentID = Column(String, primary_key=True)

class ReceiverAgreement(Base):
    __tablename__ = 'ReceiverAgreements'
    SenderComponentID = Column(String, primary_key=True)
    ReceiverComponentID = Column(String, primary_key=True)
    InterfaceName = Column(String, primary_key=True)
    InterfaceNamespace = Column(String, primary_key=True)
    ChannelID = Column(String)

class ValueMapping(Base):
    __tablename__ = 'ValueMappings'
    GroupID = Column(String, primary_key=True)
    Description = Column(String)

class ValueMappingList(Base):
    __tablename__ = 'ValueMappingList'
    #id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ValueMappingID = Column(String, primary_key=True)


# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# --- SOAP Request Handling ---
HEADERS = {
    "Content-Type": "text/xml;charset=UTF-8",
    "SOAPAction": "http://sap.com/xi/WebService/soap1.1"
}


# Convert XML to JSON using BeautifulSoup and a helper function
def xml_to_dict(element):
    # Recursively convert BeautifulSoup XML element to dict
    if not element.contents or all(isinstance(child, str) and not child.strip() for child in element.contents):
        return element.get_text(strip=True)
    result = {}
    for child in element.find_all(recursive=False):
        key = child.name
        value = xml_to_dict(child)
        if key in result:
            # If key already exists, convert to list
            if not isinstance(result[key], list):
                result[key] = [result[key]]
                result[key].append(value)
        else:
            result[key] = value
    return result

def get_payload(endpoint_key, query_tag, item=None):
    """Generates a SOAP payload for querying Integrated Configurations."""
    if 'list' in endpoint_key.lower():
        # For list endpoints, we use a different query tag
        payload = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://sap.com/xi/BASIS">
            <soapenv:Header/>
            <soapenv:Body>
                <web:{query_tag}/>
            </soapenv:Body>
            </soapenv:Envelope>
            """
        return payload
    elif 'CommunicationChannel' == endpoint_key:
        # For list endpoints, we use a different query tag
        payload = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:p1="http://sap.com/xi/BASIS">
            <soapenv:Header/>
            <soapenv:Body>
                <p1:{query_tag}  > 
                    <ReadContext>User</ReadContext>
                    <CommunicationChannelID>"""
        
        logger.info(f"Building payload for {endpoint_key} with query tag {query_tag} and item {pformat(item)}")
        for column in item.__table__.columns:
            k = column.name
            v = getattr(item, k)
            logger.info(f"Processing key: {k}, value: {v}")
            if v is not None:
                payload += f" <{k}>{v}</{k}>" 
        
        payload += f"""
                    </CommunicationChannelID>
                </p1:{query_tag}>
            </soapenv:Body>
            </soapenv:Envelope>
            """
        return payload.strip()

def send_soap_request(url, payload):
    """Sends a SOAP request and returns the response text."""
    try:
        response = requests.post(
            url,
            data=payload.encode('utf-8'),
            headers=HEADERS,
            auth=HTTPBasicAuth(USERNAME, PASSWORD)
        )
        response.raise_for_status() # Raises an HTTPError for bad responses (4XX or 5XX)

        # Save response for debugging
        debug_dir = "debug_responses"
        os.makedirs(debug_dir, exist_ok=True)
        now = pendulum.now()
        now = now.format('YYYYMMDDHHmmss')
        filename = f"soap_response_{now}_{uuid.uuid4().hex}.xml"
        filepath = os.path.join(debug_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        logger.info(f"SOAP response saved to {filepath}")

        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during SOAP request to {url}: {e}")
        raise

# --- Generic Extraction Logic ---
def extract_and_store(endpoint_key, query_tag, result_tag, model_cls, row_builder, item=None):
    """
    Generic function to fetch data from a SOAP endpoint, parse it, and store it in the database.
    """
    model_cls.metadata.create_all(bind=engine, checkfirst=True)
   
    db = SessionLocal()
    logger.info(f"🚀 Starting extraction for {endpoint_key}...")
    try:
        # The QueryRequest payload is common across many Directory APIs
        payload = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://sap.com/xi/BASIS">
           <soapenv:Header/>
           <soapenv:Body>
              <web:{query_tag}/>
           </soapenv:Body>
        </soapenv:Envelope>
        """
        payload = get_payload(endpoint_key, query_tag,item)
        xml_response = send_soap_request(SOAP_ENDPOINTS[endpoint_key], payload)
        soup = BeautifulSoup(xml_response, "lxml-xml")
        results = soup.find_all(result_tag)
        logger.info(f"Found {len(results)} items for {endpoint_key} with tag '{result_tag}'.")
        if not results:
            logger.warning(f"⚠️ No results found for {endpoint_key} with tag '{result_tag}'.")
            return {"status": "success", "message": "No items to process.", "rows_processed": 0}

        # Clear the table before inserting new data to avoid duplicates
        #db.query(model_cls).delete()
        #logger.info(f"🧹 Cleared table {model_cls.__tablename__} before insertion.")

        for item in tqdm(results, desc=f"Parsing and storing {endpoint_key}"):
            row = row_builder(item)
            if row:
                db.merge(row)

        db.commit()
        
        # Log a sample of the data
        df = pd.read_sql_table(model_cls.__tablename__, engine)
        logger.info(f"✅ Successfully stored {len(df)} rows in '{model_cls.__tablename__}'. Sample data:\n" +
            tabulate(df.head(5), headers="keys", tablefmt="pretty"))

        return {"status": "success", "rows_processed": len(results)}

    except Exception as e:
        db.rollback()
        logger.error(f"❌ An error occurred during extraction for {endpoint_key}: {e}")

        logger.exception(f"💥 Stacktrace for extraction error in {endpoint_key}: {traceback.format_exc()}")

        return {"status": "error", "message": str(e)}
    finally:
        db.close()
        logger.info(f"🏁 Finished extraction for {endpoint_key}.")

# --- Flask Routes ---

@app.route("/extract/all", methods=["GET"])
def extract_all():
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

@app.route("/extract/integrated_configurations", methods=["GET"])
def extract_integrated_configurations():
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
    return jsonify(extract_and_store(
        "IntegratedConfigurationsList",
        "IntegratedConfigurationQueryRequest",
        "IntegratedConfigurationID",
        IntegratedConfigurationsList,
        build_row
    )) 


import asyncio
import threading
from datetime import datetime, timedelta

# Stato globale per la progressione e il caching
extract_status = {
    "running": False,
    "completed_at": None,
    "processed": 0,
    "total": 0,
    "result": None
}
extract_lock = threading.Lock()

@app.route("/extract/communication_channels", methods=["GET"])
def extract_communication_channels():
    """Asynchronous extraction of Communication Channel objects with progress tracking."""

    def build_row(item):
        xml_str = str(item)
        UUID_Str = hashlib.sha256(xml_str.encode('utf-8')).hexdigest()
        xml_json = xml_to_dict(item)
        json_str = json.dumps(xml_json, ensure_ascii=False, indent=2)
        return CommunicationChannel(
            UUID=UUID_Str,
            FullObjectXML=xml_str.strip() if xml_str else "",
            FullObjectJSON=pformat(json_str) if json_str else "",
            FullObject=json_str.strip() if json_str else "",
        )

    with extract_lock:
        now = datetime.utcnow()
        # Se completato da meno di 1 ora, ritorna solo lo stato completato
        if extract_status["completed_at"] and (now - extract_status["completed_at"]) < timedelta(hours=1):
            return jsonify({
                "status": "completed",
                "processed": extract_status["processed"],
                "total": extract_status["total"]
            })
        # Se già in esecuzione, ritorna lo stato di avanzamento
        if extract_status["running"]:
            percent = (extract_status["processed"] / extract_status["total"] * 100) if extract_status["total"] else 0
            return jsonify({
                "status": "running",
                "percent_complete": round(percent, 2),
                "processed": extract_status["processed"],
                "total": extract_status["total"]
            })
        # Altrimenti, avvia l'estrazione
        extract_status["running"] = True
        extract_status["processed"] = 0
        extract_status["total"] = 0
        extract_status["result"] = None
        extract_status["completed_at"] = None

    def extraction_task():
        db = SessionLocal()
        try:
            items = db.query(CommunicationChannelList).all()
            total = len(items)
            with extract_lock:
                extract_status["total"] = total
            logger.info(f"📦 Found {total} CommunicationChannelList items in the database.")
            results = []
            for idx, item in enumerate(items, 1):
                single_result = extract_and_store(
                    "CommunicationChannel",
                    "CommunicationChannelReadRequest",
                    "CommunicationChannel",
                    CommunicationChannel,
                    build_row,
                    item
                )
                with extract_lock:
                    extract_status["processed"] = idx
                results.append(single_result)
            with extract_lock:
                extract_status["result"] = results
                extract_status["completed_at"] = datetime.utcnow()
                extract_status["running"] = False
        except Exception as e:
            with extract_lock:
                extract_status["running"] = False
            logger.error(f"❌ Error in async extraction: {e}")
        finally:
            db.close()

    # Avvia il task in un thread separato
    threading.Thread(target=extraction_task, daemon=True).start()

    return jsonify({
        "status": "started",
        "processed": 0,
        "total": extract_status["total"]
    })



@app.route("/extract/communication_channels_list", methods=["GET"])
def extract_communication_channels_list():
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
    return jsonify(extract_and_store(
        "CommunicationChannelList",
        "CommunicationChannelQueryRequest",
        "CommunicationChannelID",
        CommunicationChannelList,
        build_row
    ))
 

@app.route("/extract/sender_agreements", methods=["GET"])
def extract_sender_agreements():
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
    return jsonify(extract_and_store(
        "SenderAgreementList",
        "SenderAgreementQueryRequest",
        "SenderAgreementID",
        SenderAgreementList,
        build_row
    ))

@app.route("/extract/receiver_agreements", methods=["GET"])
def extract_receiver_agreements():
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
    return jsonify(extract_and_store(
        "ReceiverAgreementList",
        "ReceiverAgreementQueryRequest",
        "ReceiverAgreementID",
        ReceiverAgreementList,
        build_row
    ))

@app.route("/extract/value_mappings", methods=["GET"])
def extract_value_mappings():
    """Extracts Value Mapping objects."""
    def build_row(item):
        # Note: The PDF indicates ValueMappingID and GroupName are part of the response.
        return ValueMapping(
            GroupID=item.find("ValueMappingID").get_text(strip=True) if item.find("ValueMappingID") else "",
            Description=item.find("GroupName").get_text(strip=True) if item.find("GroupName") else ""
        )
    return jsonify(extract_and_store(
        "ValueMapping",
        "ValueMappingQueryRequest",
        "ValueMapping",
        ValueMapping,
        build_row
    ))

@app.route("/extract/value_mappings_list", methods=["GET"])
def extract_value_mappings_list():
    """Extracts Value Mapping objects."""
    def build_row(item):
        #ilog = item.get_text(strip=True) if item else ""
        #logger.info(f"{build_row.__name__} called with item: {item} - {pformat(ilog)}")
        # Note: The PDF indicates ValueMappingID and GroupName are part of the response.
        return ValueMappingList(
            ValueMappingID=item.get_text(strip=True) if item else "",
        )
    return jsonify(extract_and_store(
        "ValueMappingList",
        "ValueMappingQueryRequest",
        "ValueMappingID",
        ValueMappingList,
        build_row
    ))

# --- Server Start ---
if __name__ == "__main__":
    # Setup basic logger
    logger.add("file_{time}.log")
    
    # Check for credentials
    if USERNAME == "YOUR_USERNAME" or PASSWORD == "YOUR_PASSWORD":
        logger.warning("Using default credentials. Please set SAP_PO_USER and SAP_PO_PASSWORD environment variables.")
        
    logger.info(f"Starting Flask server on port 5001. Connecting to SAP PO at {HOST}")
    app.run(debug=True, port=5001)

