import json

from models import Student, Teacher
from logger import logger


# Сохраняем пользователей в JSON
def save_users(service_users):
    data = []

    for user in service_users:
        data.append(user.to_dict())

    try:
        with open(
            "data/users.json",
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

        logger.info(
            f"Данные сохранены в users.json. "
            f"Количество пользователей={len(service_users)}"
        )

    except OSError as error:
        logger.error(
            f"Ошибка сохранения users.json: {error}"
        )
        raise


# Загружаем пользователей из JSON
def load_users():
    try:
        with open(
            "data/users.json",
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

    except FileNotFoundError:
        logger.warning(
            "Файл users.json не найден. "
            "Будет создан новый список пользователей"
        )
        return []

    except json.JSONDecodeError:
        logger.error(
            "Файл users.json повреждён или содержит неправильный JSON"
        )
        return []

    users = []

    for item in data:
        try:
            if item["type"] == "student":
                user = Student(
                    item["user_id"],
                    item["first_name"],
                    item["last_name"],
                    item["age"],
                    item["email"],
                    item["faculty"],
                    item["course"],
                    item["gpa"]
                )

            elif item["type"] == "teacher":
                user = Teacher(
                    item["user_id"],
                    item["first_name"],
                    item["last_name"],
                    item["age"],
                    item["email"],
                    item["department"],
                    item["subject"],
                    item["experience"]
                )

            else:
                logger.warning(
                    f"Неизвестный тип пользователя: "
                    f"{item.get('type')}"
                )
                continue

            users.append(user)

        except (KeyError, ValueError, TypeError) as error:
            logger.error(
                f"Не удалось загрузить пользователя из JSON: {error}"
            )

    logger.info(
        f"Пользователи загружены из JSON. "
        f"Количество={len(users)}"
    )

    return users


# Безопасный ввод целого числа
def input_int(prompt):
    try:
        return int(input(prompt))

    except ValueError:
        logger.warning(
            f"Некорректный ввод int для поля: {prompt}"
        )

        print("Введите значение числом")
        return None


# Безопасный ввод числа с точкой
def input_float(prompt):
    try:
        return float(input(prompt))

    except ValueError:
        logger.warning(
            f"Некорректный ввод float для поля: {prompt}"
        )

        print("Введите корректное число")
        return None