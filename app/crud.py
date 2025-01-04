from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from app.models import Category, Excursion, City, Organizer
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
