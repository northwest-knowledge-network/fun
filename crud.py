#
# NKN Flask demo
#

# import some python libraries
import os
from flask import Flask
from flask import flash, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy


# create the Flask app object
app = Flask(__name__)

# set some app configs
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://crud:cruduser@localhost/crud"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///crud.sqlite3"
app.secret_key = "kjfhfiuhf8883773"

# instantiate the SQLAlchemy database
db = SQLAlchemy(app)

# define the data model
class Book(db.Model):
	title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

	def __repr__(self):
		return "<Title: {}>".format(self.title)

#
# ROUTES
#

#  home page
@app.route("/", methods=["GET", "POST"])
def home():

	if(session.get('logged_in')):
		print("In home()  Session logged in")
	else:
		print("In home()  Session logged out")

	if request.form:
		book = Book(title=request.form.get("title"))
		db.session.add(book)
		db.session.commit()

	books = Book.query.all()

	return render_template("home.html", books=books, authed=session.get('logged_in'))



# handle login
@app.route('/login', methods=['POST'])
def do_admin_login():
	print("IN do_admin_login()")
	if request.form['password'] == '123' and request.form['username'] == 'admin':
		session['logged_in'] = True
		session.modified = True
		print("logged_in == True")
	else:
		flash('wrong password!')
		print("wrong password!")
	return redirect("/")


# handle logout
@app.route('/logout', methods=['POST'])
def do_admin_logout():
	print("IN do_admin_logout()")
	session['logged_in'] = False
	return redirect("/")


# process updates to records
@app.route("/update", methods=["POST"])
def update():
	newtitle = request.form.get("newtitle")
	oldtitle = request.form.get("oldtitle")
	book = Book.query.filter_by(title=oldtitle).first()
	book.title = newtitle
	db.session.commit()
	return redirect("/")



# process record deletions
@app.route("/delete", methods=["POST"])
def delete():
	title = request.form.get("title")
	book = Book.query.filter_by(title=title).first()
	db.session.delete(book)
	db.session.commit()
	return redirect("/")


if __name__ == '__main__':
	app.run(port=8009, debug=True)

