import logging
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime
from sqlalchemy.sql import text
from databases import Database
from data.database import get_database, sqlalchemy_engine, insert_logs
from gateway.perdix import perdix_post_login, perdix_fetch_customer

router = APIRouter()


@router.post("/perdix-customer", status_code=status.HTTP_200_OK,  tags=["Perdix"])
async def fetch_customer(customer_id):
    try:
        # test = await perdix_post_login('data')
        test = await perdix_fetch_customer(customer_id)
        print(test)

        result = test
        print(customer_id)
        return result
    except Exception as e:
        print(e.args[0])