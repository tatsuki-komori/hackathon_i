from flask import Flask,render_template,request,session,redirect,url_for
from models.models import User, Task
from models.database import db_session
from datetime import datetime
from app import key
from hashlib import sha256

app = Flask(__name__)
app.secret_key = key.SECRET_KEY


@app.route("/")
def index():
    if "user_id" in session and User.query.get(session["user_id"]):

        if "team_name" in session:
            all_tasks = Task.query.filter_by(completed=True).outerjoin(User, User.id == Task.user_id).filter(User.team_name == session["team_name"]).order_by(Task.done_datetime.desc())
        else:
            all_tasks = Task.query.filter_by(completed=True).order_by(Task.done_datetime.desc())
        
        user_id = session["user_id"]
        user = User.query.get(user_id)
        name = user.user_name
        myteam_name = user.team_name

        return render_template("index.html", name=name, all_tasks=all_tasks, myteam_name=myteam_name)
    else:
        return redirect(url_for("top",status="logout"))

@app.route("/mypage")
def mypage():
    user_id = session["user_id"]
    user = User.query.get(user_id)
    goal = user.goal
    name = user.user_name
    myteam_name = user.team_name
    user_tasks = Task.query.filter_by(user_id=user_id)

    if user_tasks.count() != 0:
        rate = user_tasks.filter_by(completed=True).count() / user_tasks.count()
    else:
        rate = 0.0

    if "display_task" in session and session["display_task"] == '1':
        return render_template("mypage_done.html", name=name, goal=goal, user_tasks=user_tasks, rate=rate, myteam_name=myteam_name)
    else:
        return render_template("mypage_tasks.html", name=name, goal=goal, user_tasks=user_tasks, rate=rate, myteam_name=myteam_name)

@app.route("/mypage/switch", methods=["post"])
def switch():
    session["display_task"] = request.form["switch"]
    return redirect(url_for("mypage"))

@app.route("/top")
def top():
    status = request.args.get("status")
    return render_template("top.html",status=status)


@app.route("/login",methods=["post"])
def login():
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        if user.hashed_password == hashed_password:
            session["user_id"] = user.id
            return redirect(url_for("index"))
        else:
            return redirect(url_for("top",status="wrong_password"))
    else:
        return redirect(url_for("top",status="user_notfound"))


@app.route("/newcomer")
def newcomer():
    status = request.args.get("status")
    return render_template("newcomer.html",status=status)


@app.route("/registar",methods=["post"])
def registar():
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        return redirect(url_for("newcomer",status="exist_user"))
    else:
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        user = User(user_name, hashed_password, 0)
        db_session.add(user)
        db_session.commit()
        session["user_id"] = user.id
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("next_task", None)
    session.pop("display_task", None)
    return redirect(url_for("top",status="logout"))

@app.route("/add", methods=["post"])
def add():
    content = request.form["content"]
    detail = request.form["detail"]
    task = Task(content, detail, session["user_id"], User.query.get(session["user_id"]).user_name)
    if Task.query.filter_by(user_id=session["user_id"]).count() == 0:
        task.next_flag = True
    db_session.add(task)
    db_session.commit()
    return redirect(url_for("mypage"))

@app.route("/done", methods=["post"])
def complete():
    task_id = request.form["done_task_id"]
    task = Task.query.filter_by(id=task_id).first()
    task.completed = True
    task.next_flag = False
    task.done_datetime = datetime.now()
    rest_task = Task.query.filter_by(user_id=session["user_id"]).filter_by(completed=False).filter_by(next_flag=False)
    if rest_task.count() != 0:
        rest_task.order_by(Task.id.asc()).first().next_flag = True
    db_session.commit()
    
    return redirect(url_for("mypage"))

@app.route("/edit", methods=["post"])
def edit():
    task = Task.query.filter_by(id=request.form["edit_task_id"]).first()
    task.content = request.form["content"]
    task.detail = request.form["detail"]
    db_session.commit()
    return redirect(url_for("mypage"))

@app.route("/set_team", methods=["post"])
def set_team():
    myteam_name = request.form["myteam_name"]
    if myteam_name != '':
        user = User.query.get(session["user_id"])
        user.team_name = myteam_name
        db_session.commit()
    return redirect(url_for("mypage"))

@app.route("/filter_team", methods=["post"])
def filter_team():
    team_name = request.form["filter_team"]
    if team_name == '':
        session.pop("team_name", None)
    else:
        session["team_name"] = team_name
    return redirect(url_for("index"))

@app.route("/mypage/this_is_next", methods=["post"])
def this_is_next():
    user_id = session["user_id"]
    for task in Task.query.filter_by(user_id=user_id).filter_by(next_flag=True):
        task.next_flag = False
    Task.query.get(request.form["this_is_next"]).next_flag = True
    db_session.commit()
    return redirect(url_for("mypage"))

@app.route("/mypage/add_goal", methods=["post"])
def add_goal():
    user = User.query.get(session["user_id"])
    user.goal = request.form["add_goal"]
    db_session.commit()
    return redirect(url_for("mypage"))

if __name__ == "__main__":
    app.run(debug=True)