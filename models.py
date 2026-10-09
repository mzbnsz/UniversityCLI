from abc import ABC, abstractmethod

from logger import logger


class User(ABC):

    def __init__(self, user_id, first_name, last_name, age, email):
        # Проверяем имя
        if not first_name.strip():
            logger.warning(
                f"Попытка создать пользователя с пустым именем. ID={user_id}"
            )
            raise ValueError("Имя не может быть пустым")

        # Проверяем фамилию
        if not last_name.strip():
            logger.warning(
                f"Попытка создать пользователя с пустой фамилией. ID={user_id}"
            )
            raise ValueError("Фамилия не может быть пустой")

        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email

    # Проверка возраста
    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if value < 16 or value > 100:
            logger.warning(
                f"Некорректный возраст: {value}"
            )
            raise ValueError("Возраст должен быть от 16 до 100")

        self.__age = value

    # Проверка email
    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if "@" not in value or "." not in value:
            logger.warning(
                f"Некорректный email: {value}"
            )
            raise ValueError("Некорректный email")

        self.__email = value

    # Дочерние классы обязаны реализовать get_info()
    @abstractmethod
    def get_info(self):
        pass


class Student(User):

    def __init__(
        self,
        user_id,
        first_name,
        last_name,
        age,
        email,
        faculty,
        course,
        gpa
    ):
        # Общие данные передаём в User
        super().__init__(
            user_id,
            first_name,
            last_name,
            age,
            email
        )

        self.faculty = faculty
        self.course = course
        self.gpa = gpa

    # Проверка GPA
    @property
    def gpa(self):
        return self.__gpa

    @gpa.setter
    def gpa(self, value):
        if value < 0 or value > 5:
            logger.warning(
                f"Некорректный GPA: {value}"
            )
            raise ValueError("GPA должен быть от 0 до 5")

        self.__gpa = value

    # Проверка курса
    @property
    def course(self):
        return self.__course

    @course.setter
    def course(self, value):
        if value < 1 or value > 5:
            logger.warning(
                f"Некорректный курс: {value}"
            )
            raise ValueError("Курс должен быть от 1 до 5")

        self.__course = value

    # Информация о студенте
    def get_info(self):
        return (
            f"ID: {self.user_id}, "
            f"Name: {self.first_name}, "
            f"Last name: {self.last_name}, "
            f"Age: {self.age}, "
            f"Email: {self.email}, "
            f"Faculty: {self.faculty}, "
            f"Course: {self.course}, "
            f"GPA: {self.gpa}"
        )

    # Превращаем объект в словарь для JSON
    def to_dict(self):
        return {
            "type": "student",
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "faculty": self.faculty,
            "course": self.course,
            "gpa": self.gpa
        }


class Teacher(User):

    def __init__(
        self,
        user_id,
        first_name,
        last_name,
        age,
        email,
        department,
        subject,
        experience
    ):
        # Общие данные передаём в User
        super().__init__(
            user_id,
            first_name,
            last_name,
            age,
            email
        )

        self.department = department
        self.subject = subject
        self.experience = experience

    # Проверка стажа
    @property
    def experience(self):
        return self.__experience

    @experience.setter
    def experience(self, value):
        if value < 0:
            logger.warning(
                f"Некорректный стаж: {value}"
            )
            raise ValueError("Стаж не может быть отрицательным")

        self.__experience = value

    # Информация о преподавателе
    def get_info(self):
        return (
            f"ID: {self.user_id}, "
            f"Name: {self.first_name}, "
            f"Last name: {self.last_name}, "
            f"Age: {self.age}, "
            f"Email: {self.email}, "
            f"Department: {self.department}, "
            f"Subject: {self.subject}, "
            f"Experience: {self.experience}"
        )

    # Превращаем объект в словарь для JSON
    def to_dict(self):
        return {
            "type": "teacher",
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "department": self.department,
            "subject": self.subject,
            "experience": self.experience
        }