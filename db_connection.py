# db_connection.py
from sqlalchemy import Table, Column, String, DateTime, Integer
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker

# MySQL connection URL
DATABASE_URL = 'mysql+pymysql://root:jcAetE0zOzd9grEdw5UFgwWK@kazbek.liara.cloud:33786/javanan4'

# Create engine and bind metadata
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Reflect the Users table from the database
users_table = Table('Users', metadata, autoload_with=engine)
event_table = Table('EventType', metadata, autoload_with=engine)
meetings_table = Table('Event', metadata,
                    Column('name', String(255)),
                    Column('date', DateTime),
                    Column('type', Integer)
                    )

def get_events_type():
    query = select(event_table.c.id, event_table.c.eventType)
    result = session.execute(query).fetchall()
    return result

def get_users():
    """Fetches userid, first name, and last name of all users from the Users table."""
    query = select(users_table.c.userId, users_table.c.firstname, users_table.c.lastname)
    result = session.execute(query).fetchall()
    return result


def insert_event(name, date, event_type):
    """Inserts a new event into the Event table."""
    print(name + ' ' + str(date) +  ' ' + event_type)              
    insert_query = meetings_table.insert().values(name=name, date=date, type=event_type)
    session.execute(insert_query)
    session.commit()
    return True, None

def add_user(userid, firstname, lastname):
    """Inserts a new user into the Users table. Returns success status and an error message."""
    # Check if the userid already exists
    query = select(users_table.c.userId).where(users_table.c.userId == userid)
    result = session.execute(query).fetchone()

    if result:
        return False, "کد گروهی تکراری است"  # "Group ID is duplicated"

    # Insert the new user
    try:
        insert_query = users_table.insert().values(userId=userid, firstname=firstname, lastname=lastname)
        session.execute(insert_query)
        session.commit()
        return True, None
    except Exception as e:
        session.rollback()
        return False, str(e)

def get_meetings():
    """Fetches all meetings from the Event table."""
    query = select(meetings_table.c.name, meetings_table.c.date, meetings_table.c.type)
    result = session.execute(query).fetchall()
    return result