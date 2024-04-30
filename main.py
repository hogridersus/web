from flask import Flask, render_template, redirect
from data import db_session
from data.models import *
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            nickname=form.nickname.data,
            about=form.about.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/0")
        return render_template('login.html', title='Авторизация',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/0")


@app.route("/marks")
def marks():
    if not current_user.is_authenticated:
        return redirect('/login')
    session = db_session.create_session()

    if current_user.status == 'student':
        school = session.query(School).filter(current_user.school_id == School.id).first()
        grade = session.query(Grade).filter(current_user.grade_id == Grade.id).first()
        subjects = {}
        for i in current_user.marks:
            subjects[i.subject.name] = session.query(Mark).filter(Mark.user_id == current_user.id,
                                                                  Mark.subject_id == i.subject_id).all()
        return render_template("marks_student.html", title='Дневник', school=school, grade=grade, subjects=subjects)
    else:
        return "not done"


@app.route("/<week_n>")
def index(week_n):
    if not current_user.is_authenticated:
        return redirect('/login')
    session = db_session.create_session()

    schools = session.query(School).all()
    users = session.query(User).all()

    if current_user.status == 'student':
        week_now = 0 + int(week_n)
        school = session.query(School).filter(current_user.school_id == School.id).first()
        grade = session.query(Grade).filter(current_user.grade_id == Grade.id).first()
        days = session.query(Day).filter(current_user.grade_id == Day.grade_id, week_now == Day.week).all()

        date = datetime.datetime.now().date() + datetime.timedelta(weeks=int(week_n))
        start = date - datetime.timedelta(days=date.weekday())
        end = start + datetime.timedelta(days=6)

        week = f"{'{:02d}'.format(start.day)}.{'{:02d}'.format(start.month)} - {'{:02d}'.format(end.day)}.{'{:02d}'.format(end.month)}"
        return render_template("index_student.html", title='Дневник', school=school, grade=grade, days=days, week=week,
                               week_int=week_now)
    elif current_user.status == 'teacher':
        week_now = 0 + int(week_n)
        school = session.query(School).filter(current_user.school_id == School.id).first()
        days = session.query(Day).filter(week_now == Day.week).all()

        date = datetime.datetime.now().date() + datetime.timedelta(weeks=int(week_n))
        start = date - datetime.timedelta(days=date.weekday())
        end = start + datetime.timedelta(days=6)

        week = f"{'{:02d}'.format(start.day)}.{'{:02d}'.format(start.month)} - {'{:02d}'.format(end.day)}.{'{:02d}'.format(end.month)}"
        lessons = dict()
        for i in days:
            lessons[i.name] = session.query(Lesson).filter(current_user.id == Lesson.teacher_id,
                                                           i.id == Lesson.day_id).all()
        return render_template("index_teacher.html", title='Журнал', school=school, days=days, week=week,
                               week_int=week_now, lessons=lessons)


def main():
    db_session.global_init("db/data.db")
    session = db_session.create_session()

    app.run(port=8080, host='127.0.0.1')


def add_default():
    session = db_session.create_session()

    for i in ['Алгебра', 'Геометрия', 'Русский Язык', 'ИЗО', 'Музыка', 'Математика', 'Литература', 'Физика',
              'Химия', 'Английский язык', 'Физкультура', 'Биология', 'Информатика', 'Технология']:
        subject = Subject()
        subject.name = i
        session.add(subject)
        session.commit()

    school = School()
    school.login = 'maou33'
    school.name = 'МАОУ СОШ 33'
    session.add(school)
    session.commit()

    for i in ['1А', '1Б', '1В', '1Г',
              '2А', '2Б', '2В', '2Г',
              '3А', '3Б', '3В', '3Г',
              '4А', '4Б', '4В', '4Г',
              '5А', '5Б', '5В', '5Г',
              '6А', '6Б', '6В', '6ИМ', '6Л', '6ФМ',
              '7А', '7Б', '7В', '7ИМ', '7Л', '7ФМ',
              '8А', '8Б', '8В', '8ИМ', '8Л', '8ФМ',
              '9А', '9Б', '9В', '9ИМ', '9Л', '9ФМ',
              '10-1', '10-2', '10-3', '10-4',
              '11-1', '11-2', '11-3', '11-4']:
        grade = Grade()
        grade.name = i
        school.grades.append(grade)
        session.commit()

    user = User()
    user.login = 'test'
    user.email = 'test@test.com'
    user.name = 'тестик'
    user.set_password('test')
    session.add(user)
    session.commit()

    grade = session.query(Grade).filter(Grade.name == '9ИМ', Grade.school_id == school.id).first()
    subject = session.query(Subject).filter(Subject.name == 'Русский Язык').first()

    grade.users.append(user)
    session.commit()
    school.users.append(user)
    session.commit()

    user1 = User()
    user1.login = 'test_t'
    user1.email = 'test_t@test.com'
    user1.name = 'тестик 2'
    user1.status = 'teacher'
    user1.set_password('test_t')
    session.add(user1)
    session.commit()
    for i in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']:
        day = Day()
        day.name = i
        day.week = 0
        session.add(day)
        session.commit()

        lesson = Lesson()
        lesson.order = 1
        lesson.homework = f'Купить слона из мха ({i})'
        lesson.time = '8:15-8:55'
        lesson.classroom = '302'
        lesson.teacher = user1
        day.lessons.append(lesson)
        session.commit()
        grade.lessons.append(lesson)
        session.commit()
        subject.lessons.append(lesson)
        session.commit()

        day.lessons.append(lesson)
        session.commit()

        grade.days.append(day)
        session.commit()

    subject = session.query(Subject).filter(Subject.name == 'Алгебра').first()
    for i in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']:
        day = Day()
        day.name = i
        day.week = 1
        session.add(day)
        session.commit()

        lesson = Lesson()
        lesson.order = 1
        lesson.homework = f'Съесть из мха ({i})'
        lesson.time = '8:15-8:55'
        lesson.classroom = '301'
        day.lessons.append(lesson)
        session.commit()
        grade.lessons.append(lesson)
        session.commit()
        subject.lessons.append(lesson)
        session.commit()

        day.lessons.append(lesson)
        session.commit()

        lesson = Lesson()
        lesson.order = 2
        lesson.homework = f'Съесть из мха ({i} часть 2)'
        lesson.time = '9:05-9:45'
        lesson.classroom = '306'
        day.lessons.append(lesson)
        session.commit()
        grade.lessons.append(lesson)
        session.commit()
        subject.lessons.append(lesson)
        session.commit()

        day.lessons.append(lesson)
        session.commit()

        grade.days.append(day)
        session.commit()
    mark = Mark()
    mark.value = 5
    mark.coeff = 1
    lesson.marks.append(mark)
    session.commit()
    user.marks.append(mark)
    session.commit()
    subject.marks.append(mark)
    session.commit()
    day.marks.append(mark)
    session.commit()

    session.commit()


if __name__ == '__main__':
    main()
