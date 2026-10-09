from models import Student, Teacher
from services import UniversityService
from utils import (
    input_float,
    input_int,
    save_users,
    load_users
)
from logger import logger


# Создаём сервис и загружаем старые данные
service = UniversityService()
service.users = load_users()

logger.info("CLI приложение запущено")


while True:
    print("\n=== UNIVERSITY CLI ===")
    print("1. Add student")
    print("2. Add teacher")
    print("3. Show all users")
    print("4. Find user by ID")
    print("5. Update user")
    print("6. Delete user")
    print("7. Search user")
    print("0. Exit")

    choice = input("Choose an option: ")

    if choice == "0":
        logger.info("CLI приложение закрыто")

        print("Goodbye!")
        break

    elif choice == "1":
        user_id = input_int("ID: ")

        if user_id is None:
            continue

        first_name = input("First name: ")
        last_name = input("Last name: ")

        age = input_int("Age: ")

        if age is None:
            continue

        email = input("Email: ")
        faculty = input("Faculty: ")

        course = input_int("Course: ")

        if course is None:
            continue

        gpa = input_float("GPA: ")

        if gpa is None:
            continue

        try:
            student = Student(
                user_id,
                first_name,
                last_name,
                age,
                email,
                faculty,
                course,
                gpa
            )

            if service.add_user(student):
                save_users(service.users)

                print("Студент успешно добавлен!")
            else:
                print(
                    "Пользователь с таким ID уже существует!"
                )

        except ValueError as error:
            logger.warning(
                f"Ошибка создания студента: {error}"
            )
            print(error)

    elif choice == "2":
        user_id = input_int("ID: ")

        if user_id is None:
            continue

        first_name = input("First name: ")
        last_name = input("Last name: ")

        age = input_int("Age: ")

        if age is None:
            continue

        email = input("Email: ")
        department = input("Department: ")
        subject = input("Subject: ")

        experience = input_int("Experience: ")

        if experience is None:
            continue

        try:
            teacher = Teacher(
                user_id,
                first_name,
                last_name,
                age,
                email,
                department,
                subject,
                experience
            )

            if service.add_user(teacher):
                save_users(service.users)

                print(
                    "Преподаватель успешно добавлен!"
                )
            else:
                print(
                    "Пользователь с таким ID уже существует!"
                )

        except ValueError as error:
            logger.warning(
                f"Ошибка создания преподавателя: {error}"
            )
            print(error)

    elif choice == "3":
        service.get_all_users()

    elif choice == "4":
        user_id = input_int("ID: ")

        if user_id is None:
            continue

        user = service.find_user_by_id(user_id)

        if user is not None:
            print(user.get_info())
        else:
            print("Пользователь не найден!")

    elif choice == "5":
        user_id = input_int("ID: ")

        if user_id is None:
            continue

        user = service.find_user_by_id(user_id)

        if user is None:
            print("Пользователь не найден!")
            continue

        first_name_input = input(
            "First name (Enter = skip): "
        )

        first_name = (
            first_name_input
            if first_name_input
            else None
        )

        last_name_input = input(
            "Last name (Enter = skip): "
        )

        last_name = (
            last_name_input
            if last_name_input
            else None
        )

        age_input = input(
            "Age (Enter = skip): "
        )

        if age_input:
            try:
                age = int(age_input)

            except ValueError:
                print("Введите возраст числом")
                continue
        else:
            age = None

        email_input = input(
            "Email (Enter = skip): "
        )

        email = (
            email_input
            if email_input
            else None
        )

        try:
            updated = service.update_user(
                user_id,
                first_name,
                last_name,
                age,
                email
            )

            if updated:
                save_users(service.users)

                print(
                    "Данные пользователя обновлены!"
                )

        except ValueError as error:
            logger.warning(
                f"Ошибка обновления пользователя: {error}"
            )
            print(error)

    elif choice == "6":
        user_id = input_int("ID: ")

        if user_id is None:
            continue

        if service.delete_user(user_id):
            save_users(service.users)

            print("Пользователь удалён!")
        else:
            print("Пользователь не найден!")

    elif choice == "7":
        search_input = input("Search: ")

        result = service.search_user(
            search_input
        )

        if result:
            for user in result:
                print(user.get_info())
        else:
            print("Ничего не найдено!")

    else:
        logger.warning(
            f"Выбран неизвестный пункт меню: {choice}"
        )

        print("Такого пункта меню нет!")