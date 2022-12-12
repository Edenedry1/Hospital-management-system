from flask import Blueprint, render_template,request,flash
auth = Blueprint('auth',__name__)

@auth.route('/Login' , methods=['GET' , 'POST'])
def Login():
    return render_template("login.html" , text="צוות רפואי / מטופל")
@auth.route ('/Logout')
def Logout():
    return "<p>Logout</p>"
@auth.route('/Sign_up', methods=['GET' , 'POST'])
def Sign_up():
    if request.method == 'POST':
        choose = request.form.get('choose')
        ID = request.form.get('ID')
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if choose != "צוות רפואי" or choose !="מטופל":
            flash("הכנס מטופל / צוות רפואי בלבד", category='error')
        elif len(ID) != 9:
            flash("אורך תעודת הזהות צריך להיות בן 9 ספרות", category='error')

        elif len(email)<4:
            flash("אורך כתובת המייל צריך להיות לפחות 5 ", category='error')
        elif len(name) < 2:
            flash("נא להכניס שם בעל יותר משתי אותיות", category='error')

        elif password1 != password2:
            flash("הסיסמאות לא זהות", category='error')

        else:
            flash( "המשתמש נוצר בהצלחה!" , category='secces')
    return render_template("sign_up.html")