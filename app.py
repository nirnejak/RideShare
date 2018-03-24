from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import session
from flask import logging
from passlib.hash import sha256_crypt

from flask_mysqldb import MySQL

import os

# Import from own library
from decorators import is_logged_in
from decorators import is_not_logged_in

# Importing Forms
from forms import RegisterForm

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'RideShare'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MYSQL
mysql = MySQL(app)

# Index
@app.route('/')
def index():
	return render_template('home.html')

# Terms
@app.route('/about')
def about():
	return render_template('about.html')

# User Register
@app.route('/register', methods=['GET','POST'])
@is_not_logged_in
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		# User General Details
		fname = form.fname.data
		lname = form.lname.data
		contactNo = form.contactNo.data
		alternateContactNo = form.alternateContactNo.data
		email = form.email.data
		password = sha256_crypt.encrypt(str(form.password.data))

		# User Address
		addLine1 = form.addLine1.data
		addLine2 = form.addLine2.data
		colony = form.colony.data
		city = form.city.data
		state = form.state.data

		# Create cursor
		cur = mysql.connection.cursor()

		# Add User into Database
		cur.execute("INSERT INTO users(fname, lname, contactNo, alternateContactNo, email, password, addLine1, addLine2, colony, city, state) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (fname, lname, contactNo, alternateContactNo, email, password, addLine1, addLine2, colony, city, state))

		# Comit to DB
		mysql.connection.commit()

		# Close connection
		cur.close()

		flash('You are now Registered and can Log In','success')
		return redirect(url_for('login'))

	return render_template('register.html', form = form)

# User login
@app.route('/login', methods=['GET','POST'])
@is_not_logged_in
def login():
	if request.method == 'POST':
		# Get Form Fields
		username = request.form['username']
		password_candidate = request.form['password']

		# Create cursor
		cur = mysql.connection.cursor()

		# Get user by either Email or ContactNo
		if '@' in username:
			result = cur.execute("SELECT userId, password, userStatus, userType, fname, lname, city FROM USERS WHERE email = %s",[username])
		else:
			result = cur.execute("SELECT userId, password, userStatus, userType, fname, lname, city FROM USERS WHERE contactNo = %s",[username])

		if result>0:
			# Get stored hash
			data = cur.fetchone()
			password = data['password']
			userId = data['userId']
			userStatus = data['userStatus']
			userType = data['userType']
			city = data['city']

			# Compate Passwords
			if sha256_crypt.verify(password_candidate, password):
				session['logged_in'] = True
				session['userId'] = userId
				session['userStatus'] = userStatus
				session['userType'] = userType
				session['city'] = city
				
				msg = "Welcome {} {}".format(data['fname'],data['lname'])
				flash(msg,'success')

				return redirect(url_for('dashboard'))
			else:
				error = "Invalid login"
				return render_template('login.html', error = error)
			# Close connection
		else:
			error = "Username not found"
			return render_template('login.html', error = error)
	return render_template('login.html')

# Logout
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You are now Logged Out','success')
	return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
	return render_template('dashboard.html')




# this part of code was buggy so some parts are removed

@app.route('/nearbyRides', methods=['GET','POST'])
@is_logged_in
def nearbyRides():
	if request.method == 'POST':
		RideId = request.form['rideId']

		# Create cursor
		cur = mysql.connection.cursor()

		# Add User into Database
		cur.execute("INSERT INTO ShareRequest(RideID, requestUserId) VALUES (%s, %s)", (RideId, session['userId']))

		# Comit to DB
		mysql.connection.commit()

		# Close connection
		cur.close()

		
		flash('Your Request for Ride is sent to the user!','warning')
		return redirect(url_for('dashboard'))
	
	# Create cursor
	cur = mysql.connection.cursor()

	# Add User into Database
	result = cur.execute("SELECT * FROM ride WHERE rideDate = DATE(NOW()) and city = %s and rideStatus = %s",(session['city'],"PENDING"))

	rides = cur.fetchall()

	# Comit to DB
	mysql.connection.commit()

	# Close connection
	cur.close()

	if result>0:
		return render_template('nearbyRides.html',rides = rides)
	else:
		flash('No Rides in your city!','warning')
		return redirect(url_for('dashboard'))

@app.route('/rideRequests', methods=['GET','POST'])
@is_logged_in
def rideRequests():
	if request.method == 'POST':
		pass

	# Create cursor
	cur = mysql.connection.cursor()

	# Add User into Database

	result = cur.execute("SELECT * FROM ShareRequest")

	rideRequests = cur.fetchall()

	# Comit to DB
	mysql.connection.commit()

	# Close connection
	cur.close()

	if result>0:
		return render_template('rideRequests.html', rideRequests = rideRequests)
	else:
		flash('No Requests for Your Ride!','warning')
		return redirect(url_for('dashboard'))

    return render_template('rideRequests.html')


@app.route('/shareRide', methods=['GET','POST'])
@is_logged_in
def shareRide():
	if request.method == 'POST':
		rideDate = request.form['rideDate']
		rideTime = request.form['rideTime']
		fromLocation = request.form['fromLocation']
		toLocation = request.form['toLocation']
		city = request.form['city']
		state = request.form['state']

		# Create cursor
		cur = mysql.connection.cursor()

		# Add User into Database
		cur.execute("INSERT INTO Ride(creatorUserId, rideDate, rideTime, fromLocation, toLocation, city, state) VALUES (%s, %s, %s, %s, %s, %s,%s)", (session['userId'], rideDate, rideTime, fromLocation, toLocation, city, state))

		# Comit to DB
		mysql.connection.commit()

		# Close connection
		cur.close()

		flash('Your ride is shared people around you can now send you request for your ride','success')
		return redirect(url_for('dashboard'))
	return render_template('shareRide.html')


if __name__ == '__main__':
	app.secret_key = 'secret123'
	port = int(os.environ.get("PORT",7070))
	app.run(host='0.0.0.0', port=port, debug=True)