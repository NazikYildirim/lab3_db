# Weather DB Migration to MySQL — Task 5
## Про проєкт
Завдання полягало у міграції даних з PostgreSQL до MySQL з використанням SQLAlchemy. В результаті створено копію бази в MySQL, сумісну з оригінальною структурою.

## Виконано в рамках завдання 5
Налаштовано окремі engine та Session для PostgreSQL і MySQL.

Створено скрипт create_mysql_schema.py для створення таблиць у MySQL.

Створено скрипт migrate_data.py для перенесення даних з PostgreSQL до MySQL.

Забезпечено підтримку однакової структури в обох базах.

## Структура
app/db.py — обидва підключення (PostgresSession, MySQLSession)

create_mysql_schema.py — створення таблиць

migrate_data.py — перенесення даних



## Навігація по завданнях
- **Завдання 1** – опис моделей (ORM) — task-1-models
- **Завдання 2** – рефакторинг структури БД через Alembic — task-2-alembic-refactor
- **Завдання 3** – обчислення колонки is_safe_to_go_out — task-3-safety-logic
- **Завдання 4** – консольна утиліта (CLI) — task-4-cli-tool
- **Завдання 5** – міграція з PostgreSQL до MySQL — task-5-mysql-migration
