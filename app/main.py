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
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
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

                weather = Weather(
                    country=country,
                    wind_degree=int(row.get("wind_degree") or 0),
                    wind_kph=float(row.get("wind_kph") or 0.0),
                    wind_direction=WindDirection[row.get("wind_dir")] if row.get("wind_dir") in WindDirection.__members__ else None,
                    last_updated=date,
                    sunrise=parse_time(row.get("sunrise"))
                )

                session.add(weather)
                session.flush()

                astronomy = AstronomyInfo(
                    weather_id=weather.id,
                    sunset=parse_time(row.get("sunset")),
                    moonrise=parse_time(row.get("moonrise")),
                    moonset=parse_time(row.get("moonset")),
                    moon_phase=row.get("moon_phase"),
                    moon_illumination=int(row.get("moon_illumination") or 0)
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
