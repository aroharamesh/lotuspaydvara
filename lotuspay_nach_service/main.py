import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware


from lotuspay_nach_service.routes.customers import router as customer_router
from lotuspay_nach_service.routes.bank_accounts import router as bank_account_router
from lotuspay_nach_service.routes.sources import router as source_router
from lotuspay_nach_service.routes.subscriptions import router as subscriptions_router
from lotuspay_nach_service.routes.ach_debits import router as achdebits_router
from lotuspay_nach_service.routes.mandates import router as mandate_router
from lotuspay_nach_service.routes.events_status import router as events_router
from lotuspay_nach_service.routes.perdix import router as perdix_router
from lotuspay_nach_service.routes.lotuspay_events import router as lotuspay_event_router
from lotuspay_nach_service.data.database import get_database, sqlalchemy_engine
from lotuspay_nach_service.data.customer_model import (customer_metadata)
from lotuspay_nach_service.data.bankaccount_model import (bankaccount_metadata)
from lotuspay_nach_service.data.source_model import source_metadata, perdix_metadata
from lotuspay_nach_service.data.subscription_model import (subscription_metadata)
from lotuspay_nach_service.data.achdebit_model import (achdebit_metadata)
from lotuspay_nach_service.data.mandate_model import (mandate_metadata)
from lotuspay_nach_service.data.events_model import (events_metadata)


from lotuspay_nach_service.data.logs_model import (logs_metadata)

origins = ["*"]


app = FastAPI(title="Perdix-LotusPay",
              debug=True,
    description='testing the descrption',
    version="0.0.1",
    terms_of_service="http://dvara.com/terms/",
    contact={
        "name": "Lotus Pay Integration",
        "url": "http://x-force.example.com/contact/",
        "email": "contact@dvara.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await get_database().connect()
    # metadata.create_all(sqlalchemy_engine)
    customer_metadata.create_all(sqlalchemy_engine)
    bankaccount_metadata.create_all(sqlalchemy_engine)
    source_metadata.create_all(sqlalchemy_engine)
    perdix_metadata.create_all(sqlalchemy_engine)
    subscription_metadata.create_all(sqlalchemy_engine)
    logs_metadata.create_all(sqlalchemy_engine)
    achdebit_metadata.create_all(sqlalchemy_engine)
    mandate_metadata.create_all(sqlalchemy_engine)
    events_metadata.create_all(sqlalchemy_engine)


@app.on_event("shutdown")
async def shutdown():
    await get_database().disconnect()

app.include_router(customer_router, prefix="")
app.include_router(bank_account_router, prefix="/bank-account")
app.include_router(perdix_router, prefix="")
app.include_router(source_router, prefix="")
app.include_router(subscriptions_router, prefix="")
app.include_router(achdebits_router, prefix="")
app.include_router(mandate_router, prefix="")
app.include_router(events_router, prefix="")
app.include_router(lotuspay_event_router, prefix="")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)
