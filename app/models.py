from sqlalchemy import Column, Integer, String, Float, Date, Time, Enum, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

# Enum для напряму вітру
class WindDirection(enum.Enum):
    N = "N"
    NNE = "NNE"
    NE = "NE"
    ENE = "ENE"
    E = "E"
    ESE = "ESE"
    SE = "SE"
    SSE = "SSE"
    S = "S"
    SSW = "SSW"
    SW = "SW"
    WSW = "WSW"
    W = "W"
    WNW = "WNW"
    NW = "NW"
    NNW = "NNW"


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

class SafetyLevel(enum.Enum):
    YES = "yes"
    NO = "no"

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

    is_safe_to_go_out = Column(Enum(SafetyLevel, name="safetylevel"))

    # зворотній зв'язок
    weather = relationship("Weather", back_populates="astronomy")