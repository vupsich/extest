from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from app.models import Booking, Category, Customer, Excursion, City, Organizer
from sqlalchemy.orm import joinedload

def get_random_excursions_by_city(db: Session, city_name: str, limit: int = 5):
    return (
        db.query(
            Excursion.excursion_id,  # Добавляем id
            Excursion.excursion_name,
            Excursion.excursion_description,
            Excursion.start_date,
            Excursion.end_date,
            Excursion.max_participants,
            Excursion.price,
            Excursion.location,
            Excursion.weather_sensitive,
            City.city_name.label("city_name"),
            Category.category_name.label("category_name"),
            Organizer.organizer_name.label("organizer_name"),
        )
        .join(City, City.city_id == Excursion.city_id)
        .join(Category, Category.category_id == Excursion.category_id)
        .join(Organizer, Organizer.organizer_id == Excursion.organizer_id)
        .filter(City.city_name == city_name)
        .order_by(func.random())
        .limit(limit)
        .all()
    )



def get_excursion_by_id(db: Session, excursion_id: int):
    return (
        db.query(Excursion)
        .options(
            joinedload(Excursion.city), 
            joinedload(Excursion.category), 
            joinedload(Excursion.organizer)
        )
        .filter(Excursion.excursion_id == excursion_id)
        .first()
    )

def get_customer_by_phone(db: Session, phone: str):
    """Получение клиента по номеру телефона"""
    return db.query(Customer).filter(Customer.customer_phone == phone).first()

def create_customer(db: Session, customer_name: str, customer_phone: str):
    """Создание нового клиента"""
    new_customer = Customer(customer_name=customer_name, customer_phone=customer_phone)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

def get_booking(db: Session, customer_id: int, excursion_id: int):
    """Получение бронирования для клиента и экскурсии"""
    return db.query(Booking).filter(
        Booking.customer_id == customer_id,
        Booking.excursion_id == excursion_id
    ).first()

def create_booking(db: Session, customer_id: int, excursion_id: int):
    """Создание нового бронирования"""
    new_booking = Booking(customer_id=customer_id, excursion_id=excursion_id)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking