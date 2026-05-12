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

example2 = """<CommunicationChannel>
	<MasterLanguage>EN</MasterLanguage>
	<AdministrativeData>
		<ResponsibleUserAccountID>storella</ResponsibleUserAccountID>
		<LastChangeUserAccountID>rapposel</LastChangeUserAccountID>
		<LastChangeDateTime>2021-04-15T10:24:33.459+02:00</LastChangeDateTime>
		<FolderPathID>/</FolderPathID>
	</AdministrativeData>
	<Description languageCode="EN">FATELPI@FATELPI01</Description>
	<CommunicationChannelID>
		<PartyID/>
		<ComponentID>BC_ArchiFlow_ME</ComponentID>
		<ChannelID>CC_JDBC_SND_ID_ARCHIVE_ARCHIFLOW</ChannelID>
	</CommunicationChannelID>
	<AdapterMetadata>
		<Name>JDBC</Name>
		<Namespace>http://sap.com/xi/XI/System</Namespace>
		<SoftwareComponentVersionID>0050568f-0aac-1ed4-a6e5-6926325e2eb3</SoftwareComponentVersionID>
	</AdapterMetadata>
	<Direction>Sender</Direction>
	<TransportProtocol>JDBC</TransportProtocol>
	<TransportProtocolVersion/>
	<MessageProtocol>JDBC</MessageProtocol>
	<MessageProtocolVersion>3.0.0527</MessageProtocolVersion>
	<AdapterEngineName/>
	<AdapterSpecificAttribute>
		<Name>jdbcDriver</Name>
		<Namespace/>
		<Value>com.ibm.as400.access.AS400JDBCDriver</Value>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>connectionURL</Name>
		<Namespace/>
		<Value>jdbc:as400:10.1.17.98/CSMR40DAT</Value>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>dbuser</Name>
		<Namespace/>
		<Value>FATELPI</Value>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>dbpassword</Name>
		<Namespace/>
		<Value/>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>qualityOfService</Name>
		<Namespace/>
		<Value>EO</Value>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>queueName</Name>
		<Namespace/>
		<Value/>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>pollInterval</Name>
		<Namespace/>
		<Value>300</Value>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>pollIntervalMsecs</Name>
		<Namespace/>
		<Value/>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>retryInterval</Name>
		<Namespace/>
		<Value/>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>queryStatement</Name>
		<Namespace/>
		<Value>select trim(IDARCSIAV) as IDARCSIAV, trim(USERELAB) as USERELAB  from CSMR40DAT.TPSAPFTE where COD_AZ_SIA = 'ME'</Value>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>documentname</Name>
		<Namespace/>
		<Value>MT_eDocumentCompanyCode_Jdbc</Value>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>documentnamespace</Name>
		<Namespace/>
		<Value>urn:menarini.com:integration:e-invoice</Value>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>updateStatement</Name>
		<Namespace/>
		<Value>&lt;TEST&gt;</Value>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>execute</Name>
		<Namespace/>
		<Value/>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>executeTimeout</Name>
		<Namespace/>
		<Value/>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>executeTerminateAfterTimeout</Name>
		<Namespace/>
		<Value>0</Value>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>adapterStatus</Name>
		<Namespace/>
		<Value>active</Value>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>additionalParameters</Name>
		<Namespace/>
		<Value>0</Value>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>isolationLevel</Name>
		<Namespace/>
		<Value>-1</Value>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>autoCommit</Name>
		<Namespace/>
		<Value>0</Value>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>dbdisconnect</Name>
		<Namespace/>
		<Value>0</Value>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>doNotRequireEmptyElement</Name>
		<Namespace/>
		<Value>0</Value>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>dateFormat</Name>
		<Namespace/>
		<Value/>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>timeFormat</Name>
		<Namespace/>
		<Value/>
	</AdapterSpecificAttribute>
	<AdapterSpecificAttribute>
		<Name>timestampFormat</Name>
		<Namespace/>
		<Value/>
	</AdapterSpecificAttribute>
	<AdapterSpecificTableAttribute>
		<Name>addParameterParams</Name>
		<Namespace/>
	</AdapterSpecificTableAttribute>
	<ModuleProcess>
		<ProcessStep>
			<ModuleName>CallSapAdapter</ModuleName>
			<ModuleType>Local Enterprise Bean</ModuleType>
			<ParameterGroupID>0</ParameterGroupID>
		</ProcessStep>
	</ModuleProcess>
	<SenderIdentifier schemeAgencyID="" schemeID=""/>
	<ReceiverIdentifier schemeAgencyID="" schemeID=""/>
</CommunicationChannel>
"""

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

"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(example2,'lxml-xml')
ret = xml_to_dict(soup)
print(ret)
"""