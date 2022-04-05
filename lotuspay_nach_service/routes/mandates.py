from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime

from databases import Database
from data.database import get_database, sqlalchemy_engine, insert_logs
from gateway.lotuspay_mandate import lotus_pay_patch_mandate, lotus_pay_mandate_cancel


from data.mandate_model import (
    mandates,
    MandateBase,
    MandateCreate,
    MandateDB,
    mandates_cancel,
    MandateCancelCreate
)


router = APIRouter()


@router.post("/mandate", response_model=MandateDB, status_code=status.HTTP_201_CREATED,  tags=["Mandates"])
async def update_mandate(
        id_token: str,
        mandate_id: str,
    mandate: MandateCreate, database: Database = Depends(get_database)
) -> MandateDB:
    try:
        print('thank you')
        mandate_info = mandate.dict()
        response_mandate_id = await lotus_pay_patch_mandate('mandates', mandate_id, id_token, mandate_info)
        if response_mandate_id is not None:
            store_record_time = datetime.now()
            mandate_info = {
                'mandate_id': mandate_id,
                'metadata': str(mandate_info),
                'created_date': store_record_time
            }
            insert_query = mandates.insert().values(mandate_info)
            mandate_db_id = await database.execute(insert_query)
            result = JSONResponse(status_code=200, content={"mandate_id": mandate_db_id})
    except Exception as e:
        print('thank you', e.args[0])
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', e.args[0],
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})
    return result


@router.post("/mandate-cancellation", status_code=status.HTTP_200_OK,  tags=["Mandates"])
async def mandate_cancellation(
        reason: MandateCancelCreate,
        mandate_id: str,
        database: Database = Depends(get_database)
) -> MandateDB:

    try:
        print('before posting')
        reason_info = reason.dict()
        response_mandate_id = await lotus_pay_mandate_cancel('mandates', mandate_id, reason_info)
        print('after posting', response_mandate_id)
        store_record_time = datetime.now()
        if response_mandate_id is not None:
            mandate_info = {
                'mandate_id': response_mandate_id,
                'created_date': store_record_time
            }
            delete_query = mandates_cancel.insert().values(mandate_info)
            print(delete_query)
            mandate_id = await database.execute(delete_query)
        result = response_mandate_id

    except:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})
    return result
