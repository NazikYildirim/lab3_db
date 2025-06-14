from sqlalchemy import Column, Integer, String, Float, Date, Time, Enum, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

# Enum для напряму вітру
class WindDirection(enum.Enum):
    N = "N"
    S = "S"
    E = "E"
    W = "W"
    NE = "NE"
    NW = "NW"
    SE = "SE"
    SW = "SW"

# Основна таблиця
class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True)
    country = Column(String)
    wind_degree = Column(Integer)
    wind_kph = Column(Float)
    wind_direction = Column(Enum(WindDirection))
    last_updated = Column(Date)
    sunrise = Column(Time)

    # Зв'язок з AstronomyInfo
    astronomy = relationship("AstronomyInfo", back_populates="weather", uselist=False)

# Таблиця з даними про небесні тіла
class AstronomyInfo(Base):
    __tablename__ = "astronomy_info"

    id = Column(Integer, primary_key=True)
    weather_id = Column(Integer, ForeignKey("weather.id"))
    sunset = Column(Time)
    moonrise = Column(Time)
    moonset = Column(Time)
    moon_phase = Column(String)
    moon_illumination = Column(Integer)

    # зворотній зв'язок
    weather = relationship("Weather", back_populates="astronomy")