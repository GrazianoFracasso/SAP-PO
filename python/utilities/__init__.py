import inspect
myself = lambda: inspect.stack()[1][3]

example = """<IntegratedConfiguration>
	<MasterLanguage>EN</MasterLanguage>
	<AdministrativeData>
		<ResponsibleUserAccountID>sburleal</ResponsibleUserAccountID>
		<LastChangeUserAccountID>sburleal</LastChangeUserAccountID>
		<LastChangeDateTime>2020-10-16T10:56:38.123+02:00</LastChangeDateTime>
		<FolderPathID>/</FolderPathID>
	</AdministrativeData>
	<Description languageCode="EN">SD Small Sales Shipment to Tracelink Kaluga</Description>
	<IntegratedConfigurationID>
		<SenderPartyID/>
		<SenderComponentID>M1QCLNT500</SenderComponentID>
		<InterfaceName>ZRU_SD_SMALL_SHP.ZRU_SHIPINT</InterfaceName>
		<InterfaceNamespace>urn:sap-com:document:sap:idoc:messages</InterfaceNamespace>
		<ReceiverPartyID/>
		<ReceiverComponentID/>
	</IntegratedConfigurationID>
	<InboundProcessing>
		<SenderInterfaceSoftwareComponentVersion>66eeb600-e04b-11e9-bf39-ebbe0a640c6f</SenderInterfaceSoftwareComponentVersion>
		<CommunicationChannel>
			<PartyID/>
			<ComponentID>M1QCLNT500</ComponentID>
			<ChannelID>DefaultIDOCSender</ChannelID>
		</CommunicationChannel>
		<SchemaValidationIndicator>false</SchemaValidationIndicator>
		<VirusScan>Use Global</VirusScan>
	</InboundProcessing>
	<Receivers>
		<ReceiverRule>
			<Receiver>
				<PartyID>Kaluga</PartyID>
				<ComponentID>TRACELINK_TST</ComponentID>
			</Receiver>
		</ReceiverRule>
		<NoReceiverBehaviour>Error Message</NoReceiverBehaviour>
	</Receivers>
	<ReceiverInterfaces>
		<Receiver>
			<PartyID>Kaluga</PartyID>
			<ComponentID>TRACELINK_TST</ComponentID>
		</Receiver>
		<ReceiverInterfaceRule>
			<Operation>ZRU_SD_SMALL_SHP.ZRU_SHIPINT</Operation>
			<Mapping>
				<Name>OM_SalesShipment_Small_SKTTK</Name>
				<Namespace>urn:menarini.com:integration:tracelink:SalesShipment_SKTTK</Namespace>
				<SoftwareComponentVersionID>66eeb600-e04b-11e9-bf39-ebbe0a640c6f</SoftwareComponentVersionID>
			</Mapping>
			<Interface>
				<Name>SI_SalesShipment_Small_SKTTK_ASYNC_IN</Name>
				<Namespace>urn:menarini.com:integration:tracelink:SalesShipment_SKTTK</Namespace>
				<SoftwareComponentVersionID>66eeb600-e04b-11e9-bf39-ebbe0a640c6f</SoftwareComponentVersionID>
			</Interface>
		</ReceiverInterfaceRule>
		<QualityOfService>EO</QualityOfService>
	</ReceiverInterfaces>
	<OutboundProcessing>
		<Receiver>
			<PartyID>Kaluga</PartyID>
			<ComponentID>TRACELINK_TST</ComponentID>
		</Receiver>
		<ReceiverInterface>
			<Name>SI_SalesShipment_Small_SKTTK_ASYNC_IN</Name>
			<Namespace>urn:menarini.com:integration:tracelink:SalesShipment_SKTTK</Namespace>
			<SoftwareComponentVersionID>66eeb600-e04b-11e9-bf39-ebbe0a640c6f</SoftwareComponentVersionID>
		</ReceiverInterface>
		<CommunicationChannel>
			<PartyID>Kaluga</PartyID>
			<ComponentID>TRACELINK_TST</ComponentID>
			<ChannelID>CC_SFTP_SalesShipment_SKTTK_Receiver</ChannelID>
		</CommunicationChannel>
		<SchemaValidationIndicator>false</SchemaValidationIndicator>
		<VirusScan>Use Global</VirusScan>
		<HeaderMapping>
			<Sender/>
			<Receiver/>
		</HeaderMapping>
	</OutboundProcessing>
	<Logging>
		<UseGlobal>false</UseGlobal>
		<SpecificConfiguration>BI=0,MS=2,AM=2</SpecificConfiguration>
	</Logging>
	<Staging>
		<UseGlobal>false</UseGlobal>
		<SpecificConfiguration>BI=0,VI=0,MS=3,AM=3,VO=0</SpecificConfiguration>
	</Staging>
</IntegratedConfiguration>"""

def xml_to_dict(element, skip_html_body=True):
    # Skip automatically added html/body tags if they weren't in original XML
    if skip_html_body and element.name and element.name.lower() in ['html', 'body']:
        # If html/body has only one child element, return that child's content
        child_elements = element.find_all(recursive=False)
        if len(child_elements) == 1:
            return xml_to_dict(child_elements[0], skip_html_body)
        elif len(child_elements) > 1:
            # Multiple children, process normally but skip the wrapper
            result = {}
            for child in child_elements:
                key = child.name
                value = xml_to_dict(child, skip_html_body)
                
                if key in result:
                    if not isinstance(result[key], list):
                        result[key] = [result[key]]
                    result[key].append(value)
                else:
                    result[key] = value
            return result
    
    # Recursively convert BeautifulSoup XML element to dict
    
    # Check if element has no child elements (only text content)
    child_elements = element.find_all(recursive=False)
    
    if not child_elements:
        # Element has no child elements, return its text content
        text = element.get_text(strip=True)
        return text if text else None
    
    # Element has child elements, process them
    result = {}
    for child in child_elements:
        key = child.name
        value = xml_to_dict(child, skip_html_body)
        
        if key in result:
            # If key already exists, convert to list
            if not isinstance(result[key], list):
                result[key] = [result[key]]
            result[key].append(value)
        else:
            result[key] = value
    
    return result

from bs4 import BeautifulSoup
soup = BeautifulSoup(example,'lxml-xml')
ret = xml_to_dict(soup)
print(ret)