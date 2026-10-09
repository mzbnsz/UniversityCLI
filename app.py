from flask import Flask, render_template, request, redirect, url_for
# Flask - создаёт веб-приложение
# render_template - открывает HTML
# request - получает данные, которые отправил браузер
# redirect - перенаправляет пользователя на другую страницу
# url_for - строит адрес страницы по имени функции

from models import Student, Teacher
# импортируем класс Student, чтобы создавать новых студентов

from services import UniversityService
# наша бизнес-логика

from utils import load_users, save_users
# load_users - загрузить JSON
# save_users - сохранить JSON


app = Flask(__name__)
# создаём Flask-приложение


service = UniversityService()
# создаём сервис

service.users = load_users()
# загружаем всех пользователей из JSON


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/students")
def students():

    query = request.args.get("q", "").strip()
    # request.args получает данные из URL
    # например: /students?q=Ali
    # тогда query будет равен "Ali"

    if query:
        # если пользователь что-то ввёл

        results = service.search_user(query)
        # ищем пользователей через наш services.py

        students_list = [
            user for user in results
            if isinstance(user, Student)
        ]
        # search_user может найти и Teacher
        # поэтому оставляем только объекты Student

    else:
        # если поиск пустой

        students_list = service.get_students()
        # показываем всех студентов


    return render_template(
        "students.html",
        students=students_list,
        query=query
    )
    # students -> список для таблицы
    # query -> то, что пользователь написал в Search

@app.route("/students/add", methods=["GET", "POST"])
# этот адрес умеет работать сразу с двумя HTTP-методами:
# GET  - показать форму
# POST - принять данные формы

def add_student():

    if request.method == "POST":
        # если браузер отправил форму

        try:

            user_id = int(request.form["user_id"])
            # получаем ID из формы и превращаем строку в int

            first_name = request.form["first_name"]
            # получаем имя

            last_name = request.form["last_name"]
            # получаем фамилию

            age = int(request.form["age"])
            # возраст превращаем в int

            email = request.form["email"]

            faculty = request.form["faculty"]

            course = int(request.form["course"])

            gpa = float(request.form["gpa"])
            # GPA превращаем в float


            new_student = Student(
                user_id,
                first_name,
                last_name,
                age,
                email,
                faculty,
                course,
                gpa
            )
            # создаём настоящий объект Student


            if not service.add_user(new_student):
                # если ID уже существует

                return "User with this ID already exists"


            save_users(service.users)
            # сохраняем обновлённый список в JSON


            return redirect(url_for("students"))
            # после сохранения отправляем пользователя назад на /students


        except ValueError as error:

            return f"Error: {error}"
            # если age/course/gpa неправильные или модель выбросила ValueError


    return render_template("add_student.html")
    # если это обычный GET-запрос, просто показываем форму


@app.route("/teachers")
def teachers():

    query = request.args.get("q", "").strip()
    # получаем поисковый запрос из URL


    if query:

        results = service.search_user(query)
        # ищем среди всех пользователей

        teachers_list = [
            user for user in results
            if isinstance(user, Teacher)
        ]
        # оставляем только Teacher

    else:

        teachers_list = service.get_teachers()
        # если поиска нет, показываем всех


    return render_template(
        "teachers.html",
        teachers=teachers_list,
        query=query
    )

@app.route("/statistics")
def statistics():

    students_list = service.get_students()
    teachers_list = service.get_teachers()

    total_students = len(students_list)
    total_teachers = len(teachers_list)
    total_users = len(service.users)


    if students_list:

        average_gpa = (
            sum(student.gpa for student in students_list)
            / len(students_list)
        )

        top_student = max(
            students_list,
            key=lambda student: student.gpa
        )

    else:

        average_gpa = 0
        top_student = None


    return render_template(
        "statistics.html",
        total_users=total_users,
        total_students=total_students,
        total_teachers=total_teachers,
        average_gpa=average_gpa,
        top_student=top_student
    )

@app.route("/teachers/add", methods=["GET", "POST"])
# GET  -> показать форму
# POST -> принять данные формы

