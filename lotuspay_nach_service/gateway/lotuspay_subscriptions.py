from datetime import datetime
import requests
from resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from data.database import insert_logs


async def lotus_pay_post_subscriptions(context, data):
    """ Generic Post Method for lotuspay Subscription """
    try:
        print('coming inside of lotups pay subscritiopn')
        url = f'http://api-test.lotuspay.com/v1/{context}/'
        print(url)
        print(data)
        str_url = str(url)
        str_data = str(data)
        subscription_context_response = requests.post(url, json=data, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        print('response',subscription_context_response)
        subscription_context_dict = response_to_dict(subscription_context_response)
        subscription_context_response_id = subscription_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, subscription_context_response.status_code, subscription_context_response.content, datetime.now())
        print('logid is ', log_id)
        result = subscription_context_response_id

    except:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, subscription_context_response.status_code, subscription_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})

    return result


async def lotus_pay_subscription_cancel(context, subscription_id):
    """ Generic Post Method for lotuspay achdebit """
    try:
        url = f'http://api-test.lotuspay.com/v1/{context}/{subscription_id}/cancel'
        str_url = str(url)
        # str_data = str(data)
        print(url)
        subscription_context_response = requests.post(url, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        print(subscription_context_response)
        print(subscription_context_response.status_code)
        achdebit_context_dict = response_to_dict(subscription_context_response)
        achdebit_context_id = achdebit_context_dict.get('id')
        print(subscription_context_response.content)
        # achdebit_context_response_id = achdebit_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', subscription_id, subscription_context_response.status_code, subscription_context_response.content, datetime.now())
        # result = JSONResponse(status_code=200, content={"message": "Subscripton Deletion Accepted"})
        result = achdebit_context_id
    except:
        log_id = await insert_logs(str_url, 'LOTUSPAY', subscription_id, subscription_context_response.status_code, subscription_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})

    return result