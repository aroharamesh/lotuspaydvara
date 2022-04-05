
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime

from databases import Database
from data.database import get_database, sqlalchemy_engine, insert_logs
from gateway.lotuspay_ach_debit import lotus_pay_achdbit_post, lotus_pay_achdbit_cancel
from data.achdebit_model import (
    achdebits,
    ACHDebitBase,
    ACHDebitCreate,
    ACHDebitDB,
)


router = APIRouter()


@router.post("/achdebits", response_model=ACHDebitDB, status_code=status.HTTP_201_CREATED,  tags=["ACH Debits"])
async def create_ach_debits(
    achdebit: ACHDebitCreate, database: Database = Depends(get_database)
) -> ACHDebitDB:

    try:
        achdebit_info = achdebit.dict()
        response_achdebit_id = await lotus_pay_achdbit_post('ach_debits', achdebit_info)
        print(response_achdebit_id)
        if response_achdebit_id is not None:
            achdebit_info = {
                **achdebit_info,
                'achdebit_id': response_achdebit_id,
                'created_date': datetime.now()
            }
            insert_query = achdebits.insert().values(achdebit_info)
            achdebit_id = await database.execute(insert_query)
            result = JSONResponse(status_code=200, content={"achdebit_id": response_achdebit_id})
        result = response_achdebit_id

    except:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})
    return result


@router.post("/achdebits-cancellation", status_code=status.HTTP_200_OK,  tags=["ACH Debits"])
async def create_ach_debits_cancellation(
    mandate: str, database: Database = Depends(get_database)
) -> ACHDebitDB:

    try:
        print('before posting')
        response_achdebit_id = await lotus_pay_achdbit_cancel('ach_debits', mandate)
        print('after posting', response_achdebit_id)

        result = response_achdebit_id

    except:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})
    return result