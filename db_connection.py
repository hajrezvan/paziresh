# db_connection.py

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


def get_users():
    """Fetches userid, first name, and last name of all users from the Users table."""
    query = select(users_table.c.userId, users_table.c.firstname, users_table.c.lastname)
    result = session.execute(query).fetchall()
    return result

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
