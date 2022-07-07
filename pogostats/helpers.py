from sqlalchemy import create_engine
from pogostats import Session, Base

def load_db_session():
    session = Session()
    return session

def get_query_columns(query):
    column_descriptions = query.column_descriptions
    columns = [column_desc['name'] for column_desc in column_descriptions]
    return columns