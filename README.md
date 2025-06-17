# Weather Database Refactor — Task 2

## Про проєкт

Цей проєкт є частиною лабораторної роботи з міграції бази даних. Він реалізує рефакторинг структури погодної бази даних за допомогою ORM SQLAlchemy та інструменту міграцій Alembic. В якості джерела використано глобальний CSV-датасет з погодними даними. Мета — винести інформацію про сходи й заходи небесних тіл в окрему таблицю.

## Виконано в рамках завдання 2

Створено дві таблиці:
- weather – містить загальні погодні дані (наприклад, country, wind_kph, sunrise тощо)
- astronomy_info – містить колонки, що стосуються небесних тіл (sunset, moonrise, moon_phase тощо) та пов’язана з weather через зовнішній ключ weather_id.

Між таблицями встановлено зв'язок один до одного. Дублікати записів не імпортуються.

## Технічний стек

- Python
- PostgreSQL
- SQLAlchemy
- Alembic
- pgAdmin 4

## Структура проєкту

- app/models.py — опис ORM моделей
- app/db.py — створення engine та session
- app/main.py — імпорт даних із CSV
- alembic/ — міграції
- alembic.ini, env.py — конфігурація
- .env — зберігаються чутливі дані для підключення

## Налаштування та запуск

1. Створення віртуального середовища:
python -m venv venv
.\venv\Scripts\activate для Windows
2. Встановлення залежностей:
pip install -r requirements.txt
3. Застосування міграцій:
alembic upgrade head
4. Імпорт даних:
python -m app.main

## 🔍 Навігація по завданнях

- **Завдання 1** – опис моделей (ORM) - task-1-models
- **Завдання 2** – рефакторинг структури БД через Alembic - task-2-alembic-refactor
- **Завдання 3** – обчислення колонки is_safe_to_go_out - task-3-safety-logic
- **Завдання 4** – консольна утиліта (CLI) - task-4-cli-tool
- **Завдання 5** – міграція з PostgreSQL до MySQL - task-5-mysql-migration
