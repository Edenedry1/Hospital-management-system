from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User, Chat
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import os

# from flask import Blueprint, render_template
# from flask_login import login_required,current_user


views = Blueprint('views',__name__)
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        is_active_patient = request.form.get('is_active_patient')
        user = User.query.filter_by(ID=session["user_id"]).first()
        user.is_active_patient = is_active_patient

    # return render_template("home.html", user_name=session['user_name'])
    return render_template("home.html", user_name=session['user_name'], user_role=session['user_role'])


@views.route('/home', methods=['GET', 'POST'])
@login_required
def home2():
    if request.method == 'POST':
        is_active_patient = request.form.get('is_active_patient')
        user = User.query.filter_by(ID=session["user_id"]).first()
        user.is_active_patient = is_active_patient

    # return render_template("home.html", user_name=session['user_name'])
    return render_template("home.html", user_name=session['user_name'], user_role=session['user_role'])

@views.route('/patients', methods=['GET', 'POST'])
def patients():
    print("In views.route(patients)")
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        if 'approve' in request.form.keys():
            flash("patient_id = " + patient_id)
            # print("received patient_id=" + patient_id)
            # user = User.query.filter_by(ID=patient_id).first()
            user = db.session.query(User).filter(User.ID == patient_id).one()
            # user = User.query.filter_by(ID=patient_id).first()
            if user.place_in_queue != 1:
                # demoted_user = User.query.filter_by(place_in_queue=user.place_in_queue - 1).first()
                demoted_user = db.session.query(User) \
                    .filter(User.role == 'patient') \
                    .filter(User.is_approved == 1) \
                    .filter(User.place_in_queue == user.place_in_queue - 1) \
                    .one()
                user.place_in_queue = user.place_in_queue - 1
                demoted_user.place_in_queue = demoted_user.place_in_queue + 1
                db.session.commit()
        elif 'read_file' in request.form.keys():
            file_path = fr'{os.path.dirname(__file__)}\static\{patient_id}.pdf'
            if os.path.isfile(file_path):
                with open(file_path, 'r') as f:
                    return render_template('view_pdf.html',
                                           patient_id=patient_id,
                                           path=fr'static\{patient_id}.pdf')

    #return render_template("patients.html", patients=User.query.all())
    return render_template("patients.html",
          patients=db.session.query(User)
                           .filter(User.role == 'patient')
                           .filter(User.is_approved == 1)
                           .filter(User.place_in_queue > 0)
                           .order_by(db.asc(User.place_in_queue)))

@views.route('/message_for_patient', methods=['GET', 'POST'])
def add_message_for_patient():
    if request.method == 'POST':
        patient_id = request.form['ID']
        message = request.form['message']
        user = db.session.query(User).filter(User.role == 'patient').filter(User.ID == patient_id).first()
        user.message = message
        db.session.commit()
    return render_template("secretary_write_message.html")


@views.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        employee_id = request.form['ID']
        content = request.form['content']
        messages = db.session.query(Chat).all()
        max_id = max(message.message_id for message in messages) if messages else 0
        db.session.add(Chat(message_id=max_id + 1, employee_id=employee_id, content=content))
        db.session.commit()
    messages = db.session.query(Chat).order_by(db.asc(Chat.message_id)).all()[-8:]
    return render_template("chat.html", messages=messages)


@views.route('/patients_for_secretary', methods=['GET', 'POST'])
def patients_for_secretary():
    print("In views.route(patients)")
    if request.method == "POST":
        patient_id = request.form.get("patient_id")
        if "approve" in request.form.keys():
            flash("patient_id = " + patient_id)
            # print("received patient_id=" + patient_id)
            user = User.query.filter_by(ID=patient_id).first()
            # user = User.query.filter_by(ID=patient_id).first()
            approved_users = list(db.session.query(User).filter(User.role == "patient").filter(User.is_approved == 1))
            max_in_queue = max(approved_user.place_in_queue for approved_user in approved_users) if approved_users else 0
            user.place_in_queue = max_in_queue + 1
            user.is_approved = 1
            db.session.commit()
        elif "read_file" in request.form.keys():
            file_path = fr"{os.path.dirname(__file__)}\static\{patient_id}.pdf"
            if os.path.isfile(file_path):
                return render_template("view_pdf.html",
                                       patient_id=patient_id,
                                       path=fr"static\{patient_id}.pdf")


    #return render_template("patients.html", patients=User.query.all())
    return render_template("patiensts_for_secretary.html",
          patients=db.session.query(User).filter(User.role == 'patient')
                           .filter(User.is_approved != 1)
                           .filter(User.message == "")
                           .order_by(db.asc(User.place_in_queue)))

# @views.route('/nurse')
# def nurse():
#     return render_template("nurse.html",n_action=User.query.all())

