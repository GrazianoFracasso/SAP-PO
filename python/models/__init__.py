from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Text
# --- SQLAlchemy Models ---
# These models define the database schema for storing the extracted SAP PO data.
Base = declarative_base()

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