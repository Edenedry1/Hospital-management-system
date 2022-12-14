from flask import Blueprint, render_template,request,flash,redirect
# from .models import User
# from . import db
from flask_login import login_user, login_required, logout_user,current_user
auth = Blueprint('auth',__name__)

@auth.route('/Login' , methods=['GET' , 'POST'])
def Login():
    return render_template("login.html" , text="Medical staff / patient ")
@auth.route ('/Logout')
@login_required
def Logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/Sign_up', methods=['GET' , 'POST'])
def Sign_up():

    if request.method == 'POST':
        choose = request.form.get('choose')
        ID = request.form.get('ID')
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
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

        else:
            flash( "User created successfully!" , category='secces')
    return render_template("sign_up.html")