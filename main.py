import datetime
import os
import random
import flask_login
from flask import Flask, url_for, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# forms
from forms.registration import RegisterForm
from forms.login import LoginForm
from forms.add_folder import FolderForm
from forms.add_status import StatusForm
from forms.add_task import TaskForm
from forms.edit_task import EditTaskForm
# db
from data import db_session
from data.users import User
from data.tasks import Tasks
from data.folders import Folder
from data.status import Status
from data.importance import Importance

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key1'
app.config['GALLERY_FOLDER'] = 'static/img'

login_manager = LoginManager()
login_manager.init_app(app)

current_user_id = 0
loggin = False


@app.route('/folder', methods=['GET', 'POST'])
@login_required
def folder():
    form = FolderForm()
    if form.validate_on_submit():
        add_folder(form.name.data)
        return redirect('/index')
    return render_template('addFolder.html', form=form)


@app.route('/task', methods=['GET', 'POST'])
@login_required
def task():
    form = TaskForm()
    db_sess = db_session.create_session()
    form.set_status_choices([s.name for s in db_sess.query(Status).filter(Status.user_id == current_user.id)])
    form.set_importance_choices([s.name for s in db_sess.query(Importance).all()])
    form.set_folder_choices([s.name for s in db_sess.query(Folder).filter(Folder.user_id == current_user.id)])
    if form.validate_on_submit():
        params_session = db_session.create_session()
        for i in params_session.query(Folder).filter(Folder.name == ''.join(form.folder.data)):
            f = i.id
        for i in params_session.query(Status).filter(Status.name == ''.join(form.status.data)):
            s = i.id
        for i in params_session.query(Importance).filter(Importance.name == ''.join(form.importance.data)):
            im = i.id
        params_session.expire_on_commit = False
        params_session.commit()
        add_task(form.name.data, form.description.data, f, s, im)
        return redirect('/')
    return render_template('addTask.html', form=form)


@app.route('/task_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def task_edit(id):
    form = EditTaskForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        task = db_sess.query(Tasks).filter(Tasks.id == id,).first()

        if task:
            form.name.data = task.title
            form.description.data = task.description
        else:
            abort(404)
    db_sess = db_session.create_session()
    form.set_status_choices([s.name for s in db_sess.query(Status).filter(Status.user_id == current_user.id)])
    form.set_importance_choices([s.name for s in db_sess.query(Importance).all()])
    form.set_folder_choices([s.name for s in db_sess.query(Folder).filter(Folder.user_id == current_user.id)])
    if form.validate_on_submit():
        task = db_sess.query(Tasks).filter(Tasks.id == id, ).first()
        params_session = db_session.create_session()
        for i in params_session.query(Folder).filter(Folder.name == ''.join(form.folder.data)):
            f = i.id
        for i in params_session.query(Status).filter(Status.name == ''.join(form.status.data)):
            s = i.id
        for i in params_session.query(Importance).filter(Importance.name == ''.join(form.importance.data)):
            im = i.id
        params_session.expire_on_commit = False
        params_session.commit()
        if task:
            task.title = form.name.data
            task.description = form.description.data
            task.status_id = s
            task.folder_id = f
            task.importance_id = im
            db_sess.commit()
        else:
            abort(404)
        return redirect('/')
    return render_template('editTask.html', form=form)


@app.route('/delete_task/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_task(id):
    db_sess = db_session.create_session()
    task = db_sess.query(Tasks).filter(Tasks.id == id,
                                       Tasks.user == current_user).first()
    if task:
        db_sess.delete(task)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/status', methods=['GET', 'POST'])
@login_required
def status():
    form = StatusForm()
    if form.validate_on_submit():
        add_status(form.name.data)
        return redirect('/index')
    return render_template('addStatus.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/test')
def test():
    return redirect('/index')


@app.route('/index/<int:folder_id>', methods=['GET', 'POST'])
def get_tasks(folder_id):
    db_sess = db_session.create_session()
    tasks = db_sess.query(Tasks).filter(Tasks.folder_id == folder_id)
    folders = db_sess.query(Folder).filter(Folder.user_id == current_user.id)
    folder_name = db_sess.query(Folder).filter(Folder.id == folder_id, Folder.user_id == current_user.id).first().name
    return render_template("index.html", tasks=tasks, folders=folders, folder_name=folder_name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            loggin = True
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        tasks = db_sess.query(Tasks).filter(Tasks.user_id == current_user.id)
        folders = db_sess.query(Folder).filter(Folder.user_id == current_user.id)
        return render_template("index.html", tasks=tasks, folders=folders)
    else:
        return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
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
        if form.image.data:
            print(form.image.data)

        user = User(
            login=form.name.data,
            email=form.email.data,
            about=form.about.data,
            img=0
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/index')
    return render_template('register.html', title='Регистрация', form=form)


def add_folder(text):
    db_sess = db_session.create_session()
    f = Folder(
        name=text,
        user_id=current_user.id
    )
    db_sess.add(f)
    db_sess.commit()


def add_status(text):
    db_sess = db_session.create_session()
    s = Status(
        name=text,
        user_id=current_user.id
    )
    db_sess.add(s)
    db_sess.commit()


def delete_status(n):
    db_sess = db_session.create_session()
    db_sess.query(Status).filter(Status.id == int(n)).delete()
    db_sess.commit()


def delete_task(n):
    db_sess = db_session.create_session()
    db_sess.query(Tasks).filter(Tasks.id == int(n)).delete()
    db_sess.commit()


def add_task(title, description, folder, status, importance):
    task = Tasks(
        title=title,
        description=description,
        deadline=datetime.datetime.now(),
        folder_id=folder,
        status_id=status,
        importance_id=importance
    )
    db_sess = db_session.create_session()
    current_user.tasks.append(task)
    db_sess.merge(current_user)
    db_sess.commit()


if __name__ == '__main__':
    db_session.global_init("db/main.db")
    app.run(port=8080, host='127.0.0.1')
