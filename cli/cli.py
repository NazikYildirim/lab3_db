import argparse
import sys
from datetime import datetime, date
from app.db import SessionLocal
from app.models import Weather, AstronomyInfo

def show_help():
    print("""
Інструкція користування CLI:

python cli.py --country <назва країни> [опції]

Обов’язкові параметри:
  --country       назва країни (наприклад Ukraine)

Додаткові опції:
  --date          дата в форматі YYYY-MM-DD (за замовчуванням: сьогодні)
  --safe          показати лише якщо безпечно виходити надвір
  --wind-max      максимальна дозволена швидкість вітру, км/год

Приклади:
  python cli.py --country Ukraine
  python cli.py --country Poland --date 2025-06-10 --safe
  python cli.py --country France --wind-max 15

Якщо команда не працює як `python cli.py`, спробуйте:
  python -m cli.cli help
щоб побачити цю підказку знову.
    """)

def main():
    if len(sys.argv) == 1 or sys.argv[1] == "help":
        show_help()
        return

    parser = argparse.ArgumentParser(description="Показати погоду за країною та датою")
    parser.add_argument("--country", required=True, help="Країна")
    parser.add_argument("--date", help="Дата у форматі YYYY-MM-DD")
    parser.add_argument("--safe", action="store_true", help="Тільки якщо безпечно виходити")
    parser.add_argument("--wind-max", type=float, help="Максимальна швидкість вітру")

    args = parser.parse_args()
    session = SessionLocal()

    try:
        query_date = (
            datetime.strptime(args.date, "%Y-%m-%d").date()
            if args.date else date.today()
        )

        query = session.query(Weather).filter(
            Weather.country.ilike(args.country),
            Weather.last_updated == query_date
        )

        if args.wind_max is not None:
            query = query.filter(Weather.wind_kph <= args.wind_max)

        weather = query.first()

        if not weather:
            print("Нічого не знайдено для цієї дати.")

            available_dates = session.query(Weather.last_updated).filter(
                Weather.country.ilike(args.country)
            ).distinct().order_by(Weather.last_updated).all()

            if available_dates:
                print(f"Доступні дати для {args.country}:")
                for d in available_dates:
                    print(f"  - {d[0]}")
            else:
                print(f"Взагалі немає даних для країни {args.country}.")
            return


        astronomy = session.query(AstronomyInfo).filter_by(weather_id=weather.id).first()

        if args.safe and (astronomy.is_safe_to_go_out.value != "yes"):
            print("На жаль, виходити не рекомендовано")
            return


        print(f"Країна: {weather.country}")
        print(f"Дата: {weather.last_updated}")
        print("------------------------")
        print(f"Вітер: {weather.wind_kph} км/год")
        print(f"Напрямок: {weather.wind_direction.name if weather.wind_direction else '---'} ({weather.wind_degree}°)")
        print(f"Схід сонця: {weather.sunrise}")
        
        if not astronomy:
            print("Астрономічна інформація відсутня для цієї дати.")
        else:
            print(f"Захід сонця: {astronomy.sunset if astronomy.sunset else 'немає даних'}")
            print(f"Схід місяця: {astronomy.moonrise if astronomy.moonrise else 'немає даних'}")
            print(f"Захід місяця: {astronomy.moonset if astronomy.moonset else 'немає даних'}")
            print(f"Фаза місяця: {astronomy.moon_phase if astronomy.moon_phase else 'немає даних'}")
            print(f"Освітлення місяця: {str(astronomy.moon_illumination) + '%' if astronomy.moon_illumination is not None else 'немає даних'}")
            print(f"Чи безпечно виходити: {astronomy.is_safe_to_go_out.value if astronomy.is_safe_to_go_out else 'немає даних'}")


#        print(f"Країна: {weather.country}")
#        print(f"Дата: {weather.last_updated}")
#        print("------------------------")
#        print(f"Вітер: {weather.wind_kph} км/год")
#        print(f"Напрямок: {weather.wind_direction.name if weather.wind_direction else '---'} ({weather.wind_degree}°)")
#        print(f"Схід сонця: {weather.sunrise}")
#        
#        print(f"Захід сонця: {astronomy.sunset if astronomy.sunset else 'немає даних'}")
#        print(f"Схід місяця: {astronomy.moonrise if astronomy.moonrise else 'немає даних'}")
#        print(f"Захід місяця: {astronomy.moonset if astronomy.moonset else 'немає даних'}")
#        print(f"Фаза місяця: {astronomy.moon_phase if astronomy.moon_phase else 'немає даних'}")
#        print(f"Освітлення місяця: {str(astronomy.moon_illumination) + '%' if astronomy.moon_illumination is not None else 'немає даних'}")
#        print(f"Чи безпечно виходити: {astronomy.is_safe_to_go_out.value if astronomy.is_safe_to_go_out else 'немає даних'}")


    finally:
        session.close()

if __name__ == "__main__":
    main()
