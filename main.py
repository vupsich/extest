from fastapi import FastAPI, HTTPException

app = FastAPI()

# Мини-база данных (список словарей)
excursions_db = [
    {"id": 1, "name": "Экскурсия по городу", "description": "Прогулка по историческому центру города", "price": 25.0},
    {"id": 2, "name": "Экскурсия в музей", "description": "Посещение местного музея", "price": 15.5},
    {"id": 3, "name": "Экскурсия в парк", "description": "Прогулка по национальному парку", "price": 20.0},
]

# 1. Эндпоинт для получения всех экскурсий
@app.get("/excursions/")
def get_excursions():
    return excursions_db

# 2. Эндпоинт для получения экскурсии по ID
@app.get("/excursions/{excursion_id}")
def get_excursion(excursion_id: int):
    # Ищем экскурсию по ID в базе данных
    for excursion in excursions_db:
        if excursion["id"] == excursion_id:
            return excursion
    # Если экскурсия не найдена, выбрасываем ошибку 404
    raise HTTPException(status_code=404, detail="Excursion not found")