from datetime import datetime
import requests
from resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from data.database import insert_logs


async def lotus_pay_post_bank_account(context, customer_id, data):
    """ Generic Post Method for lotuspay bank accounts """
    try:
        url = f'http://api-test.lotuspay.com/v1/customers/{customer_id}/{context}/'
        str_url = str(url)
        str_data = str(data)
        bank_account_context_response = requests.post(url, data=data, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        bank_account_context_dict = response_to_dict(bank_account_context_response)
        bank_account_context_response_id = bank_account_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, bank_account_context_response.status_code, bank_account_context_response.content,
                                   datetime.now())
        result = bank_account_context_response_id
    except:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, bank_account_context_response.status_code, bank_account_context_response.content,
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})
    return result
