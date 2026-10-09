# UniversityCLI

UniversityCLI — консольная система управления пользователями университета.

Проект позволяет работать со студентами и преподавателями, хранить данные, искать пользователей, изменять информацию и формировать простую статистику.

Проект создан на Python с использованием ООП и модульной архитектуры.

---

## Основные возможности

### Пользователи

Система поддерживает два типа пользователей:

- Student
- Teacher

Оба наследуются от базового класса `User`.

---

## Student

Студент содержит:

- ID
- имя
- фамилию
- возраст
- email
- факультет
- курс обучения
- средний балл

Возможности:

- добавить студента
- посмотреть всех студентов
- найти студента по ID
- найти студента по имени
- изменить данные студента
- удалить студента
- посмотреть информацию о студенте

---

## Teacher

Преподаватель содержит:

- ID
- имя
- фамилию
- возраст
- email
- кафедру
- предмет
- стаж работы

Возможности:

- добавить преподавателя
- посмотреть список преподавателей
- найти преподавателя
- изменить данные
- удалить преподавателя

---

# ООП

## Наследование

Базовый класс:

User

От него наследуются:

User
├── Student
└── Teacher

Общие данные находятся в `User`.

Например:

- id
- first_name
- last_name
- age
- email

А специфические данные находятся в дочерних классах.

---

## Инкапсуляция

Некоторые данные должны быть защищены.

Например:

_age

Изменение возраста должно происходить через:

@property

и

@age.setter

Нельзя установить:

- отрицательный возраст
- слишком большой возраст
- некорректное значение

---

## Полиморфизм

Классы Student и Teacher должны иметь одинаковый метод:

get_info()

Но каждый класс реализует его по-своему.

Например:

Student.get_info()

возвращает данные студента.

Teacher.get_info()

возвращает данные преподавателя.

---

## Абстракция

Класс User сделать абстрактным.

Использовать:

from abc import ABC, abstractmethod

Метод:

get_info()

должен быть абстрактным.

Student и Teacher обязаны его реализовать.

---

# Структура проекта

UniversityCLI/

    main.py
    models.py
    services.py
    utils.py
    data/
        users.json
    logs/
        app.log
    README.md

---

# models.py

Содержит классы:

- User
- Student
- Teacher

Здесь находится только структура объектов и их методы.

Например:

User
Student
Teacher

---

# services.py

Содержит бизнес-логику приложения.

Например:

- add_student()
- add_teacher()
- get_all_students()
- get_all_teachers()
- find_user_by_id()
- search_user()
- update_user()
- delete_user()

Также здесь будет класс:

UniversityService

который управляет пользователями системы.

---

# utils.py

Содержит вспомогательные функции.

Например:

- validate_email()
- validate_age()
- generate_id()
- load_data()
- save_data()

Также здесь будет обработка ошибок пользовательского ввода.

---

# main.py

Точка входа в программу.

Здесь находится CLI-интерфейс.

Пример:

=========================
     UNIVERSITY CLI
=========================

1. Students
2. Teachers
3. Search
4. Statistics
0. Exit

Выберите действие:

---

# Меню студентов

1. Add student
2. Show students
3. Find student
4. Update student
5. Delete student
0. Back

---

# Меню преподавателей

1. Add teacher
2. Show teachers
3. Find teacher
4. Update teacher
5. Delete teacher
0. Back

---

# Поиск

Пользователь должен иметь возможность искать:

- по ID
- по имени
- по фамилии
- по email

---

# Сортировка

Добавить возможность сортировать студентов:

- по имени
- по возрасту
- по курсу
- по среднему баллу

Например:

Students sorted by GPA

1. Ali Karimov — 4.9
2. Ahmad Saidov — 4.7
3. John Smith — 4.1

---

# Статистика

Добавить отдельный раздел:

Statistics

Он должен показывать:

- количество студентов
- количество преподавателей
- общее количество пользователей
- средний возраст студентов
- средний GPA студентов
- студент с самым высоким GPA

Пример:

University Statistics

Students: 24
Teachers: 7
Total users: 31

Average student age: 20.4
Average GPA: 4.2

Top student:
Ali Karimov — GPA 4.9

---

# Хранение данных

Данные не должны исчезать после завершения программы.

Использовать:

JSON

Файл:

data/users.json

При запуске программы данные загружаются.

При изменении данных они сохраняются обратно.

---

# Пример JSON

