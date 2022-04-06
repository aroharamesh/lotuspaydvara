from datetime import datetime
import requests
from resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from data.database import insert_logs
from resource.config import settings
from resource.commons import get_env_or_fail, get_env

# from commons import get_env_or_fail

LOTUSPAY_SERVER = 'lotus-pay-server'


# async def lotus_pay_post(context, data):
#     """ Generic Post Method for lotuspay customer """
#     try:
#         url = f'http://api-test.lotuspay.com/v1/{context}/'
#         str_url = str(url)
#         str_data = str(data)
#         customer_context_response = requests.post(url, data=data, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
#         customer_context_dict = response_to_dict(customer_context_response)
#         customer_context_response_id = customer_context_dict.get('id')
#         log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, customer_context_response.status_code, customer_context_response.content, datetime.now())
#         result = customer_context_response_id
#
#     except:
#         log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, customer_context_response.status_code, customer_context_response.content, datetime.now())
#         result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})
#
#     return result


async def lotus_pay_post(context, data,
                         # settings: Settings = Depends(get_settings)
                         ):
    """ Generic Post Method for lotuspay customer """
    try:
        print('coming inside lotus pay post')
        db_section = 'lotuspay-server'

        # print(settings.lotuspay_url)
        # h = get_env(db_section, 'lotuspay-url')
        # print(h)
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        print(validate_url)
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')

        print(api_key)

        # url = f'http://api-test.lotuspay.com/v1/{context}/'
        url = validate_url + f'/{context}/'
        str_url = str(url)
        str_data = str(data)
        # customer_context_response = requests.post(url, data=data, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        customer_context_response = requests.post(url, data=data, auth=(api_key, ''))
        customer_context_dict = response_to_dict(customer_context_response)
        customer_context_response_id = customer_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, customer_context_response.status_code, customer_context_response.content, datetime.now())
        result = customer_context_response_id

    except Exception as e:
        print(e.args[0])
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, customer_context_response.status_code, customer_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})

    return result

