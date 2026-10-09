import tkinter as tk
from tkinter import ttk, messagebox

from models import Student, Teacher
from services import UniversityService
from utils import load_users, save_users
from logger import logger


# ---------------- COLORS ----------------

BG = "#0f172a"
SIDEBAR = "#111827"

PRIMARY = "#3b82f6"
ACCENT = "#38bdf8"

LIGHT_BLUE = "#bae6fd"
VERY_LIGHT_BLUE = "#e0f2fe"

CARD = "#7dd3fc"

TEXT = "#000000"

ROW_WHITE = "#f8fafc"
ROW_LIGHT = "#e0f2fe"
SELECT = "#7dd3fc"

DANGER = "#ef4444"
SUCCESS = "#22c55e"
SECONDARY = "#94a3b8"


# ---------------- SERVICE ----------------

service = UniversityService()
service.users = load_users()

logger.info("GUI приложение запущено")


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()

root.title("University Manager")
root.geometry("1180x680")
root.minsize(1000, 600)

root.configure(bg=BG)

current_view = "all"
current_tree = None


# ---------------- TABLE STYLE ----------------

style = ttk.Style()

style.theme_use("clam")


# Основные строки таблицы
style.configure(
    "Treeview",
    background=ROW_WHITE,
    foreground="black",
    fieldbackground=ROW_WHITE,
    rowheight=38,
    font=("Arial", 12),
    borderwidth=0
)


# Заголовки таблицы
style.configure(
    "Treeview.Heading",
    background=PRIMARY,
    foreground="black",
    font=("Arial", 13, "bold"),
    relief="flat",
    padding=(10, 12)
)


# Выбранная строка
style.map(
    "Treeview",
    background=[("selected", SELECT)],
    foreground=[("selected", "black")]
)


# Наведение на заголовок
style.map(
    "Treeview.Heading",
    background=[("active", ACCENT)],
    foreground=[("active", "black")]
)


# ---------------- COMMON ----------------

def save_data():
    save_users(service.users)


def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()


def close_app():
    logger.info("GUI приложение закрыто")
    root.destroy()


root.protocol("WM_DELETE_WINDOW", close_app)


# Получаем пользователя из выбранной строки
def get_selected_user():
    if current_tree is None:
        return None

    selected = current_tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Сначала выберите пользователя"
        )

        return None

    values = current_tree.item(
        selected[0],
        "values"
    )

    # 0 = номер строки
    # 1 = ID пользователя
    user_id = int(values[1])

    return service.find_user_by_id(user_id)


# ---------------- REFRESH ----------------

def refresh_current_view():

    if current_view == "students":
        show_students()

    elif current_view == "teachers":
        show_teachers()

    else:
        show_all_users()


# ---------------- TABLE ----------------

