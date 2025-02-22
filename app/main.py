from typing import List
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import crud, models, schemas
from app.database import engine, Base, get_db
from experta import MATCH, KnowledgeEngine, Rule, Fact
import random

Base.metadata.create_all(bind=engine)

app = FastAPI()

class FilterRequest(BaseModel):
    city: str | None = None
    price: float | None = None
    max_participants: int | None = None
    category: str | None = None  

class ExcursionSelector(KnowledgeEngine):
    def __init__(self, excursions):
        super().__init__()
        self.filtered_excursions = excursions

    @Rule(Fact(city=MATCH.city))
    def filter_by_city(self, city):
        self.filtered_excursions = [
            e for e in self.filtered_excursions if e.city_name.lower() == city.lower()
        ]

    @Rule(Fact(price=MATCH.price))
    def filter_by_price(self, price):
        self.filtered_excursions = [
            e for e in self.filtered_excursions if e.price <= price
        ]

    @Rule(Fact(max_participants=MATCH.max_participants))
    def filter_by_max_participants(self, max_participants):
        self.filtered_excursions = [
            e for e in self.filtered_excursions if e.max_participants <= max_participants
        ]

    @Rule(Fact(category=MATCH.category))
    def filter_by_category(self, category):
        self.filtered_excursions = [
            e for e in self.filtered_excursions if e.category_name.lower() == category.lower()
        ]

    def get_results(self):
        return self.filtered_excursions



@app.get("/excursions/random/", response_model=List[schemas.ExcursionDetail])
def random_excursions(city_name: str, db: Session = Depends(get_db)):
    excursions = crud.get_random_excursions_by_city(db, city_name)
    if not excursions:
        raise HTTPException(status_code=404, detail="No excursions found")

    response = [
        {
            "excursion_id": e.excursion_id,  
            "excursion_name": e.excursion_name,
            "excursion_description": e.excursion_description,
            "start_date": e.start_date.isoformat() if e.start_date else None,
            "end_date": e.end_date.isoformat() if e.end_date else None,
            "max_participants": e.max_participants,
            "price": float(e.price) if e.price else None,
            "location": e.location,
            "weather_sensitive": e.weather_sensitive,
            "city_name": e.city_name,
            "category_name": e.category_name,
            "organizer_name": e.organizer_name,
        }
        for e in excursions
    ]
    return response

@app.get("/excursion/{excursion_id}", response_model=schemas.ExcursionDetail)
def excursion_detail(excursion_id: int, db: Session = Depends(get_db)):
    excursion = crud.get_excursion_by_id(db, excursion_id)
    if not excursion:
        raise HTTPException(status_code=404, detail="Excursion not found")
    return {
        "excursion_id": excursion.excursion_id,
        "excursion_name": excursion.excursion_name,
        "excursion_description": excursion.excursion_description,
        "start_date": excursion.start_date.isoformat() if excursion.start_date else None,
        "end_date": excursion.end_date.isoformat() if excursion.end_date else None,
        "max_participants": excursion.max_participants,
        "price": float(excursion.price) if excursion.price else None,
        "location": excursion.location,
        "weather_sensitive": excursion.weather_sensitive,
        "city_name": excursion.city.city_name if excursion.city else None,
        "category_name": excursion.category.category_name if excursion.category else None,
        "organizer_name": excursion.organizer.organizer_name if excursion.organizer else None,
    }

@app.post("/booking/")
def create_booking(booking_request: schemas.BookingRequest, db: Session = Depends(get_db)):
    excursion = crud.get_excursion_by_id(db, booking_request.excursion_id)
    if not excursion:
        raise HTTPException(status_code=404, detail="Excursion not found")

    customer = crud.get_customer_by_phone(db, booking_request.customer_phone)
    if not customer:
        customer = crud.create_customer(
            db,
            customer_name=booking_request.customer_name,
            customer_phone=booking_request.customer_phone,
        )

    existing_booking = crud.get_booking(db, customer.customer_id, booking_request.excursion_id)
    if existing_booking:
        raise HTTPException(status_code=400, detail="Booking already exists")

    booking = crud.create_booking(
        db,
        customer_id=customer.customer_id,
        excursion_id=booking_request.excursion_id,
    )
    return {"message": "Booking successfully created", "booking_id": booking.booking_id}


@app.post("/filter_excursions/")
def filter_excursions(filters: FilterRequest, db: Session = Depends(get_db)):
    excursions = crud.get_all_excursions(db)

    engine = ExcursionSelector(excursions)
    engine.reset()

    if filters.city:
        engine.declare(Fact(city=filters.city))
    if filters.price:
        engine.declare(Fact(price=filters.price))
    if filters.max_participants:
        engine.declare(Fact(max_participants=filters.max_participants))
    if filters.category:
        engine.declare(Fact(category=filters.category))  

    engine.run()

    filtered_excursions = engine.get_results()

    if not filtered_excursions:
        raise HTTPException(status_code=404, detail="No excursions found")

    random_excursion = random.choice(filtered_excursions)
    return {
        "excursion_id": random_excursion.excursion_id,
        "excursion_name": random_excursion.excursion_name,
        "excursion_description": random_excursion.excursion_description,
        "start_date": random_excursion.start_date.isoformat() if random_excursion.start_date else None,
        "end_date": random_excursion.end_date.isoformat() if random_excursion.end_date else None,
        "max_participants": random_excursion.max_participants,
        "price": float(random_excursion.price) if random_excursion.price else None,
        "location": random_excursion.location,
        "weather_sensitive": random_excursion.weather_sensitive,
        "city_name": random_excursion.city_name,
        "category_name": random_excursion.category_name,
        "organizer_name": random_excursion.organizer_name,
    }


@app.get("/bookings/{customer_phone}", response_model=List[schemas.ExcursionDetail])
def get_customer_bookings(customer_phone: str, db: Session = Depends(get_db)):
    customer = crud.get_customer_by_phone(db, customer_phone)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    bookings = crud.get_bookings_by_phone(db, customer_phone)
    if not bookings:
        return []  

    return [
        schemas.ExcursionDetail(
            excursion_id=booking.excursion.excursion_id,
            excursion_name=booking.excursion.excursion_name,
            excursion_description=booking.excursion.excursion_description,
            start_date=booking.excursion.start_date.isoformat(),
            end_date=booking.excursion.end_date.isoformat(),
            max_participants=booking.excursion.max_participants,
            price=float(booking.excursion.price),
            location=booking.excursion.location,
            weather_sensitive=booking.excursion.weather_sensitive,
            city_name=booking.excursion.city.city_name,
            category_name=booking.excursion.category.category_name,
            organizer_name=booking.excursion.organizer.organizer_name,
        )
        for booking in bookings
    ]
