import sqlalchemy
from databases import Database
from lotuspay_nach_service.data.logs_model import applogs


# DATABASE_URL = "sqlite:///chapter6_sqlalchemy.db"
# DATABASE_URL = "mysql+pymysql://root:Aroha123@localhost/Aroha"
DATABASE_URL = "mysql+pymysql://root:Aroha123@172.17.0.2/Aroha"
# DATABASE_URL = "mysql+pymysql://admin:7f06EX0Tk2vUSMun966j@spicemoney-db-host/lotuspay"
database = Database(DATABASE_URL)
sqlalchemy_engine = sqlalchemy.create_engine(DATABASE_URL)


def get_database() -> Database:
    return database


async def insert_logs(url, app_type, request_json, status_code, content, created):
    Database = get_database()
    log_info = {'request': url,
                'request_type': 'POST',
                'app_type': app_type,
                'request_json': request_json,
                'response_status': status_code,
                'response_content': content,
                'created_date': created}
    insert_query = applogs.insert().values(log_info)
    log_id = await Database.execute(insert_query)
    return log_id
