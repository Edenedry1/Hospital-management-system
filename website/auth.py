
import logging


from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user

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

                # user.is_active = True
                # user.get_id = ID
                # login_user(user, remember=True)

                # user = User(ID=ID, email=email, password=password1, Name=Name, role=role, question=question)
                #db.session.add(user)
                # db.session.commit()
                max_place_in_queue = db.session.query(db.func.max(user.place_in_queue)).first()
                flash('Logged in successfully! place in queue = ' + str(max_place_in_queue), category='success')

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
                    return render_template("patient.html")
                # else:
                #     return render_template("home.html", user_name=user.Name, user_role=user.role)
                return render_template("home.html", user_name=user.Name, user_role=user.role)
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

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
        answer =  request.form.get('answer')
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

            user = User(ID=ID, email=email, password=password1, Name=Name,role = role,answer = answer)

           # user = User(ID=ID, email=email, password=password1, Name=Name)

            db.session.add(user)
            db.session.commit()
            flash("User created successfully!", category='success')
    return render_template("sign_up.html")


@auth.route('/nurse', methods=['GET', 'POST'])
def Nurse():
    if request.method == 'POST':
        n_action = request.form.get('n_action')
        user = User(n_action=n_action)
        # db.session.add(user)
        # logging.ERROR('0')
        if user.n_action == '1':
            db.session.commit()
            # logging.ERROR('1')
            # return render_template("patients.html")
            return redirect(url_for('views.patients'))
        # flash("home", category='success')
        return render_template("nurse.html")

@auth.route('/Secretary', methods=['GET', 'POST'])
def Secretary():
     if request.method == 'POST':
         s_action = request.form.get('s_action')
         user = User(s_action=s_action)
         # db.session.add(user)
         # logging.ERROR('0')
         if user.s_action == '2':
             db.session.commit()
             # logging.ERROR('1')
             #return render_template("patients.html")
             return redirect(url_for('views.patients_for_secretary'))
         # flash("home", category='success')
         return render_template("medical_secretary.html")

@auth.route('/button')
def button():
    return 'Button pressed!'

@auth.route('/patient', methods=['GET', 'POST'])
def patient():
    if request.method == 'POST':
        ID = request.form.get('ID')
        allergy = request.form.get('allergy')
        reason = request.form.get('reason')
        user = User.query.filter_by(ID=ID).first()
        user.allergy = allergy
        db.session.commit()
        user.reason = reason
        db.session.commit()
    return render_template("patient.html")


