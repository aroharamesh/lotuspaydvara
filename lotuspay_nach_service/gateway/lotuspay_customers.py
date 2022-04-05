from datetime import datetime
import requests
from resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from data.database import insert_logs


async def lotus_pay_post(context, data):
    """ Generic Post Method for lotuspay customer """
    try:
        url = f'http://api-test.lotuspay.com/v1/{context}/'
        str_url = str(url)
        str_data = str(data)
        customer_context_response = requests.post(url, data=data, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        customer_context_dict = response_to_dict(customer_context_response)
        customer_context_response_id = customer_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, customer_context_response.status_code, customer_context_response.content, datetime.now())
        result = customer_context_response_id

    except:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, customer_context_response.status_code, customer_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})

    return result