def show_user_table(users, title):
    global current_tree

    clear_content()


    # Заголовок страницы
    tk.Label(
        content_frame,
        text=f"{title} ({len(users)})",
        font=("Arial", 26, "bold"),
        fg="black",
        bg=ACCENT
    ).pack(
        fill="x",
        padx=35,
        pady=(28, 0),
        ipady=10
    )


    tk.Label(
        content_frame,
        text="University user management",
        font=("Arial", 12),
        fg="black",
        bg=LIGHT_BLUE
    ).pack(
        fill="x",
        padx=35,
        pady=(0, 18),
        ipady=6
    )


    # ---------------- SEARCH ----------------

    search_frame = tk.Frame(
        content_frame,
        bg=BG
    )

    search_frame.pack(
        fill="x",
        padx=35,
        pady=(0, 15)
    )


    search_entry = tk.Entry(
        search_frame,
        font=("Arial", 13),
        bg="white",
        fg="black",
        insertbackground="black",
        relief="flat"
    )

    search_entry.pack(
        side="left",
        fill="x",
        expand=True,
        ipady=8,
        padx=(0, 10)
    )


    tk.Button(
        search_frame,
        text="Search",
        width=11,
        bg=ACCENT,
        fg="black",
        activebackground=LIGHT_BLUE,
        activeforeground="black",
        relief="flat",
        command=lambda: search_users(search_entry.get())
    ).pack(
        side="left"
    )


    # ---------------- TABLE ----------------

    table_card = tk.Frame(
        content_frame,
        bg=ACCENT
    )

    table_card.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=(0, 10)
    )


    table_inner = tk.Frame(
        table_card,
        bg="white"
    )

    table_inner.pack(
        fill="both",
        expand=True,
        padx=2,
        pady=2
    )


    columns = (
        "number",
        "id",
        "type",
        "name",
        "age",
        "email",
        "details"
    )


    current_tree = ttk.Treeview(
        table_inner,
        columns=columns,
        show="headings"
    )


    scrollbar = ttk.Scrollbar(
        table_inner,
        orient="vertical",
        command=current_tree.yview
    )


    current_tree.configure(
        yscrollcommand=scrollbar.set
    )


    # Заголовки
    current_tree.heading("number", text="№")
    current_tree.heading("id", text="ID")
    current_tree.heading("type", text="Type")
    current_tree.heading("name", text="Name")
    current_tree.heading("age", text="Age")
    current_tree.heading("email", text="Email")
    current_tree.heading("details", text="Details")


    # Размеры
    current_tree.column("number", width=50, anchor="center")
    current_tree.column("id", width=70, anchor="center")
    current_tree.column("type", width=100, anchor="center")
    current_tree.column("name", width=190)
    current_tree.column("age", width=70, anchor="center")
    current_tree.column("email", width=220)
    current_tree.column("details", width=350)


    current_tree.pack(
        side="left",
        fill="both",
        expand=True
    )


    scrollbar.pack(
        side="right",
        fill="y"
    )


    # Цвет строк
    current_tree.tag_configure(
        "oddrow",
        background=ROW_WHITE
    )

    current_tree.tag_configure(
        "evenrow",
        background=ROW_LIGHT
    )


    # Заполняем таблицу
    for number, user in enumerate(
        users,
        start=1
    ):

        if isinstance(user, Student):

            user_type = "Student"

            details = (
                f"{user.faculty} | "
                f"Course: {user.course} | "
                f"GPA: {user.gpa}"
            )

        else:

            user_type = "Teacher"

            details = (
                f"{user.department} | "
                f"{user.subject} | "
                f"Experience: {user.experience}"
            )


        row_tag = (
            "evenrow"
            if number % 2 == 0
            else "oddrow"
        )


        current_tree.insert(
            "",
            "end",
            values=(
                number,
                user.user_id,
                user_type,
                f"{user.first_name} {user.last_name}",
                user.age,
                user.email,
                details
            ),
            tags=(row_tag,)
        )


    # ---------------- ACTION BUTTONS ----------------

    buttons_frame = tk.Frame(
        content_frame,
        bg=BG
    )

    buttons_frame.pack(
        fill="x",
        padx=35,
        pady=(5, 20)
    )


    tk.Button(
        buttons_frame,
        text="Add Student",
        width=13,
        bg=PRIMARY,
        fg="black",
        activebackground=ACCENT,
        activeforeground="black",
        relief="flat",
        command=show_student_form
    ).pack(
        side="left",
        padx=(0, 8)
    )


    tk.Button(
        buttons_frame,
        text="Add Teacher",
        width=13,
        bg=PRIMARY,
        fg="black",
        activebackground=ACCENT,
        activeforeground="black",
        relief="flat",
        command=show_teacher_form
    ).pack(
        side="left",
        padx=(0, 8)
    )


    tk.Button(
        buttons_frame,
        text="Edit",
        width=10,
        bg=ACCENT,
        fg="black",
        activebackground=LIGHT_BLUE,
        activeforeground="black",
        relief="flat",
        command=edit_selected_user
    ).pack(
        side="left",
        padx=(0, 8)
    )


    tk.Button(
        buttons_frame,
        text="Delete",
        width=10,
        bg=DANGER,
        fg="black",
        activebackground="#f87171",
        activeforeground="black",
        relief="flat",
        command=delete_selected_user
    ).pack(
        side="left"
    )


# ---------------- VIEWS ----------------

def show_all_users():
    global current_view

    current_view = "all"

    show_user_table(
        service.users,
        "All Users"
    )


def show_students():
    global current_view

    current_view = "students"

    show_user_table(
        service.get_students(),
        "Students"
    )


def show_teachers():
    global current_view

    current_view = "teachers"

    show_user_table(
        service.get_teachers(),
        "Teachers"
    )


# ---------------- SEARCH ----------------

def search_users(query):

    query = query.strip()

    if not query:
        refresh_current_view()
        return

    results = service.search_user(query)

    show_user_table(
        results,
        f"Search: {query}"
    )


# ---------------- DELETE ----------------

def delete_selected_user():

    user = get_selected_user()

    if user is None:
        return


    answer = messagebox.askyesno(
        "Delete",
        f"Удалить {user.first_name} {user.last_name}?"
    )


    if not answer:
        return


    service.delete_user(
        user.user_id
    )

    save_data()

    refresh_current_view()


