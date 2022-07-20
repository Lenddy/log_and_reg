from flask import flash, redirect, render_template, request, session
from flask_app import app
from flask_app.models.registration_model import Registration
from flask_bcrypt import Bcrypt
#setting a variable for the =Bcrypt
#to get it to work you need to import Bcrypt
bcrypt = Bcrypt(app)


# registration page
@app.route("/")
def show_reg():
    return render_template("log_and_reg.html")


#registration form 
#validates creation of a user
#encrypts the password
@app.route("/", methods = ["post"])
def create_user():
    print(request.form)
    if not Registration.validate(request.form):
        return redirect("/")
    data = {
        **request.form,
        "password": bcrypt.generate_password_hash(request.form["password"])
    }
    session["id"]= Registration.add_one(data)
    return redirect("/dashboard")


#login form
#checks that the email and the password match in the database  
#checks for the password hash encryptions
#stores the id in session
@app.route("/log_in",methods = ["post"])
def log_in():
    data = {
        "email": request.form["email"]
    }
    user = Registration.get_by_email(data)
    if not user:
        flash("Invalid Email/Password","match")
        print("user")
        return redirect("/")
    if not bcrypt.check_password_hash(user.password,request.form["password"]):
        flash("Invalid Email/Password","match")
        print("password")
        return redirect("/")
    session["id"]=user.id
    return redirect("/dashboard")


# renders dashboard page
# redirect to the login page if user try to go to the dashboard using the url
@app.route("/dashboard")
def log_in_form():
    if "id" not in session:
        return redirect("/")
    user = Registration.get_by_id({"id": session["id"]})
    return render_template("user_home_page.html",user = user)


#erase session and logs user out
@app.route("/log_out")
def log_out():
    session.pop("id")
    return redirect("/")