[
    {
        "id": 1,
        "type": "student",
        "first_name": "Ali",
        "last_name": "Karimov",
        "age": 19,
        "email": "ali@example.com",
        "faculty": "Computer Science",
        "course": 2,
        "gpa": 4.5
    }
]

---

# Проверка данных

Программа должна проверять ввод.

Нельзя добавить:

- пустое имя
- отрицательный возраст
- неправильный email
- курс меньше 1
- GPA меньше 0
- GPA больше 5

При неправильном вводе программа не должна падать.

Пользователь должен получить понятное сообщение.

Например:

Invalid age. Please enter a number between 16 and 100.

---

# Исключения

Использовать:

try
except

Программа должна корректно обрабатывать:

- неправильный ввод
- отсутствие файла
- поврежденный JSON
- попытку найти несуществующего пользователя
- неверный ID

---

# Logging

Добавить логирование.

Использовать стандартный модуль:

logging

Файл:

logs/app.log

Пример:

INFO - Student created: ID 12
INFO - Teacher deleted: ID 5
WARNING - User not found: ID 44
ERROR - Failed to load users.json

Это сделает проект ближе к реальному приложению.

---

# ID

Каждый пользователь должен иметь уникальный ID.

Например:

Student:
ID: 1

Teacher:
ID: 2

Student:
ID: 3

ID не должны повторяться.

---

# __str__

Для Student и Teacher реализовать:

__str__()

Чтобы можно было сделать:

print(student)

и получить нормальный результат.

Например:

[Student #15] Ali Karimov | Computer Science | Course 2 | GPA: 4.5

---

# Требования к коду

Проект должен:

- использовать ООП
- использовать наследование
- использовать инкапсуляцию
- использовать полиморфизм
- использовать абстракцию
- использовать @property
- использовать исключения
- работать с JSON
- использовать функции
- использовать модули
- использовать logging
- иметь понятные имена переменных
- не хранить всю программу в main.py

---

# Дополнительные функции

После основной версии можно добавить:

## Export

Экспорт студентов в:

students.txt

или:

students.csv

---

## Top students

Показать TOP-5 студентов по GPA.

---

## Filtering

Например:

Показать только студентов:

Faculty = Computer Science

или:

Course = 2

---

# Версия 2.0

После изучения SQL заменить JSON на:

PostgreSQL

Добавить:

- SQL
- PostgreSQL
- SQLAlchemy

Архитектура проекта при этом останется похожей.

---

# Версия 3.0

В будущем проект можно превратить в Backend API.

Использовать:

FastAPI

Пример endpoints:

GET /students
GET /students/{id}
POST /students
PUT /students/{id}
DELETE /students/{id}

То есть этот проект можно постепенно развивать:

CLI
↓
PostgreSQL
↓
FastAPI
↓
полноценный backend-проект

---

# Что демонстрирует проект

UniversityCLI демонстрирует знания:

- Python
- Object-Oriented Programming
- Inheritance
- Encapsulation
- Polymorphism
- Abstraction
- File handling
- JSON
- Exception handling
- Logging
- Modular architecture
- CRUD operations
- Input validation

---

# План разработки

## Stage 1 — Project structure

Создать:

main.py
models.py
services.py
utils.py
README.md

Создать папки:

data/
logs/

---

## Stage 2 — Models

Создать:

User
Student
Teacher

Реализовать:

inheritance
abstractmethod
property
__str__

---

## Stage 3 — UniversityService

Реализовать:

add
show
find

для Student и Teacher.

---

## Stage 4 — CRUD

Добавить:

Create
Read
Update
Delete

---

## Stage 5 — JSON

Добавить:

load_data()
save_data()

---

## Stage 6 — Validation

Проверять:

age
email
GPA
course
empty fields

---

## Stage 7 — Search and sorting

Добавить:

search
filter
sorting

---

## Stage 8 — Statistics

Добавить статистику университета.

---

## Stage 9 — Logging

Добавить логирование действий.

---

## Stage 10 — Refactoring

Проверить архитектуру.

Убрать повторяющийся код.

Привести проект в чистый вид.

---

## Stage 11 — GitHub

Добавить:

README.md
.gitignore
requirements.txt (если понадобятся зависимости)

Сделать понятные Git commits.

Например:

Initial project structure

Add User, Student and Teacher models

Implement student CRUD

Add JSON persistence

Add validation

Add logging

Add statistics

Refactor project structure