from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

# Мини-база данных (список словарей) с добавлением городов
excursions_db = [
    {"id": 1, "name": "Экскурсия по городу", "description": "Прогулка по историческому центру Иркутска", "price": 25.0, "city": "Иркутск"},
    {"id": 2, "name": "Экскурсия в музей", "description": "Посещение краеведческого музея в Ангарске", "price": 15.5, "city": "Ангарск"},
    {"id": 3, "name": "Экскурсия в парк", "description": "Прогулка по природному парку в Братске", "price": 20.0, "city": "Братск"},
    {"id": 4, "name": "Прогулка на Байкал", "description": "Экскурсия на озеро Байкал с гидом", "price": 50.0, "city": "Листвянка"},
    {"id": 5, "name": "Экскурсия на плотину", "description": "Посещение Братской ГЭС", "price": 30.0, "city": "Братск"},
    {"id": 6, "name": "Архитектура Иркутска", "description": "Ознакомление с деревянным зодчеством Иркутска", "price": 40.0, "city": "Иркутск"},
    {"id": 7, "name": "Тур на Тальцы", "description": "Поездка в архитектурно-этнографический музей", "price": 45.0, "city": "Иркутск"},
]

# 1. Эндпоинт для получения всех экскурсий с возможностью фильтрации по городу через параметры запроса
@app.get("/excursions/")
def get_excursions(city: str = Query(None, description="Название города для фильтрации экскурсий")):
    if city:
        city_excursions = [excursion for excursion in excursions_db if excursion["city"].lower() == city.lower()]
        if not city_excursions:
            raise HTTPException(status_code=404, detail="No excursions found in the specified city")
        return city_excursions
    return excursions_db

# 2. Эндпоинт для получения экскурсии по ID
@app.get("/excursions/{excursion_id}")
def get_excursion(excursion_id: int):
    for excursion in excursions_db:
        if excursion["id"] == excursion_id:
            return excursion
    raise HTTPException(status_code=404, detail="Excursion not found")
