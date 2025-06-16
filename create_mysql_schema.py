from app.models import Base
from app.db import mysql_engine

Base.metadata.create_all(bind=mysql_engine)
print("Створена таблиці в MySQL")