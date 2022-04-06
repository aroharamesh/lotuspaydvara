
import logging
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime

from databases import Database
from data.database import get_database, sqlalchemy_engine, insert_logs
from gateway.lotuspay_source import lotus_pay_post_source, lotus_pay_post_source2, lotus_pay_post_source3
from data.source_model import (
    sources,
    SourceBase,
    SourceCreate,
    SourceDB,
    Source2Create,
    Source3Create
)

router = APIRouter()

logger = logging.getLogger("arthmate-lender-handoff-service")


async def get_source_or_404(
    source: str,
    database: Database = Depends(get_database)
) -> SourceDB:
    # print('coming inside of get source')
    # print(source)

    select_query = sources.select().where(sources.c.source_id == source)
    # print(select_query)
    raw_source = await database.fetch_one(select_query)
    # print(raw_source)

    if raw_source is None:
        return None

    return SourceDB(**raw_source)


@router.post("/source", status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def create_source(
    source: SourceCreate,
        database: Database = Depends(get_database)
) -> SourceDB:

    try:
        print('Coming inside of Source')
        source_info = source.dict()
        source_id = source_info.get('source_id')

        verify_source_in_db = await get_source_or_404(source_id, database)
        if verify_source_in_db is None:
            response_source_id = await lotus_pay_post_source('sources', source_info)
            if response_source_id is not None:
                store_record_time = datetime.now()
                nach_debit = source_info.get('nach_debit')
                nach_type = source_info.get('type')
                nach_debit['type'] = nach_type
                nach_debit['source_id'] = response_source_id
                nach_debit['created_date'] = store_record_time
                insert_query = sources.insert().values(nach_debit)
                source_id = await database.execute(insert_query)

                result = JSONResponse(status_code=200, content={"source_id": response_source_id})
            else:
                log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                           datetime.now())
                result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})

        else:
            print('Source already exists in DB')
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Source Already Exists in DB',
                                       datetime.now())
            result = JSONResponse(status_code=200, content={"message": "Source Already Exists in DB"})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})

    return result


@router.post("/source/{customer_id}", status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def customer_source(
    source2: Source2Create,
        database: Database = Depends(get_database)
) -> SourceDB:

    try:
        print('Coming inside of Customer')
        source_info = source2.dict()
        source_id = source_info.get('source_id')
        redirect = source_info.get('redirect')
        str_redirect = str(redirect)
        customer = source_info.get('customer')
        verify_source_in_db = await get_source_or_404(source_id, database)
        if verify_source_in_db is None:
            response_source_id = await lotus_pay_post_source2('sources', source_info)
            if response_source_id is not None:
                store_record_time = datetime.now()

                nach_debit = source_info.get('nach_debit')
                nach_type = source_info.get('type')
                nach_debit['type'] = nach_type
                nach_debit['source_id'] = response_source_id
                nach_debit['created_date'] = store_record_time
                nach_debit['redirect'] = str_redirect
                nach_debit['customer'] = customer
                insert_query = sources.insert().values(nach_debit)
                source_id = await database.execute(insert_query)

                result = JSONResponse(status_code=200, content={"source_id": response_source_id})
            else:
                log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                           datetime.now())
                result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})

        else:
            print('Source already exists in DB')
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Source Already Exists in DB',
                                       datetime.now())
            result = JSONResponse(status_code=200, content={"message": "Source Already Exists in DB"})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})

    return result


@router.post("/source/{bank_account}", response_model=SourceDB, status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def source_bank_account(
    source3: Source3Create,
        database: Database = Depends(get_database)
) -> SourceDB:

    try:
        print('Coming inside of Bank Account')
        source_info = source3.dict()
        print('comingg isndfns')
        print(source_info)
        source_id = source_info.get('bank_account')
        redirect = source_info.get('redirect')
        str_redirect = str(redirect)
        bank_account = source_info.get('bank_account')
        # verify_source_in_db = await get_source_or_404(source_id, database)
        # if verify_source_in_db is None:
        response_source_id = await lotus_pay_post_source3('sources', source_info)
        if response_source_id is not None:
            store_record_time = datetime.now()

            nach_debit = source_info.get('nach_debit')
            nach_type = source_info.get('type')
            nach_debit['type'] = nach_type
            nach_debit['source_id'] = response_source_id
            nach_debit['created_date'] = store_record_time
            nach_debit['redirect'] = str_redirect
            nach_debit['bank_account'] = bank_account
            insert_query = sources.insert().values(nach_debit)
            source_id = await database.execute(insert_query)

            result = JSONResponse(status_code=200, content={"source_id": response_source_id})
        else:
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                       datetime.now())
            result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})

        # else:
        #     print('Source already exists in DB')
        #     log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Source Already Exists in DB',
        #                                datetime.now())
        #     result = JSONResponse(status_code=200, content={"message": "Source Already Exists in DB"})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})

    return result