def add_teacher():

    if request.method == "POST":
        # если пользователь нажал Save Teacher

        try:

            user_id = int(request.form["user_id"])
            # получаем ID

            first_name = request.form["first_name"]
            # имя

            last_name = request.form["last_name"]
            # фамилия

            age = int(request.form["age"])
            # возраст

            email = request.form["email"]
            # email

            department = request.form["department"]
            # кафедра

            subject = request.form["subject"]
            # предмет

            experience = int(request.form["experience"])
            # стаж


            new_teacher = Teacher(
                user_id,
                first_name,
                last_name,
                age,
                email,
                department,
                subject,
                experience
            )
            # создаём настоящий объект Teacher


            if not service.add_user(new_teacher):
                # если такой ID уже существует

                return "User with this ID already exists"


            save_users(service.users)
            # сохраняем изменения в users.json


            return redirect(url_for("teachers"))
            # после добавления возвращаемся к таблице Teachers


        except ValueError as error:

            return f"Error: {error}"
            # если пользователь ввёл некорректные данные


    return render_template("add_teacher.html")
    # если это GET — просто показываем HTML-форму

@app.route("/students/delete/<int:user_id>", methods=["POST"])
# <int:user_id> означает:
# взять число из адреса и передать его в функцию как user_id

def delete_student(user_id):

    service.delete_user(user_id)
    # удаляем пользователя через уже готовый сервис

    save_users(service.users)
    # сохраняем обновлённый список в JSON

    return redirect(url_for("students"))
    # возвращаемся на страницу студентов

@app.route("/teachers/delete/<int:user_id>", methods=["POST"])

def delete_teacher(user_id):

    service.delete_user(user_id)

    save_users(service.users)

    return redirect(url_for("teachers"))

@app.route("/students/edit/<int:user_id>", methods=["GET", "POST"])
# GET  -> открыть форму уже с текущими данными
# POST -> сохранить изменённые данные

def edit_student(user_id):

    student = service.find_user_by_id(user_id)
    # ищем пользователя по ID

    if student is None:
        return "Student not found"
        # если такого ID нет


    if request.method == "POST":
        # если пользователь нажал Save

        try:

            first_name = request.form["first_name"]
            # новое имя

            last_name = request.form["last_name"]
            # новая фамилия

            age = int(request.form["age"])
            # новый возраст

            email = request.form["email"]
            # новый email

            faculty = request.form["faculty"]
            # новый факультет

            course = int(request.form["course"])
            # новый курс

            gpa = float(request.form["gpa"])
            # новый GPA


            service.update_user(
                user_id,
                first_name,
                last_name,
                age,
                email
            )
            # меняем общие поля через service


            student.faculty = faculty
            student.course = course
            student.gpa = gpa
            # меняем поля, которые есть только у Student


            save_users(service.users)
            # сохраняем изменения в JSON


            return redirect(url_for("students"))
            # возвращаемся на список студентов


        except ValueError as error:

            return f"Error: {error}"


    return render_template(
        "edit_student.html",
        student=student
    )
    # если GET, показываем форму и передаём туда найденного студента


@app.route("/teachers/edit/<int:user_id>", methods=["GET", "POST"])

def edit_teacher(user_id):

    teacher = service.find_user_by_id(user_id)
    # ищем преподавателя

    if teacher is None:
        return "Teacher not found"


    if request.method == "POST":

        try:

            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            age = int(request.form["age"])
            email = request.form["email"]
            department = request.form["department"]
            subject = request.form["subject"]
            experience = int(request.form["experience"])


            service.update_user(
                user_id,
                first_name,
                last_name,
                age,
                email
            )


            teacher.department = department
            teacher.subject = subject
            teacher.experience = experience


            save_users(service.users)


            return redirect(url_for("teachers"))


        except ValueError as error:

            return f"Error: {error}"


    return render_template(
        "edit_teacher.html",
        teacher=teacher
    )


if __name__ == "__main__":
    app.run(debug=True)