# ---------------- EDIT ----------------

def edit_selected_user():

    user = get_selected_user()

    if user is None:
        return


    if isinstance(user, Student):
        show_student_form(user)

    elif isinstance(user, Teacher):
        show_teacher_form(user)


# ---------------- STUDENT FORM ----------------

def show_student_form(student=None):

    clear_content()


    title = (
        "Add Student"
        if student is None
        else "Edit Student"
    )


    tk.Label(
        content_frame,
        text=title,
        font=("Arial", 26, "bold"),
        fg="black",
        bg=ACCENT
    ).pack(
        fill="x",
        padx=40,
        pady=(30, 0),
        ipady=10
    )


    tk.Label(
        content_frame,
        text="Fill in the student information",
        font=("Arial", 12),
        fg="black",
        bg=LIGHT_BLUE
    ).pack(
        fill="x",
        padx=40,
        pady=(0, 20),
        ipady=6
    )


    form_frame = tk.Frame(
        content_frame,
        bg=BG
    )

    form_frame.pack(
        anchor="nw",
        padx=40
    )


    fields = {}


    labels = [
        "ID",
        "First name",
        "Last name",
        "Age",
        "Email",
        "Faculty",
        "Course",
        "GPA"
    ]


    for row, label_text in enumerate(labels):

        tk.Label(
            form_frame,
            text=label_text,
            width=15,
            anchor="w",
            font=("Arial", 12, "bold"),
            fg="black",
            bg=LIGHT_BLUE
        ).grid(
            row=row,
            column=0,
            padx=(0, 12),
            pady=8,
            ipady=5
        )


        entry = tk.Entry(
            form_frame,
            width=38,
            font=("Arial", 12),
            bg="white",
            fg="black",
            insertbackground="black",
            relief="flat"
        )

        entry.grid(
            row=row,
            column=1,
            pady=8,
            ipady=6
        )


        fields[label_text] = entry


    if student is not None:

        fields["ID"].insert(
            0,
            student.user_id
        )

        fields["ID"].config(
            state="disabled"
        )

        fields["First name"].insert(
            0,
            student.first_name
        )

        fields["Last name"].insert(
            0,
            student.last_name
        )

        fields["Age"].insert(
            0,
            student.age
        )

        fields["Email"].insert(
            0,
            student.email
        )

        fields["Faculty"].insert(
            0,
            student.faculty
        )

        fields["Course"].insert(
            0,
            student.course
        )

        fields["GPA"].insert(
            0,
            student.gpa
        )


    def save_student():

        try:

            user_id = (
                int(fields["ID"].get())
                if student is None
                else student.user_id
            )

            first_name = fields["First name"].get()
            last_name = fields["Last name"].get()
            age = int(fields["Age"].get())
            email = fields["Email"].get()
            faculty = fields["Faculty"].get()
            course = int(fields["Course"].get())
            gpa = float(fields["GPA"].get())


            if student is None:

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


                if not service.add_user(
                    new_student
                ):

                    messagebox.showerror(
                        "Error",
                        "Пользователь с таким ID уже существует"
                    )

                    return


            else:

                service.update_user(
                    student.user_id,
                    first_name,
                    last_name,
                    age,
                    email
                )

                student.faculty = faculty
                student.course = course
                student.gpa = gpa


            save_data()

            show_students()


        except ValueError as error:

            logger.warning(
                f"Ошибка формы Student: {error}"
            )

            messagebox.showerror(
                "Error",
                str(error)
            )


    buttons = tk.Frame(
        content_frame,
        bg=BG
    )

    buttons.pack(
        anchor="w",
        padx=40,
        pady=25
    )


    tk.Button(
        buttons,
        text="Save",
        width=12,
        bg=SUCCESS,
        fg="black",
        activebackground="#4ade80",
        activeforeground="black",
        relief="flat",
        command=save_student
    ).pack(
        side="left",
        padx=(0, 10)
    )


    tk.Button(
        buttons,
        text="Cancel",
        width=12,
        bg=SECONDARY,
        fg="black",
        activebackground=LIGHT_BLUE,
        activeforeground="black",
        relief="flat",
        command=show_students
    ).pack(
        side="left"
    )


# ---------------- TEACHER FORM ----------------

