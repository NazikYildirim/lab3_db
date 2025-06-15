import csv
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Weather, AstronomyInfo, WindDirection
from app.db import SessionLocal
import os

CSV_PATH = "./data/GlobalWeatherRepository.csv"

def parse_time(value):
    try:
        return datetime.strptime(value.strip(), "%I:%M %p").time()
    except:
        return None

def parse_date(value):
    try:
        return datetime.strptime(value.strip().split(" ")[0], "%Y-%m-%d").date()
    except:
        return None

def import_data():
    session: Session = SessionLocal()
    added = 0
    skipped = 0

    with open(CSV_PATH, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                country = row.get("country")
                date = parse_date(row.get("last_updated"))

                existing = session.query(Weather).filter_by(
                    country=country,
                    last_updated=date
                ).first()

                if existing:
                    skipped += 1
                    continue

                wd = (row.get("wind_direction") or "").strip().upper()
                weather = Weather(
                    country=country,
                    wind_degree=int(row.get("wind_degree") or 0),
                    wind_kph=float(row.get("wind_kph") or 0.0),
                    wind_direction=WindDirection[wd] if wd in WindDirection.__members__ else None,
                    last_updated=date,
                    sunrise=parse_time(row.get("sunrise"))
                )

                session.add(weather)
                session.flush()

                moon_illumination = int(row.get("moon_illumination") or 0)

                # логіка безпеки: якщо вітер сильний або затемнено — не варто виходити
                # is_safe = not (
                #     weather.wind_kph > 20 or moon_illumination < 10
                # )

                moon_illum = int(row.get("moon_illumination") or 0)
                wind_speed = float(row.get("wind_kph") or 0.0)

                is_safe = "no" if wind_speed > 20 or moon_illum < 10 else "yes"

                astronomy = AstronomyInfo(
                    weather_id=weather.id,
                    sunset=parse_time(row.get("sunset")),
                    moonrise=parse_time(row.get("moonrise")),
                    moonset=parse_time(row.get("moonset")),
                    moon_phase=row.get("moon_phase"),
                    moon_illumination=moon_illum,
                    is_safe_to_go_out=is_safe
                )

                session.add(astronomy)
                added += 1

            except Exception as e:
                print(f"Error in row: {country} → {e}")

        session.commit()
        session.close()
        print("Data imported successfully!")
        print(f"Added: {added}")
        print(f"Skipped duplicates: {skipped}")

if __name__ == "__main__":
    import_data()
