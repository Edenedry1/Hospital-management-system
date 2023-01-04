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
        flash("patient_id = " + patient_id)
        # print("received patient_id=" + patient_id)
        user = User.query.filter_by(ID=patient_id).first()
        # user = User.query.filter_by(ID=patient_id).first()
        if user.place_in_queue != 1:
            demoted_user = User.query.filter_by(place_in_queue=user.place_in_queue - 1).first()
            user.place_in_queue = user.place_in_queue - 1
            demoted_user.place_in_queue = demoted_user.place_in_queue + 1
            db.session.commit()

    #return render_template("patients.html", patients=User.query.all())
    return render_template("patients.html",
          patients=db.session.query(User)
                           .filter(User.role == 'patient')
                           .filter(User.is_approved == 1)
                           .filter(User.place_in_queue > 0)
                           .order_by(db.asc(User.place_in_queue)))

@views.route('/patients_for_secretary', methods=['GET', 'POST'])
def patients_for_secretary():
    print("In views.route(patients)")
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        flash("patient_id = " + patient_id)
        # print("received patient_id=" + patient_id)
        user = User.query.filter_by(ID=patient_id).first()
        # user = User.query.filter_by(ID=patient_id).first()
        approved_users = list(db.session.query(User).filter(User.role == 'patient').filter(User.is_approved == 1))
        max_in_queue = max(approved_user.place_in_queue for approved_user in approved_users) if approved_users else 0
        user.place_in_queue = max_in_queue + 1
        user.is_approved = 1
        db.session.commit()

    #return render_template("patients.html", patients=User.query.all())
    return render_template("patiensts_for_secretary.html",
          patients=db.session.query(User).filter(User.role == 'patient')
                           .filter(User.is_approved != 1)
                           .order_by(db.asc(User.place_in_queue)))

# @views.route('/nurse')
# def nurse():
#     return render_template("nurse.html",n_action=User.query.all())

