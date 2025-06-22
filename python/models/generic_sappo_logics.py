from tqdm import tqdm
from bs4 import BeautifulSoup
from store_data import SessionLocal,engine
from loguru import logger
from requests.auth import HTTPBasicAuth
import requests
import traceback
import uuid
import pandas as pd
from tabulate import tabulate
from pprint import pformat,pprint
import pendulum
from config import USERNAME,PASSWORD,HOST
import os


# --- SOAP Request Handling ---
HEADERS = {
    "Content-Type": "text/xml;charset=UTF-8",
    "SOAPAction": "http://sap.com/xi/WebService/soap1.1"
}

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

# --- Generic Extraction Logic ---
def extract_and_store(endpoint_key, query_tag, result_tag, model_cls, row_builder, item=None, df_log = True):
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
        
        if df_log:
            df = pd.read_sql_table(model_cls.__tablename__, engine)
            logger.info(f"✅ Successfully stored {len(df)} rows in '{model_cls.__tablename__}'. Sample data:\n" +
                tabulate(df.head(1), headers="keys", tablefmt="pretty",maxcolwidths=400,maxheadercolwidths=400))
        else:
            logger.info(f"✅ Successfully stored {len(results)} rows in '{model_cls.__tablename__}'.")

        return {"status": "success", "rows_processed": len(results)}

    except Exception as e:
        db.rollback()
        logger.error(f"❌ An error occurred during extraction for {endpoint_key}: {e}")

        logger.exception(f"💥 Stacktrace for extraction error in {endpoint_key}: {traceback.format_exc()}")

        return {"status": "error", "message": str(e)}
    finally:
        db.close()
        logger.info(f"🏁 Finished extraction for {endpoint_key}.")