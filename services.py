from models import Student, Teacher
from logger import logger


class UniversityService:

    def __init__(self):
        # Здесь хранятся все пользователи
        self.users = []

        logger.info("UniversityService создан")

    # Добавление пользователя
    def add_user(self, user):
        if self.find_user_by_id(user.user_id) is not None:
            logger.warning(
                f"Пользователь не добавлен. "
                f"ID уже существует: {user.user_id}"
            )
            return False

        self.users.append(user)

        logger.info(
            f"Пользователь добавлен: "
            f"ID={user.user_id}, "
            f"name={user.first_name} {user.last_name}"
        )

        return True

    # Показать всех пользователей
    def get_all_users(self):
        logger.debug(
            f"Запрошен список всех пользователей. "
            f"Количество={len(self.users)}"
        )

        for user in self.users:
            print(user.get_info())

    # Поиск по ID
    def find_user_by_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                logger.debug(
                    f"Пользователь найден по ID={user_id}"
                )
                return user

        logger.debug(
            f"Пользователь не найден по ID={user_id}"
        )

        return None

    # Удаление пользователя
    def delete_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                self.users.remove(user)

                logger.info(
                    f"Пользователь удалён: ID={user_id}"
                )

                return True

        logger.warning(
            f"Удаление не выполнено. "
            f"Пользователь не найден: ID={user_id}"
        )

        return False

    # Обновление пользователя
    def update_user(
        self,
        user_id,
        first_name=None,
        last_name=None,
        age=None,
        email=None
    ):
        user = self.find_user_by_id(user_id)

        if user is None:
            logger.warning(
                f"Обновление не выполнено. "
                f"Пользователь не найден: ID={user_id}"
            )
            return False

        if first_name is not None:
            user.first_name = first_name

        if last_name is not None:
            user.last_name = last_name

        if age is not None:
            user.age = age

        if email is not None:
            user.email = email

        logger.info(
            f"Данные пользователя обновлены: ID={user_id}"
        )

        return True

    # Поиск по имени, фамилии или email
    def search_user(self, query):
        results = []

        query = query.lower()

        for user in self.users:
            if (
                query in user.first_name.lower()
                or query in user.last_name.lower()
                or query in user.email.lower()
            ):
                results.append(user)

        logger.info(
            f"Поиск пользователей: query='{query}', "
            f"найдено={len(results)}"
        )

        return results

    # Получить студентов
    def get_students(self):
        students = []

        for user in self.users:
            if isinstance(user, Student):
                students.append(user)

        logger.debug(
            f"Запрошен список студентов. "
            f"Количество={len(students)}"
        )

        return students

    # Получить преподавателей
    def get_teachers(self):
        teachers = []

        for user in self.users:
            if isinstance(user, Teacher):
                teachers.append(user)

        logger.debug(
            f"Запрошен список преподавателей. "
            f"Количество={len(teachers)}"
        )

        return teachers