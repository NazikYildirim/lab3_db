from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_DATABASE_URL = os.getenv("DB_URL")
pg_engine = create_engine(POSTGRES_DATABASE_URL)
PostgresSession = sessionmaker(autocommit=False, autoflush=False, bind=pg_engine)

MYSQL_DATABASE_URL = "mysql+pymysql://root@localhost/weather_db_mysql"
mysql_engine = create_engine(MYSQL_DATABASE_URL)
MySQLSession = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)



# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import os
# from dotenv import load_dotenv
# 
# load_dotenv()
# DATABASE_URL = os.getenv("DB_URL")
# 
# MYSQL_DATABASE_URL = "mysql+pymysql://root@localhost/weather_db_mysql"
# 
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)