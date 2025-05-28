import psycopg2
from psycopg2 import sql
from faker import Faker
import random
from datetime import datetime, timedelta

# Настройки подключения к БД 
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "mysecretpassword"
DB_PORT = '5433'

# Количество записей
NUM_PATIENTS = 30  # > 20
NUM_TRIALS = 7  # > 5
NUM_MEASUREMENTS = 250  # > 200

# Инициализация Faker
faker = Faker()
connection = None
cursor = None

# Подключение к БД

try:
    connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    cursor = connection.cursor()

    # Генерация пациентов
    print("Заполняем таблицу 'patients'...")
    patients = []
    for i in range(1, NUM_PATIENTS+1):
        name = faker.name()
        age = random.randint(18, 90)
        gender = random.choice(["Male", "Female"])
        condition = random.choice(["Diabetes", "Hypertension", "Asthma", "Cancer", "Arthritis"])
        cursor.execute(
            "INSERT INTO patients (patient_id, name, age, gender, condition) VALUES (%s, %s, %s, %s, %s) RETURNING patient_id",
            (i, name, age, gender, condition)
        )
        patients.append(cursor.fetchone()[0])

    # Генерация исследований
    print("Заполняем таблицу 'trials'...")
    trials = []
    for i in range(1, NUM_TRIALS + 1):
        trial_name = faker.sentence(nb_words=3)  # Генерация названия исследования
        start_date = faker.date_between(start_date="-2y", end_date="-1y")
        end_date = start_date + timedelta(days=random.randint(30, 180))
        cursor.execute(
            "INSERT INTO trials (trial_id, trial_name, start_date, end_date) VALUES (%s, %s, %s, %s) RETURNING trial_id",
            (i, trial_name, start_date, end_date)
        )
        trials.append(cursor.fetchone()[0])

    # Генерация измерений
    print("Заполняем таблицу 'measurements'...")
    measurement_id = 1

    for i in range(NUM_MEASUREMENTS):
        patient_id = random.choice(patients)
        trial_id = random.choice(trials)
        measurement_date = faker.date_between(start_date="-1y", end_date="today")

        # Определяем препараты для данного исследования (Плацебо + случайный)
        drug_options =["Плацебо", random.choice(["Аспирин", "Ибупрофен", "Парацетамол", "Метформин", "Лизиноприл"])]
        drug = random.choice(drug_options)

        condition_score = random.randint(0, 100)  # 0-100
        cursor.execute(
            "INSERT INTO measurements (measurement_id, patient_id, trial_id, measurement_date, drug, condition_score) VALUES (%s, %s, %s, %s, %s, %s)",
            (measurement_id, patient_id, trial_id, measurement_date, drug, condition_score)
        )
        measurement_id += 1

    # Сохранение изменений
    connection.commit()
    print("Данные успешно добавлены!")

except Exception as error:
    print(f"Ошибка: {error}")
    if connection:
        connection.rollback()

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
        print("Соединение с БД закрыто.")
