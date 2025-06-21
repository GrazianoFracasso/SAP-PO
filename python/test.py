import requests
import pandas as pd
from loguru import logger

# Set up logging
logger.add("soap_request.log", rotation="1 MB", level="INFO")

def InterfaceConfiguration():
    # Define the URL and the payload
    url = "http://sappod.menarini.net:54000/IntegratedConfigurationInService/IntegratedConfigurationInImplBean"
    payload = """<?xml version="1.0" encoding="UTF-8"?>\r\n
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                    xmlns:web="http://sap.com/xi/BASIS">
    <soapenv:Header/>
    <soapenv:Body>
        <web:IntegratedConfigurationQueryRequest>
            <!-- Add any required query parameters here -->
        </web:IntegratedConfigurationQueryRequest>
    </soapenv:Body>
    </soapenv:Envelope>"""

    # Define headers
    headers = {
        'Content-Type': "text/xml",
        'SOAPAction': "http://sap.com/xi/WebService/soap1.1",
        'Authorization': "Basic U1VQLkZSQUNBU1NHOmluaTAwaW5p",
        'User-Agent': "PostmanRuntime/7.15.2",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "b2c1091c-b6d9-483d-ab22-f76ce659b5c4,9d056f19-9a34-45d5-853e-00911ba1493b",
        'Host': "sappod.menarini.net:54000",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "470",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    # Send the request
    logger.info("Sending SOAP request to the service.")
    response = requests.request("POST", url, data=payload, headers=headers)

    # Log the status code and response
    logger.info(f"Response Status Code: {response.status_code}")
    logger.info("Response received successfully.")

    # Parse the response (XML to DataFrame)
    from xml.etree import ElementTree as ET

    # Parse the XML response
    root = ET.fromstring(response.text)

    # Extract data into a list of dictionaries
    data = []
    for integrated_configuration in root.findall(".//IntegratedConfigurationID", namespaces={'ns2': 'http://sap.com/xi/BASIS'}):
        record = {
            "SenderPartyID": integrated_configuration.find("SenderPartyID").text if integrated_configuration.find("SenderPartyID") is not None else "",
            "SenderComponentID": integrated_configuration.find("SenderComponentID").text if integrated_configuration.find("SenderComponentID") is not None else "",
            "InterfaceName": integrated_configuration.find("InterfaceName").text if integrated_configuration.find("InterfaceName") is not None else "",
            "InterfaceNamespace": integrated_configuration.find("InterfaceNamespace").text if integrated_configuration.find("InterfaceNamespace") is not None else "",
            "ReceiverPartyID": integrated_configuration.find("ReceiverPartyID").text if integrated_configuration.find("ReceiverPartyID") is not None else "",
            "ReceiverComponentID": integrated_configuration.find("ReceiverComponentID").text if integrated_configuration.find("ReceiverComponentID") is not None else "",
        }
        data.append(record)

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)

    # Save DataFrame to Excel
    excel_file_path = "integrated_configuration_response.xlsx"

    from tabulate import tabulate

    # Display the top rows of the DataFrame in a tabular format
    print(tabulate(df.head(), headers='keys', tablefmt='pretty'))

    df.to_excel(excel_file_path, index=False)



    # Log the DataFrame save
    logger.info(f"Data saved successfully to {excel_file_path}")


InterfaceConfiguration()
# Print a message indicating the file save
logger.info("Process completed.")
