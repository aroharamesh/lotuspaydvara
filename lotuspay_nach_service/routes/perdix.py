import logging
from starlette.responses import Response
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime
from databases import Database
from data.database import get_database, sqlalchemy_engine, insert_logs
from gateway.perdix import perdix_lotuspay_source_status
from routes.events_status import get_event_status
from resource.generics import response_to_dict
from gateway.perdix import perdix_post_login,perdix_fetch_customer
from gateway.lotuspay_source import lotus_pay_post_source5
from data.database import get_database, sqlalchemy_engine, insert_logs
from data.source_model import perdix_customer, SourceDB

router = APIRouter()


@router.post("/perdix/{customer_id}",status_code=status.HTTP_200_OK,  tags=["Perdix"])
async def get_customer(customer_id,
    database: Database = Depends(get_database)
) -> SourceDB:
    try:

        store_record_time = datetime.now()
        result = {}
        request_payload={
            "type": "nach_debit"
        }
        get_perdix_data = await perdix_fetch_customer(customer_id)
        # print('getting customer', test)
        perdix_save={}
        enrollment_id = get_perdix_data.get("enrollmentId")
        firstName = (get_perdix_data.get("firstName") if get_perdix_data.get("firstName") else "")
        lastName = (get_perdix_data.get("lastName") if get_perdix_data.get("lastName") else "")
        result["debtor_account_name"] = firstName + '' + lastName
        result["amount_maximum"] = 10000
        result["debtor_email"] = get_perdix_data.get("emailId")
        result["debtor_mobile"] = get_perdix_data.get("mobileNo")
        customer_bank_details=get_perdix_data.get('customerBankAccounts')[0]
        print('customer bank account details',customer_bank_details )
        if customer_bank_details:
            print('yes found')
            result["debtor_account_name"] = customer_bank_details.get("customerNameAsInBank")
            result["debtor_agent_mmbid"] = customer_bank_details.get("ifscCode")
            result["debtor_account_number"] = customer_bank_details.get("accountNumber")
            result["debtor_account_type"] = customer_bank_details.get("accountType").lower()
        else:
            result["debtor_account_name"] = "AMIT JAIN"
            result["debtor_agent_mmbid"] = "ICIC0000001"
            result["debtor_account_number"] = "12345678"
            result["debtor_account_type"] = "savings"
            # result = {"error": "customer bank details not found"}
            print('not found')
        request_payload["nach_debit"] = result

        source_detail = await lotus_pay_post_source5('sources', request_payload, perdix=True)
        source_id = source_detail.get('id')
        perdix_save['mandate_url']=source_detail.get("redirect").get("url")

        perdix_save['source_id']=source_detail.get('id')
        perdix_save['perdix_customer_id'] = customer_id
        perdix_save['source_status']=source_detail.get('status')
        perdix_save['created_date']=store_record_time
        perdix_save['perdix_enrollment_id'] = enrollment_id
        print('perdix - saving - ', perdix_save)
        insert_query = perdix_customer.insert().values(perdix_save)
        source_id = await database.execute(insert_query)

        result = {"Mandate_url": perdix_save['mandate_url']}
    except Exception as e:
        print(e.args[0])
        result = {"error": e.args[0]}
    return result


@router.patch("/source-status/{source_id}", status_code=status.HTTP_200_OK,  tags=["Perdix"])
async def update_perdix_status(src_id:str, database: Database = Depends(get_database)
):
      try:
          mandate_id,  mandate_status, customer_id = await perdix_lotuspay_source_status(src_id)
          if mandate_id is not None:

            query = perdix_customer.update().where(perdix_customer.c.source_id==src_id).values(mandate_id=mandate_id, mandate_status=mandate_status, lotuspay_customer_id=customer_id)
            print('printing query', query)
            source_id = await database.execute(query)
            result = {"mandate_id": mandate_id}
      except Exception as e:
           log_id = await insert_logs('MYSQL', 'DB', 'UPDATE-SOURCE-STATUS', '500', {e.args[0]},
                                     datetime.now())
           result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
      return result