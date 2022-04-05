from datetime import datetime
import requests
from resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from data.database import insert_logs


async def lotus_pay_patch_mandate(context, mandate_id, id_token, data):
    """ Generic Post Method for lotuspay customer """
    try:
        print('coming inside of lotuspay mandate')
        url = f'http://api-test.lotuspay.com/v1/{context}/{mandate_id}/update?id_token={id_token}'
        print(url)
        str_url = str(url)
        str_data = str(data)
        print(data)
        mandate_context_response = requests.patch(url, json=data, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        # print(mandate_context_response.status_code, mandate_context_response.content)
        mandate_context_dict = response_to_dict(mandate_context_response)
        mandate_context_response_id = mandate_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, mandate_context_response.status_code, mandate_context_response.content, datetime.now())
        result = mandate_context_response_id

    except:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, mandate_context_response.status_code, mandate_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})

    return result


async def lotus_pay_mandate_cancel(context, mandate_id, data):
    """ Generic Post Method for lotuspay mandate """
    try:
        url = f'http://api-test.lotuspay.com/v1/{context}/{mandate_id}/cancel'
        str_url = str(url)
        # str_data = str(data)
        print(url)
        mandate_context_response = requests.post(url, json=data, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        print(mandate_context_response)
        print(mandate_context_response.status_code)
        mandate_context_dict = response_to_dict(mandate_context_response)
        mandate_context_id = mandate_context_dict.get('id')
        print(mandate_context_response.content)
        log_id = await insert_logs(str_url, 'LOTUSPAY', mandate_id, mandate_context_response.status_code, mandate_context_response.content, datetime.now())
        # result = JSONResponse(status_code=200, content={"message": "Subscripton Deletion Accepted"})
        result = mandate_context_id
    except:
        log_id = await insert_logs(str_url, 'LOTUSPAY', mandate_id, mandate_context_response.status_code, mandate_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})

    return result