from flask import Flask, jsonify
import requests
from requests.auth import HTTPBasicAuth
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from loguru import logger
from tqdm import tqdm
from prettyprinter import cpprint, pformat
from tabulate import tabulate
import pandas as pd
from bs4 import BeautifulSoup
import uuid
import os

# Configurazione Flask
app = Flask(__name__)

# Configurazione SOAP e database
USERNAME = "SUP.FRACASSG"
PASSWORD = "ini00ini"
HOST = "http://sappod.menarini.net:54000"

SOAP_ENDPOINTS = {
    "IntegratedConfiguration": f"{HOST}/IntegratedConfigurationInService/IntegratedConfigurationInImplBean",
    "CommunicationChannel": f"{HOST}/CommunicationChannelInService/CommunicationChannelInImplBean",
    "SenderAgreementList": f"{HOST}/SenderAgreementInService/SenderAgreementInImplBean",
    "ReceiverAgreement": f"{HOST}/ReceiverAgreementInService/ReceiverAgreementInImplBean",
    "ValueMapping": f"{HOST}/ValueMappingInService/ValueMappingInImplBean"
}

# Database setup
engine = create_engine("sqlite:///sap_po_data.db")
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Modelli SQLAlchemy
class IntegratedConfiguration(Base):
    __tablename__ = 'IntegratedConfigurations'
    SenderComponentID = Column(String, primary_key=True)
    InterfaceName = Column(String, primary_key=True)
    InterfaceNamespace = Column(String, primary_key=True)
    ReceiverComponentID = Column(String, primary_key=True)

class CommunicationChannel(Base):
    __tablename__ = 'CommunicationChannels'
    ComponentID = Column(String, primary_key=True)
    ChannelID = Column(String, primary_key=True)
    AdapterName = Column(String)
    Direction = Column(String)
    TransportProtocol = Column(String)
    MessageProtocol = Column(String)

class SenderAgreementList(Base):
    __tablename__ = 'SenderAgreementsList'
    SenderPartyID = Column(String, primary_key=True)
    SenderComponentID = Column(String, primary_key=True)
    InterfaceName = Column(String, primary_key=True)
    InterfaceNamespace = Column(String, primary_key=True)
    ReceiverPartyID = Column(String, primary_key=True)
    ReceiverComponentID = Column(String, primary_key=True)

class SenderAgreement(Base):
    __tablename__ = 'SenderAgreements'
    SenderComponentID = Column(String, primary_key=True)
    InterfaceName = Column(String, primary_key=True)
    InterfaceNamespace = Column(String, primary_key=True)
    ChannelID = Column(String)

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

Base.metadata.create_all(engine)

HEADERS = {
    "Content-Type": "text/xml;charset=UTF-8",
    "SOAPAction": "http://sap.com/xi/WebService/soap1.1"
}

def send_soap_request(url, payload):
    response = requests.post(
        url,
        data=payload,
        headers=HEADERS,
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )
    response.raise_for_status()

    filename = f"soap_response_{uuid.uuid4().hex}.xml"
    filepath = os.path.join("debug_responses", filename)
    os.makedirs("debug_responses", exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(response.text)
    logger.info(f"SOAP response written to {filepath}")

    return response.text

# Estrattori comuni

def extract_and_store(endpoint_key, tag_name, model_cls, row_builder):
    db = SessionLocal()
    logger.info(f"Fetching {endpoint_key}...")
    try:
        payload = f"""
        <soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:web=\"http://sap.com/xi/BASIS\">
            <soapenv:Header/>
            <soapenv:Body>
                <web:{tag_name}QueryRequest/>
            </soapenv:Body>
        </soapenv:Envelope>
        """
        xml_response = send_soap_request(SOAP_ENDPOINTS[endpoint_key], payload)
        soup = BeautifulSoup(xml_response, "lxml-xml")
        results = soup.find_all(tag_name)

        for item in tqdm(results, desc=f"Parsing {endpoint_key}"):
            row = row_builder(item)
            db.merge(row)

        db.commit()
        df = pd.read_sql_table(model_cls.__tablename__, engine)
        logger.info("\n" + tabulate(df.head(10), headers="keys", tablefmt="pretty"))
        return {"status": "success", "rows": len(results)}
    except Exception as e:
        logger.error(e)
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

@app.route("/extract/sender_agreements", methods=["GET"])
def extract_sender_agreements():
    def build_row(item):
        return SenderAgreementList(
            SenderPartyID=item.SenderPartyID.get_text() if item.SenderPartyID else "",
            SenderComponentID=item.SenderComponentID.get_text() if item.SenderComponentID else "",
            InterfaceName=item.InterfaceName.get_text() if item.InterfaceName else "",
            InterfaceNamespace=item.InterfaceNamespace.get_text() if item.InterfaceNamespace else "",
            ReceiverPartyID=item.ReceiverPartyID.get_text() if item.ReceiverPartyID else "",
            ReceiverComponentID=item.ReceiverComponentID.get_text() if item.ReceiverComponentID else ""
        )
    return jsonify(extract_and_store("SenderAgreementList", "SenderAgreementID", SenderAgreementList, build_row))

@app.route("/extract/receiver_agreements", methods=["GET"])
def extract_receiver_agreements():
    def build_row(item):
        return ReceiverAgreement(
            SenderComponentID=item.find("SenderComponentID").get_text() if item.find("SenderComponentID") else "",
            ReceiverComponentID=item.find("ReceiverComponentID").get_text() if item.find("ReceiverComponentID") else "",
            InterfaceName=item.find("InterfaceName").get_text() if item.find("InterfaceName") else "",
            InterfaceNamespace=item.find("InterfaceNamespace").get_text() if item.find("InterfaceNamespace") else "",
            ChannelID=item.find("ChannelID").get_text() if item.find("ChannelID") else ""
        )
    return jsonify(extract_and_store("ReceiverAgreement", "ReceiverAgreement", ReceiverAgreement, build_row))

@app.route("/extract/value_mappings", methods=["GET"])
def extract_value_mappings():
    def build_row(item):
        return ValueMapping(
            GroupID=item.find("ValueMappingID").get_text() if item.find("ValueMappingID") else "",
            Description=item.find("GroupName").get_text() if item.find("GroupName") else ""
        )
    return jsonify(extract_and_store("ValueMapping", "ValueMapping", ValueMapping, build_row))

# Avvio server Flask
if __name__ == "__main__":
    app.run(debug=True, port=5001)
