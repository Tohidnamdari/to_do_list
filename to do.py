from flask import Flask,render_template,request,redirect,make_response,flash
from database import db
from database import app
from database import Users
from database import acant
import datetime
db.create_all()
@app.route("/st",methods=['POST','GET'])
def st():
    return render_template('panel.html',name=request.cookies.get("userr"),found=True,items=len(Users.query.all()),subject=Users.query.all())
@app.route("/panel",methods=['POST','GET'])
def panel():
    if request.cookies.get("userr"):
        return render_template('panel.html',found=False,name=request.cookies.get("userr"))

    else:
        return redirect('/login')
@app.route("/add",methods=['POST','GET'])
def add():
    if request.cookies.get("userr"):
        if request.method=='POST':
            subject = request.form.get('subject')
            date = request.form.get('date')
            time = request.form.get('time')
            flash("add to do list", "primary")
            x = datetime.datetime.now()
            admin=Users(subject=subject,time=time,date=date,t=x.strftime("%c"))
            db.session.add(admin)
            db.session.commit()
        return render_template('add.html',use=request.cookies.get("userr"))
    else:
        return redirect('/login')
@app.route("/",methods=['POST','GET'])
def home():
    return render_template('index.html',check=request.cookies.get("userr"))
@app.route("/delete",methods=['POST','GET'])
def delete():
    if request.cookies.get("userr"):
         user=Users.query.filter_by().first()
         db.session.delete(user)
         db.session.commit()
         return redirect("/")
    else:
        return redirect('/login')
@app.route("/logout")
def logout():
    flash("user log out","danger")
    response = make_response(redirect('/login'))
    response.delete_cookie("userr")
    return response
@app.route('/login',methods=['GET','POST'])
def login():
    result=''
    user=''
    pas=''
    if request.method=='POST':
        user = request.form.get('user')
        pas = request.form.get('pas')
        found=False
        for u in range(len(acant.query.all())):
            print(user,"-",acant.query.all()[u].username,",",pas,"-",acant.query.all()[u].password)
            if user==acant.query.all()[u].username and pas==acant.query.all()[u].password:
                flash("user login","success")
                response=make_response(redirect('/panel'))
                response.set_cookie("userr",user)
                found = True
                return response
        if found==False:
                flash("user or pass wrong", "danger")
                return render_template('login.html', result=result)
    return render_template('login.html')
@app.route('/Register',methods=['POST','GET'])
def Register():
    user_name=''
    password=''
    re_password = ''
    if request.method=='POST':
        user_name1 = request.form.get('user')
        password1 = request.form.get('pas')
        re_password = request.form.get('pass')
        if password1==re_password:
            admin1=acant(username=user_name1,password=password1)
            db.session.add(admin1)
            db.session.commit()
            flash("user Register","success")
            return redirect('/add')
        else:
            flash("password or re_password wrong","danger")
            return render_template('Register.html')
    else:
        return render_template('Register.html')
if __name__=='__main__':
    app.run()