def show_teacher_form(teacher=None):

    clear_content()


    title = (
        "Add Teacher"
        if teacher is None
        else "Edit Teacher"
    )


    tk.Label(
        content_frame,
        text=title,
        font=("Arial", 26, "bold"),
        fg="black",
        bg=ACCENT
    ).pack(
        fill="x",
        padx=40,
        pady=(30, 0),
        ipady=10
    )


    tk.Label(
        content_frame,
        text="Fill in the teacher information",
        font=("Arial", 12),
        fg="black",
        bg=LIGHT_BLUE
    ).pack(
        fill="x",
        padx=40,
        pady=(0, 20),
        ipady=6
    )


    form_frame = tk.Frame(
        content_frame,
        bg=BG
    )

    form_frame.pack(
        anchor="nw",
        padx=40
    )


    fields = {}


    labels = [
        "ID",
        "First name",
        "Last name",
        "Age",
        "Email",
        "Department",
        "Subject",
        "Experience"
    ]


    for row, label_text in enumerate(labels):

        tk.Label(
            form_frame,
            text=label_text,
            width=15,
            anchor="w",
            font=("Arial", 12, "bold"),
            fg="black",
            bg=LIGHT_BLUE
        ).grid(
            row=row,
            column=0,
            padx=(0, 12),
            pady=8,
            ipady=5
        )


        entry = tk.Entry(
            form_frame,
            width=38,
            font=("Arial", 12),
            bg="white",
            fg="black",
            insertbackground="black",
            relief="flat"
        )

        entry.grid(
            row=row,
            column=1,
            pady=8,
            ipady=6
        )


        fields[label_text] = entry


    if teacher is not None:

        fields["ID"].insert(
            0,
            teacher.user_id
        )

        fields["ID"].config(
            state="disabled"
        )

        fields["First name"].insert(
            0,
            teacher.first_name
        )

        fields["Last name"].insert(
            0,
            teacher.last_name
        )

        fields["Age"].insert(
            0,
            teacher.age
        )

        fields["Email"].insert(
            0,
            teacher.email
        )

        fields["Department"].insert(
            0,
            teacher.department
        )

        fields["Subject"].insert(
            0,
            teacher.subject
        )

        fields["Experience"].insert(
            0,
            teacher.experience
        )


    def save_teacher():

        try:

            user_id = (
                int(fields["ID"].get())
                if teacher is None
                else teacher.user_id
            )

            first_name = fields["First name"].get()
            last_name = fields["Last name"].get()
            age = int(fields["Age"].get())
            email = fields["Email"].get()
            department = fields["Department"].get()
            subject = fields["Subject"].get()
            experience = int(fields["Experience"].get())


            if teacher is None:

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


                if not service.add_user(
                    new_teacher
                ):

                    messagebox.showerror(
                        "Error",
                        "Пользователь с таким ID уже существует"
                    )

                    return


            else:

                service.update_user(
                    teacher.user_id,
                    first_name,
                    last_name,
                    age,
                    email
                )

                teacher.department = department
                teacher.subject = subject
                teacher.experience = experience


            save_data()

            show_teachers()


        except ValueError as error:

            logger.warning(
                f"Ошибка формы Teacher: {error}"
            )

            messagebox.showerror(
                "Error",
                str(error)
            )


    buttons = tk.Frame(
        content_frame,
        bg=BG
    )

    buttons.pack(
        anchor="w",
        padx=40,
        pady=25
    )


    tk.Button(
        buttons,
        text="Save",
        width=12,
        bg=SUCCESS,
        fg="black",
        activebackground="#4ade80",
        activeforeground="black",
        relief="flat",
        command=save_teacher
    ).pack(
        side="left",
        padx=(0, 10)
    )


    tk.Button(
        buttons,
        text="Cancel",
        width=12,
        bg=SECONDARY,
        fg="black",
        activebackground=LIGHT_BLUE,
        activeforeground="black",
        relief="flat",
        command=show_teachers
    ).pack(
        side="left"
    )


# ---------------- STATISTICS ----------------

def create_stat_card(parent, title, value, column):

    card = tk.Frame(
        parent,
        bg=CARD,
        bd=0
    )

    card.grid(
        row=0,
        column=column,
        padx=8,
        sticky="nsew"
    )


    parent.grid_columnconfigure(
        column,
        weight=1
    )


    tk.Label(
        card,
        text=title,
        font=("Arial", 12, "bold"),
        fg="black",
        bg=CARD
    ).pack(
        padx=20,
        pady=(18, 5)
    )


    tk.Label(
        card,
        text=value,
        font=("Arial", 26, "bold"),
        fg="black",
        bg=CARD
    ).pack(
        padx=20,
        pady=(0, 18)
    )


