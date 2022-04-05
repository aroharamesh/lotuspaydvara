from datetime import datetime
import requests
from resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from data.database import insert_logs


async def lotus_pay_achdbit_post(context, data):
    """ Generic Post Method for lotuspay achdebit """
    try:
        url = f'http://api-test.lotuspay.com/v1/{context}/'
        str_url = str(url)
        str_data = str(data)
        print(str_url)
        print(str_data)
        achdebit_context_response = requests.post(url, data=data, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        achdebit_context_dict = response_to_dict(achdebit_context_response)
        achdebit_context_response_id = achdebit_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, achdebit_context_response.status_code, achdebit_context_response.content, datetime.now())
        result = achdebit_context_response_id

    except:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, achdebit_context_response.status_code, achdebit_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})

    return result


async def lotus_pay_achdbit_cancel(context, mandate_id):
    """ Generic Post Method for lotuspay achdebit """
    try:
        url = f'http://api-test.lotuspay.com/v1/{context}/{mandate_id}/cancel'
        str_url = str(url)
        # str_data = str(data)
        print(url)
        achdebit_context_response = requests.post(url, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        print(achdebit_context_response.status_code)
        achdebit_context_dict = response_to_dict(achdebit_context_response)
        print(achdebit_context_response.content)
        # achdebit_context_response_id = achdebit_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', mandate_id, achdebit_context_response.status_code, achdebit_context_response.content, datetime.now())
        result = achdebit_context_response_id

    except:
        log_id = await insert_logs(str_url, 'LOTUSPAY', mandate_id, achdebit_context_response.status_code, achdebit_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})

    return result

