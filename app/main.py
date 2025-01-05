from typing import List
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/excursions/random/", response_model=List[schemas.ExcursionDetail])
def random_excursions(city_name: str, db: Session = Depends(get_db)):
    excursions = crud.get_random_excursions_by_city(db, city_name)
    if not excursions:
        raise HTTPException(status_code=404, detail="No excursions found")
    
    response = [
        {
            "excursion_id": e.excursion_id,  # Добавляем ID
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
    # проверка, существует ли экскурсия
    excursion = crud.get_excursion_by_id(db, booking_request.excursion_id)
    if not excursion:
        raise HTTPException(status_code=404, detail="Excursion not found")
    
    # проверка, существует ли пользователь
    customer = crud.get_customer_by_phone(db, booking_request.customer_phone)
    if not customer:
        # создаем нового пользователя
        customer = crud.create_customer(
            db,
            customer_name=booking_request.customer_name,
            customer_phone=booking_request.customer_phone,
        )
    
    # проверка, есть ли уже бронирование
    existing_booking = crud.get_booking(db, customer.customer_id, booking_request.excursion_id)
    if existing_booking:
        raise HTTPException(status_code=400, detail="Booking already exists")

    # cоздаем бронирование
    booking = crud.create_booking(
        db,
        customer_id=customer.customer_id,
        excursion_id=booking_request.excursion_id,
    )
    return {"message": "Booking successfully created", "booking_id": booking.booking_id}