def show_statistics():

    global current_view

    current_view = "statistics"

    clear_content()


    students = service.get_students()
    teachers = service.get_teachers()
    total_users = len(service.users)


    if students:

        average_gpa = (
            sum(
                student.gpa
                for student in students
            )
            / len(students)
        )

        top_student = max(
            students,
            key=lambda student: student.gpa
        )

    else:

        average_gpa = 0
        top_student = None


    tk.Label(
        content_frame,
        text="University Statistics",
        font=("Arial", 28, "bold"),
        fg="black",
        bg=ACCENT
    ).pack(
        fill="x",
        padx=40,
        pady=(35, 0),
        ipady=10
    )


    tk.Label(
        content_frame,
        text="Overview of the university",
        font=("Arial", 13),
        fg="black",
        bg=LIGHT_BLUE
    ).pack(
        fill="x",
        padx=40,
        pady=(0, 25),
        ipady=6
    )


    cards_frame = tk.Frame(
        content_frame,
        bg=BG
    )

    cards_frame.pack(
        fill="x",
        padx=32,
        pady=10
    )


    create_stat_card(
        cards_frame,
        "Total Users",
        total_users,
        0
    )

    create_stat_card(
        cards_frame,
        "Students",
        len(students),
        1
    )

    create_stat_card(
        cards_frame,
        "Teachers",
        len(teachers),
        2
    )

    create_stat_card(
        cards_frame,
        "Average GPA",
        f"{average_gpa:.2f}",
        3
    )


    if top_student:

        top_frame = tk.Frame(
            content_frame,
            bg=ACCENT,
            bd=0
        )

        top_frame.pack(
            fill="x",
            padx=40,
            pady=(28, 10)
        )


        tk.Label(
            top_frame,
            text="Top Student",
            font=("Arial", 16, "bold"),
            fg="black",
            bg=ACCENT
        ).pack(
            anchor="w",
            padx=22,
            pady=(18, 6)
        )


        tk.Label(
            top_frame,
            text=f"{top_student.first_name} {top_student.last_name}",
            font=("Arial", 20, "bold"),
            fg="black",
            bg=ACCENT
        ).pack(
            anchor="w",
            padx=22,
            pady=3
        )


        tk.Label(
            top_frame,
            text=f"Faculty: {top_student.faculty}",
            font=("Arial", 12),
            fg="black",
            bg=ACCENT
        ).pack(
            anchor="w",
            padx=22,
            pady=3
        )


        tk.Label(
            top_frame,
            text=f"Course: {top_student.course}",
            font=("Arial", 12),
            fg="black",
            bg=ACCENT
        ).pack(
            anchor="w",
            padx=22,
            pady=3
        )


        tk.Label(
            top_frame,
            text=f"GPA: {top_student.gpa}",
            font=("Arial", 15, "bold"),
            fg="black",
            bg=ACCENT
        ).pack(
            anchor="w",
            padx=22,
            pady=(5, 18)
        )


# ---------------- LAYOUT ----------------

menu_frame = tk.Frame(
    root,
    width=195,
    bg=SIDEBAR
)

menu_frame.pack(
    side="left",
    fill="y"
)

menu_frame.pack_propagate(False)


content_frame = tk.Frame(
    root,
    bg=BG
)

content_frame.pack(
    side="right",
    fill="both",
    expand=True
)


# Название
tk.Label(
    menu_frame,
    text="University",
    font=("Arial", 20, "bold"),
    fg="black",
    bg=ACCENT
).pack(
    fill="x",
    padx=10,
    pady=(38, 35),
    ipady=8
)


# ---------------- MENU BUTTONS ----------------

tk.Button(
    menu_frame,
    text="All Users",
    width=17,
    bg=PRIMARY,
    fg="black",
    activebackground=ACCENT,
    activeforeground="black",
    relief="flat",
    command=show_all_users
).pack(
    pady=7
)


tk.Button(
    menu_frame,
    text="Students",
    width=17,
    bg=PRIMARY,
    fg="black",
    activebackground=ACCENT,
    activeforeground="black",
    relief="flat",
    command=show_students
).pack(
    pady=7
)


tk.Button(
    menu_frame,
    text="Teachers",
    width=17,
    bg=PRIMARY,
    fg="black",
    activebackground=ACCENT,
    activeforeground="black",
    relief="flat",
    command=show_teachers
).pack(
    pady=7
)


tk.Button(
    menu_frame,
    text="Statistics",
    width=17,
    bg=PRIMARY,
    fg="black",
    activebackground=ACCENT,
    activeforeground="black",
    relief="flat",
    command=show_statistics
).pack(
    pady=7
)


# ---------------- START ----------------

show_all_users()

root.mainloop()