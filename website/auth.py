from flask import Blueprint, render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash , check_password_hash
from . import db
from flask_login import login_user , login_required , logout_user , current_user
auth = Blueprint('auth',__name__)

@auth.route('/Login' , methods=['GET' , 'POST'])
def Login():
    if request.method == 'POST':
        ID = request.form.get('ID')
        password = request.form.get('password')

        user = User.query.filter_by(ID = ID).first()
        if user:
            if check_password_hash(user.password , password):
                flash( 'ההתחברות בוצעה בהצלחה!' , category= 'success')
                return redirect(url_for('views.home'))
            else:
                flash( 'סיסמא שגויה' , category='error')
        else:
            flash('תעודת הזהות לא נמצאה במערכת' , category='error')



    return render_template("login.html" , text="צוות רפואי / מטופל")
@auth.route ('/Logout')
def Logout():
    return "<p>Logout</p>"
@auth.route('/Sign_up', methods=['GET' , 'POST'])
def Sign_up():
    if request.method == 'POST':
        choose = request.form.get('choose')
        ID= request.form.get('ID')
        email = request.form.get('email')
        Name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(ID = ID).first()
        if user:
            flash('תעודת הזהות כבר קיימת במערכת' , category='error')

       # if choose != "צוות רפואי" or choose !="מטופל":
        #    flash("הכנס מטופל / צוות רפואי בלבד", category='error')
        elif len(ID) != 9:
            flash("אורך תעודת הזהות צריך להיות בן 9 ספרות", category='error')
        elif len(email) < 4:
            flash("אורך כתובת המייל צריך להיות לפחות 5 ", category='error')
        #elif len(Name) < 2:
         #   flash("נא להכניס שם בעל יותר משתי אותיות", category='error')

        elif password1 != password2:
            flash("הסיסמאות לא זהות", category='error')
        else:
            new_user = User(email=email , Name=Name, password = generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash( "המשתמש נוצר בהצלחה!" , category='secces')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")