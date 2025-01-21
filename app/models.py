from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime, DECIMAL, func
from sqlalchemy.orm import relationship
from app.database import Base

class City(Base):
    __tablename__ = "city"
    city_id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String, nullable=False)
    region = Column(String, nullable=False)
    country = Column(String, nullable=False)

class Category(Base):
    __tablename__ = "category"
    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, unique=True, nullable=False)

class Organizer(Base):
    __tablename__ = "organizer"
    organizer_id = Column(Integer, primary_key=True, index=True)
    organizer_name = Column(String, nullable=False)
    organizer_email = Column(String)
    organizer_phone = Column(String)
    organizer_description = Column(Text)

class Excursion(Base):
    __tablename__ = "excursion"
    excursion_id = Column(Integer, primary_key=True, index=True)
    excursion_name = Column(String, nullable=False)
    excursion_description = Column(Text)
    category_id = Column(Integer, ForeignKey("category.category_id"), nullable=False)
    organizer_id = Column(Integer, ForeignKey("organizer.organizer_id"), nullable=False)
    city_id = Column(Integer, ForeignKey("city.city_id"), nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    max_participants = Column(Integer)
    price = Column(DECIMAL(10, 2))
    location = Column(String)
    weather_sensitive = Column(Boolean, default=False)

    city = relationship("City")
    category = relationship("Category")
    organizer = relationship("Organizer")
    bookings = relationship("Booking", back_populates="excursion")


class Customer(Base):
    __tablename__ = "customer"
    customer_id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, unique=True, nullable=False)

    # Связи
    bookings = relationship("Booking", back_populates="customer")

class Booking(Base):
    __tablename__ = "booking"
    booking_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"), nullable=False)
    excursion_id = Column(Integer, ForeignKey("excursion.excursion_id"), nullable=False)
    booking_date = Column(DateTime, server_default=func.now())  
    booking_status = Column(String, default="pending")

    # Связи
    customer = relationship("Customer", back_populates="bookings")
    excursion = relationship("Excursion", back_populates="bookings")