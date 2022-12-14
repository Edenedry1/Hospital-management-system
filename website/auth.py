
import logging


from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from os.path import dirname

auth = Blueprint('auth', __name__)


@auth.route('/Login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        role = request.form.get('role')
        ID = request.form.get('ID')
        password = request.form.get('password')
        user = User.query.filter_by(ID=ID).first()
        if user:
            # if check_password_hash(user.password, password):
            #if user.password == password :

            if user.password == password:
                if user.role == 'patient':
                    user.is_active_patient = 1
                    db.session.commit()
                # user.is_active = True
                # user.get_id = ID
                # login_user(user, remember=True)

                # user = User(ID=ID, email=email, password=password1, Name=Name, role=role, question=question)
                #db.session.add(user)
                # db.session.commit()
                if user.is_approved:
                    flash('Logged in successfully! place in queue is {}'.format(user.place_in_queue),
                          category='success')
                # max_place_in_queue = db.session.query(db.func.max(user.place_in_queue)).first()

                # session['user'] = user
                session['user_id'] = user.ID
                session['user_name'] = user.Name
                session['user_role'] = user.role

                # return redirect(url_for('views.home'))
                # return render_template("home.html", user=current_user)
                # return render_template("home.html", user_name=user.Name)
                if user.role == 'nurse':
                    return render_template("nurse.html")
                elif user.role == 'medical secretary':
                    return render_template("medical_secretary.html")
                elif user.role == 'patient':
                    return render_template("patient.html",
                                           user_name=user.Name,
                                           message=user.message or "No new messages")
                # else:
                #     return render_template("home.html", user_name=user.Name, user_role=user.role)
                return render_template("home.html", user_name=user.Name, user_role=user.role)
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('ID does not exist.', category='error')

    # return render_template("login.html", user_name="Guest")
    return render_template("login.html")


# return render_template("login.html", text="Medical staff / patient ")


@auth.route('/Logout')
@login_required
def Logout():
    # logout_user()
    session['user_id'] = 'none'
    session['user_name'] = 'Guest'
    return redirect(url_for('auth.login'))


@auth.route('/Sign_up', methods=['GET', 'POST'])
def Sign_up():
    if request.method == 'POST':
        choose = request.form.get('choose')
        ID = request.form.get('ID')
        email = request.form.get('email')
        Name = request.form.get('Name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        approval = request.form.get('approval')
        role = request.form.get('role')
        answer = request.form.get('answer')
        # if choose != "Medical staff" or choose !="patient":
        #      flash("Enter patient/ medical staff", category='error')
        if len(ID) != 9:
            flash("ID card length should be 9 digits", category='error')

            # elif len(email)<4:
            #     flash("The length of the email address should be at least 5 characters", category='error')
            # elif len(name) < 2:
            #     flash("Enter a name with at least two letters", category='error')
            #
            # elif password1 != password2:
            #     flash("Passwords are not the same", category='error')
        elif approval != 'yes':
            flash("It is not possible to register without approval of the terms of use", category='error')
        else:
            user = User(ID=ID, email=email, password=password1, Name=Name, role=role, answer=answer,
                        is_active_patient=0, is_approved=0, place_in_queue=0)

           # user = User(ID=ID, email=email, password=password1, Name=Name)

            db.session.add(user)
            db.session.commit()
            flash("User created successfully!", category='success')
    return render_template("sign_up.html")


@auth.route('/nurse', methods=['GET', 'POST'])
def Nurse():
    if request.method == 'POST':
        n_action = request.form.get('n_action')
        # db.session.add(user)
        # logging.ERROR('0')
        if n_action == '1':
            # logging.ERROR('1')
            # return render_template("patients.html")
            return redirect(url_for('views.patients'))
        elif n_action == '2':
            return redirect(url_for('views.chat'))
        # flash("home", category='success')
        return render_template("nurse.html")

@auth.route('/Secretary', methods=['GET', 'POST'])
def Secretary():
     if request.method == 'POST':
         s_action = request.form.get('s_action')
         # db.session.add(user)
         # logging.ERROR('0')
         if s_action == '2':
             # logging.ERROR('1')
             #return render_template("patients.html")
             return redirect(url_for('views.patients_for_secretary'))
         elif s_action == '3':
             return redirect(url_for("views.add_message_for_patient"))
         # flash("home", category='success')
         return render_template("medical_secretary.html")

@auth.route('/button')
def button():
    return 'Button pressed!'

@auth.route('/patient', methods=['GET', 'POST'])
def patient():
    user = None
    if request.method == 'POST':
        ID = request.form.get('ID')
        user = User.query.filter_by(ID=ID).one()
        if 'submit' in request.form.keys():
            allergy = request.form.get('allergy')
            reason = request.form.get('reason')
            user = User.query.filter_by(ID=ID).first()
            user.message = ""
            user.allergy = allergy
            user.reason = reason
            user.is_approved = 0
            user.place_in_queue = 0
            db.session.commit()
        elif 'cancel' in request.form.keys():
            user = User.query.filter_by(ID=ID).one()
            user.is_active_patient = 0
            user.is_approved = 0
            user.place_in_queue = 0
            db.session.commit()
        elif 'upload' in request.form.keys():
            user = User.query.filter_by(ID=ID).one()
            user.message = ""
            user.is_approved = 0
            user.place_in_queue = 0
            db.session.commit()
            content = request.files['file'].stream.read()
            if request.files['file'].filename.endswith('.pdf'):
                with open(fr'{dirname(__file__)}\static\{ID}.pdf', 'wb') as f:
                    f.write(content)
        reset_queue()
    return render_template("patient.html",
                           user_name=user.Name if user else None,
                           message=user.message or "No new messages." if user else None)


def reset_queue():
    users = db.session.query(User)\
        .filter(User.role == 'patient')\
        .filter(User.is_approved == 1)\
        .order_by(db.asc(User.place_in_queue))\
        .all()
    counter = 0
    for user in users:
        counter += 1
        user.place_in_queue = counter
    db.session.commit()


@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        patient_id = request.form['ID']
        password = request.form['New password']
        answer = request.form['security qustion']
        user = db.session.query(User)\
            .filter(User.ID == patient_id)\
            .one()
        if user and user.answer == answer:
            user.password = password
            db.session.commit()
            return redirect(url_for('auth.Login'))
        elif not user:
            # Handle wrong ID
            pass
        elif user.answer is None:
            # Handle no answer
            pass
        else:
            # Handle incorrect answer
            pass
    return render_template("forgot_password.html")

