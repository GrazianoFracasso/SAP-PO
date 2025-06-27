from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_FILE
from loguru import logger
import inspect
# --- Database Setup ---

engine = create_engine(f"sqlite:///{DB_FILE}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger.info(f"🚀 Sessione DB creata")

# --- SQLAlchemy Models ---
# These models define the database schema for storing the extracted SAP PO data.



# OPZIONE 2: Crea automaticamente il dizionario usando globals()
def get_model_classes():
    """Restituisce un dizionario con tutte le classi del modello"""
    import inspect
    return {
        name: obj for name, obj in globals().items()
        if inspect.isclass(obj) and issubclass(obj, Base) and obj is not Base
    }

# OPZIONE 3: Funzione helper per ottenere una classe specifica
def get_model_class(class_name):
    """Restituisce la classe del modello per nome"""
    try:
        return globals()[class_name]
    except KeyError:
        raise ValueError(f"Classe '{class_name}' non trovata nel modulo models")

class ModelFactory:
    """Factory per creare istanze dei modelli dinamicamente"""
    
    def __init__(self, models_module):
        self.models = models_module
    
    def create_instance(self, class_name, **kwargs):
        """Crea un'istanza della classe specificata"""
        ModelClass = getattr(self.models, class_name)
        return ModelClass(**kwargs)
    
    def get_class(self, class_name):
        """Ottiene la classe specificata"""
        return getattr(self.models, class_name)
    
    def list_available_models(self):
        """Lista tutti i modelli disponibili"""
        import inspect
        return [
            name for name, obj in vars(self.models).items()
            if inspect.isclass(obj) and hasattr(obj, '__tablename__')
        ]

"""
# Uso del factory
factory = ModelFactory(models)
available_models = factory.list_available_models()
print(f"Modelli disponibili: {available_models}")

# Creare un'istanza dinamicamente
ic_instance = factory.create_instance(
    "IntegratedConfiguration",
    SenderPartyID="PARTY001",
    SenderComponentID="COMP001"
)
print(f"Istanza creata: {ic_instance}")
"""

Base = declarative_base()


class IntegratedConfiguration(Base):
    __tablename__ = 'IntegratedConfigurations'
    SenderPartyID = Column(String, primary_key=True)
    SenderComponentID = Column(String, primary_key=True)
    InterfaceName = Column(String, primary_key=True)
    InterfaceNamespace = Column(String, primary_key=True)
    ReceiverPartyID = Column(String, primary_key=True)
    ReceiverComponentID = Column(String, primary_key=True)
    UUID = Column(String, primary_key=True)
    FullObjectXML = Column(Text)
    FullObjectJSON = Column(Text)
    FullObject = Column(Text)  # This can be used to store the full object in a different format if needed

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
    ComponentID = Column(String, primary_key=True)
    ChannelID = Column(String, primary_key=True)
    PartyID = Column(String, primary_key=True)
    UUID = Column(String)
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

class SenderAgreement(Base):
    __tablename__ = 'SenderAgreements'
    SenderPartyID = Column(String, primary_key=True)
    SenderComponentID = Column(String, primary_key=True)
    InterfaceName = Column(String, primary_key=True)
    InterfaceNamespace = Column(String, primary_key=True)
    ReceiverPartyID = Column(String, primary_key=True)
    ReceiverComponentID = Column(String, primary_key=True)
    UUID = Column(String, primary_key=True)
    FullObjectXML = Column(Text)
    FullObjectJSON = Column(Text)
    FullObject = Column(Text)  # This can be used to store the full object in a different format if needed

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
    SenderPartyID = Column(String, primary_key=True)
    SenderComponentID = Column(String, primary_key=True)
    InterfaceName = Column(String, primary_key=True)
    InterfaceNamespace = Column(String, primary_key=True)
    ReceiverPartyID = Column(String, primary_key=True)
    ReceiverComponentID = Column(String, primary_key=True)
    UUID = Column(String, primary_key=True)
    FullObjectXML = Column(Text)
    FullObjectJSON = Column(Text)
    FullObject = Column(Text)  # This can be used to store the full object in a different format if needed

class ValueMapping(Base):
    __tablename__ = 'ValueMappings'
    ValueMappingID = Column(String, primary_key=True)
    UUID = Column(String)
    FullObjectXML = Column(Text)
    FullObjectJSON = Column(Text)
    FullObject = Column(Text)  # This can be used to store the full object in a different format if needed

class ValueMappingList(Base):
    __tablename__ = 'ValueMappingList'
    #id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ValueMappingID = Column(String, primary_key=True)


Base.metadata.create_all(engine)
logger.info(f"🚀 Create All tables dones")