from app.db import PostgresSession, MySQLSession
from app.models import Weather, AstronomyInfo

# Створюємо сесії
pg_session = PostgresSession()
mysql_session = MySQLSession()

try:
    # 1. Переносимо всі записи погоди
    all_weather = pg_session.query(Weather).all()
    for item in all_weather:
        data = item.__dict__.copy()
        data.pop("_sa_instance_state", None)
        data.pop("id", None)
        mysql_session.add(Weather(**data))

    mysql_session.commit()

    # 2. Переносимо астрономічну інфу
    all_astronomy = pg_session.query(AstronomyInfo).all()
    for item in all_astronomy:
        data = item.__dict__.copy()
        data.pop("_sa_instance_state", None)
        data.pop("id", None)
        mysql_session.add(AstronomyInfo(**data))

    mysql_session.commit()

    print("Дані успішно перенесено!")

except Exception as e:
    mysql_session.rollback()
    print("Помилка під час міграції:", e)

finally:
    pg_session.close()
    mysql_session.close()
