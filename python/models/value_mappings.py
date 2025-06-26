from models import ValueMapping,ValueMappingList, Base,engine,SessionLocal
import json
import hashlib
from utilities import xml_to_dict
from pprint import pformat
import asyncio
from loguru import logger
from status_store import get_status, set_status,StatusModel
from models.generic_sappo_logics import extract_and_store
import pendulum



def build_row(item):
    xml_str = str(item)
    ValueMappingID_ = item.find("ValueMappingID").get_text(strip=True) if item.find("ValueMappingID") else ""
    uud = ValueMappingID_
    UUID_Str = hashlib.sha256(uud.encode('utf-8')).hexdigest()
    xml_json = xml_to_dict(item)
    json_str = json.dumps(xml_json, ensure_ascii=False, indent=2)
    return ValueMapping(
        ValueMappingID= ValueMappingID_,
        UUID=UUID_Str,
        FullObjectXML=xml_str.strip() if xml_str else "",
        FullObjectJSON=pformat(json_str) if json_str else "",
        FullObject=json_str.strip() if json_str else "",
    )

def get_total():
    db = SessionLocal()
    items = db.query(ValueMappingList).all()
    total = len(items)
    return total

async def extraction_task(procedure_name: str,lock: asyncio.Lock):
    db = SessionLocal()
    try:
        items = db.query(ValueMappingList).all()
        total = len(items)
        status = await get_status(procedure_name)
        status = status.model_copy(update={"total": total})
        await set_status(procedure_name, status)

        logger.info(f"📦 Found {total} IntegratedConfigurationsList items in the database.")
        
        #TODO: rimuovi
        #maxI = 20
        #logger.warning(f"⛔️ !!!!TEMP {maxI}  ")
        results = []
        for idx, item in enumerate(items, 1):
            #maxI -= 1
            #logger.warning(f"⛔️ Changed {maxI}  ")
            #if maxI <=0:
            #    break

            single_result = extract_and_store(
                "ValueMapping",
                "ValueMappingReadRequest",
                "ValueMapping",
                ValueMapping,
                build_row,
                item.ValueMappingID,
                df_log = False
            )
            status = status.model_copy(update={"processed": idx}) 
            await set_status(procedure_name, status)
            results.append(single_result)
            #break
        status.model_copy(update={
            "result": results,
            "completed_at": str(pendulum.now()),
            "running": False
        })
        await set_status(procedure_name, status)
    except Exception as e:
        status = await get_status(procedure_name)
        status = status.model_copy(update={"running": False})
        #setattr(status, "running", False)  
        await set_status(procedure_name, status)
        logger.error(f"❌ Error in async extraction: {e}")
    finally:
        db.close()