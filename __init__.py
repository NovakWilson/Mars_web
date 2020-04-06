from flask import render_template, make_response, request, session, redirect, abort, Flask
import datetime
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from data import db_session
from flask_restful import Api
from job_resources import JobResource, JobsListResource
from users_resources import UserResource, UsersListResource
from data.users import User, LoginForm, RegisterForm, Jobs, JobForm, Departments, DepartmentForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
login_manager = LoginManager()
login_manager.init_app(app)


def getApp():
    return app


def main():
    api = Api(app)
    db_session.global_init("db/blogs.sqlite")

    api.add_resource(JobsListResource, '/api/v2/jobs')
    api.add_resource(JobResource, '/api/v2/job/<int:job_id>')

    api.add_resource(UsersListResource, '/api/v2/users')
    api.add_resource(UserResource, '/api/v2/user/<int:user_id>')

    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port)


@app.route("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs)
    return render_template("index.html", jobs=jobs)


@app.route("/departments")
def dep_index():
    session = db_session.create_session()
    deps = session.query(Departments)
    return render_template("departments.html", deps=deps)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session_db = db_session.create_session()
        user = session_db.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            session['user'] = user.id
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        #db_session.global_init("db/blogs.sqlite")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
def add_job():
    if not session:
        return 'Для добавления новой работы авторизуйтесь: <a href="/login">Войти</a>'
    form = JobForm()
    if form.validate_on_submit():
        session_db = db_session.create_session()
        if not session_db.query(User).filter(User.id == int(form.team_leader.data)).first():
            return render_template('job.html', title='Добавление работы',
                                   form=form,
                                   message="Пользователь с id {} не найден".format(form.team_leader.data))
        collaborators = [int(i) for i in form.collaborators.data.split(',')]
        for collab_id in collaborators:
            if not session_db.query(User).filter(User.id == collab_id).first():
                return render_template('job.html', title='Добавление работы',
                                   form=form,
                                   message="Пользователь с id {} не найден".format(collab_id))
        job = Jobs(
            team_leader=int(form.team_leader.data),
            user_id=int(session.get('user')),
            user=session_db.query(User).filter(User.id == int(form.team_leader.data)).first(),
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            is_finished=form.is_finished.data
        )
        session_db.add(job)
        session_db.commit()
        return redirect('/')
    return render_template('job.html', title='Добавление работы', form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    session_db = db_session.create_session()
    job = session_db.query(Jobs).filter(Jobs.id == id).first()
    if job:
        if int(session.get('user')) in (job.user_id, 1):
            if request.method == "GET":
                jobs = session_db.query(Jobs).filter(Jobs.id == id).first()
                if jobs:
                    form.team_leader.data = jobs.team_leader
                    form.job.data = jobs.job
                    form.work_size.data = jobs.work_size
                    form.collaborators.data = jobs.collaborators
                    form.start_date.data = jobs.start_date
                    form.end_date.data = jobs.end_date
                    form.is_finished.data = jobs.is_finished
                else:
                    abort(404)
            if form.validate_on_submit():
                session_db = db_session.create_session()
                jobs = session_db.query(Jobs).filter(Jobs.id == id).first()
                if jobs:
                    jobs.team_leader = form.team_leader.data
                    jobs.job = form.job.data
                    jobs.work_size = form.work_size.data
                    jobs.collaborators = form.collaborators.data
                    jobs.start_date = form.start_date.data
                    jobs.end_date = form.end_date.data
                    jobs.is_finished = form.is_finished.data
                    session_db.commit()
                    return redirect('/')
                else:
                    abort(404)
            return render_template('job.html', title='Редактирование работы', form=form)
        else:
            return 'Извените, у вас нет доступа. <a href="/">Вернуться на главную</a>'
    else:
        return 'Работы с id {} не существует. <a href="/">Вернуться на главную</a>'.format(id)


@app.route('/jobs/<int:id>/remove', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    session_db = db_session.create_session()
    job = session_db.query(Jobs).filter(Jobs.id == id).first()
    if job:
        if int(session.get('user')) in (job.user_id, 1):
            session_db.delete(job)
            session_db.commit()
            return redirect('/')
        else:
            return 'Извените, у вас нет прав. <a href="/">Вернуться на главную</a>'
    else:
        return 'Работы с id {} не существует. <a href="/">Вернуться на главную</a>'.format(id)


@app.route('/department/add', methods=['GET', 'POST'])
def add_dep():
    if not session:
        return 'Для добавления нового департамента авторизуйтесь: <a href="/login">Войти</a>'
    form = DepartmentForm()
    if form.validate_on_submit():
        session_db = db_session.create_session()
        if not session_db.query(User).filter(User.id == int(form.chief_id.data)).first():
            return render_template('department.html', title='Добавление департамента',
                                   form=form,
                                   message="Пользователь с id {} не найден".format(form.chief_id.data))
        members = [int(i) for i in form.members.data.split(',')]
        for member in members:
            if not session_db.query(User).filter(User.id == member).first():
                return render_template('department.html', title='Добавление работы',
                                   form=form,
                                   message="Пользователь с id {} не найден".format(member))
        dep = Departments(
            title=form.title.data,
            chief=session_db.query(User).filter(User.id == int(form.chief_id.data)).first(),
            chief_id=form.chief_id.data,
            members=form.members.data,
            email=form.email.data,
        )
        session_db.add(dep)
        session_db.commit()
        return redirect('/departments')
    return render_template('department.html', title='Добавление департамента', form=form)



if __name__ == '__main__':
    main()
