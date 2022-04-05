from datetime import datetime

import requests
from resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from data.database import get_database, sqlalchemy_engine, insert_logs


async def lotus_pay_post_source(context, data):
    """ Generic Post Method for lotuspay Sources """
    try:
        url = f'http://api-test.lotuspay.com/v1/{context}'
        str_url = str(url)
        str_data = str(data)
        source_context_response = requests.post(url, json=data, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        source_context_dict = response_to_dict(source_context_response)
        source_context_response_id = source_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())

        result = source_context_response_id

    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})
    return result


async def lotus_pay_post_source2(context, data):
    """ Generic Post Method for lotuspay Sources """
    try:
        url = f'http://api-test.lotuspay.com/v1/{context}'
        str_url = str(url)
        str_data = str(data)
        source_context_response = requests.post(url, json=data, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        source_context_dict = response_to_dict(source_context_response)
        source_context_response_id = source_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())

        result = source_context_response_id

    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})
    return result


async def lotus_pay_post_source3(context, data):
    """ Generic Post Method for lotuspay Sources """
    try:
        url = f'http://api-test.lotuspay.com/v1/{context}'
        str_url = str(url)
        str_data = str(data)
        print('coming inside source3 ', data)
        source_context_response = requests.post(url, json=data, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        source_context_dict = response_to_dict(source_context_response)
        source_context_response_id = source_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())

        result = source_context_response_id

    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, source_context_response.status_code, source_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})
    return result