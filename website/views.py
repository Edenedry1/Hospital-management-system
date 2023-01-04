from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user

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
        flash("patient_id = "+patient_id)
        print("received patient_id=" + patient_id)
        user = User.query.filter_by(ID=patient_id).first()
        #user = User.query.filter_by(ID=patient_id).first()
        user.place_in_queue = user.place_in_queue - 1
        db.session.commit()


    #return render_template("patients.html", patients=User.query.all())
    return render_template("patients.html",
        patients=db.session.query(User).filter(User.role == 'patient').order_by(db.asc(User.place_in_queue)))


# @views.route('/nurse')
# def nurse():
#     return render_template("nurse.html",n_action=User.query.all())

