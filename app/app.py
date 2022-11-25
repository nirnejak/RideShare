from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import session
from flask import logging
from passlib.hash import sha256_crypt

import psycopg2 as pg2

import os, sys, time

# Import from own library
from decorators import is_logged_in
from decorators import is_not_logged_in
from decorators import has_aadhar
from decorators import has_driving

# Importing Forms
from forms import RegisterForm

# Importing database credentials
from database_credentials import credentials

app = Flask(__name__)
app.config['SECRET_KEY'] = "747b60ab7ef6e02cf56da6503adae95198fa6dad"

# conn = pg2.connect(
# 	database = credentials['database'],
# 	user = credentials['user'],
# 	password = credentials['password'],
# 	host = credentials['host'],
# 	port = credentials['port']
# )

print(f'\n\n\nTrying to connect to {os.environ.get("POSTGRES_HOST")}', file=sys.stderr)
print(f'User: {os.environ.get("POSTGRES_USER")}', file=sys.stderr)
print(f'Password: {os.environ.get("POSTGRES_PASSWORD")}', file=sys.stderr)
print(f'Port: {os.environ.get("POSTGRES_PORT")}', file=sys.stderr)
print('')

startup_duration = 0
timeout_s = 30
start_time = time.time()
last_exception = None
conn = None

while (startup_duration < timeout_s):
	try:
		startup_duration = time.time() - start_time
		conn = pg2.connect(
			database = os.environ.get('POSTGRES_DB'),
			user = os.environ.get('POSTGRES_USER'),
			password = os.environ.get('POSTGRES_PASSWORD'),
			host = os.environ.get('POSTGRES_HOST'),
			port = os.environ.get('POSTGRES_PORT')
		)
		break
	except Exception as e:
		print(f'Elapsed: {int(startup_duration)} / {timeout_s} seconds')
		last_exception = e
		time.sleep(1)
if conn is None:
	print(f'Could not connect to the database within {timeout_s} seconds - {last_exception}')
	exit()

connection_status = ('Not connected', 'Connected')[conn.closed == 0]
print(f'Connection status: {connection_status}\n\n', file=sys.stderr, flush=True)

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
		alternateContactNo = ""
		emailID = form.emailID.data
		gender = str(form.gender.data).upper()
		driving = form.driving.data
		aadhar = form.aadhar.data
		password = sha256_crypt.encrypt(str(form.password.data))

		# User Address
		addLine1 = form.addLine1.data
		addLine2 = form.addLine2.data
		colony = ""
		city = form.city.data
		state = form.state.data

		# Create cursor
		cur = conn.cursor()

		try:
			if len(aadhar)==0 and len(driving)==0:
				# Add User into Database
				cur.execute("INSERT INTO users(fname, lname, contactNo, alternateContactNo, email, password, addLine1, addLine2, colony, city, state, gender, userStatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (fname, lname, contactNo, alternateContactNo, emailID, password, addLine1, addLine2, colony, city, state, gender, "NONE"))
			elif len(aadhar)!=0 and len(driving)==0:
				# Add User into Database
				cur.execute("INSERT INTO users(fname, lname, contactNo, alternateContactNo, email, password, addLine1, addLine2, colony, city, state, aadhar, gender, userStatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (fname, lname, contactNo, alternateContactNo, emailID, password, addLine1, addLine2, colony, city, state, aadhar, gender, "AADHAR"))
			elif len(aadhar)==0 and len(driving)!=0:
				# Add User into Database
				cur.execute("INSERT INTO users(fname, lname, contactNo, alternateContactNo, email, password, addLine1, addLine2, colony, city, state, gender, driving, userStatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (fname, lname, contactNo, alternateContactNo, emailID, password, addLine1, addLine2, colony, city, state, gender, driving,"DRIVING"))
			elif len(aadhar)!=0 and len(driving)!=0:
				# Add User into Database
				cur.execute("INSERT INTO users(fname, lname, contactNo, alternateContactNo, email, password, addLine1, addLine2, colony, city, state, aadhar, gender, driving, userStatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (fname, lname, contactNo, alternateContactNo, emailID, password, addLine1, addLine2, colony, city, state, aadhar, gender, driving,"BOTH"))
		except:
			conn.rollback()
			flash('Something went wrong','danger')
			return redirect(url_for('login'))

		# Comit to DB
		conn.commit()

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
		cur = conn.cursor()

		try:
			# Get user by either Email or ContactNo
			if '@' in username:
				cur.execute("SELECT userId, password, userStatus, userType, fname, lname, city FROM users WHERE email = %s",[username])
			else:
				cur.execute("SELECT userId, password, userStatus, userType, fname, lname, city FROM users WHERE contactNo = %s",[username])
		except:
			conn.rollback()
			flash('Something went wrong','danger')
			return redirect(url_for('login'))

		result = cur.fetchone()

		if result:
			# Compate Passwords
			if sha256_crypt.verify(password_candidate, result[1]):
				session['logged_in'] = True
				session['userId'] = result[0]
				session['userStatus'] = result[2]
				session['userType'] = result[3]
				session['city'] = result[6]
				
				msg = "Welcome {} {}".format(result[4],result[5])
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
@has_aadhar
def nearbyRides():
	if request.method == 'POST':
		if session['userStatus']=='REGISTERED' or session['userStatus'] == 'DRIVING' or session['userStatus'] == 'NONE':
			flash('You Don\'t have PID!','warning')
			return redirect(url_for('dashboard'))
		
		RideId = request.form['rideId']

		# Create cursor
		cur = conn.cursor()

		try:
			# Add User into Database
			cur.execute("INSERT INTO ShareRequest(RideID, requestUserId) VALUES (%s, %s);", (RideId, session['userId']))
		except:
			conn.rollback()
			flash('Something went wrong','danger')
			return redirect(url_for('dashboard'))

		# Comit to DB
		conn.commit()

		# Close connection
		cur.close()

		
		flash('Your Request for Ride is sent to the user!','success')
		return redirect(url_for('dashboard'))
	

	if session['userStatus']=='REGISTERED' or session['userStatus'] == 'DRIVING' or session['userStatus'] == 'NONE':
		flash('You Don\'t have PID!','warning')
		return redirect(url_for('dashboard'))

	# Create cursor
	cur = conn.cursor()
	print(session['userId'], file=sys.stderr)
	ui=session['userId']
	try:
		# Add User into Database
		# query_original = "SELECT * FROM Ride r, users u WHERE r.rideDate = DATE(NOW()) AND r.city = %s AND r.rideStatus = %s AND r.creatorUserId = u.userId",(session['city'],"PENDING")
		#query = "select * from (SELECT ridetime, fromlocation, tolocation, r.city, r.state, fname, lname, gender, seats, contactno, rideid, r.creatoruserid, u.userid  FROM users u, ride r where u.userid=r.creatoruserid and r.ridestatus='PENDING') as A where A.userid not in (%s);"(ui)
		cur.execute("select * from (SELECT ridetime, fromlocation, tolocation, r.city, r.state, fname, lname, gender, seats, contactno, rideid, r.creatoruserid, u.userid, r.carstatus, r.message, ridedate  FROM users u, ride r where u.userid=r.creatoruserid and r.ridestatus='PENDING') as A where A.userid != %s",[ui])
	except:
		conn.rollback()
		flash('Something went wrong','danger')
		return redirect(url_for('dashboard'))
	
	rides = cur.fetchall()

	# Comit to DB
	conn.commit()

	# Close connection
	cur.close()

	if rides:
		return render_template('nearbyRides.html', rides = rides)
	else:
		flash('No Rides in your city!','warning')
		return redirect(url_for('dashboard'))

@app.route('/womennearbyRides', methods=['GET','POST'])
@is_logged_in
@has_aadhar
def womennearbyRides():
	if request.method == 'POST':
		if session['userStatus']=='REGISTERED' or session['userStatus'] == 'DRIVING' or session['userStatus'] == 'NONE':
			flash('You Don\'t have PID!','warning')
			return redirect(url_for('dashboard'))
		
		RideId = request.form['rideId']

		# Create cursor
		cur = conn.cursor()

		try:
			# Add User into Database
			cur.execute("INSERT INTO ShareRequest(RideID, requestUserId) VALUES (%s, %s);", (RideId, session['userId']))
		except:
			conn.rollback()
			flash('Something went wrong','danger')
			return redirect(url_for('dashboard'))

		# Comit to DB
		conn.commit()

		# Close connection
		cur.close()

		
		flash('Your Request for Ride is sent to the user!','success')
		return redirect(url_for('dashboard'))
	

	if session['userStatus']=='REGISTERED' or session['userStatus'] == 'DRIVING' or session['userStatus'] == 'NONE':
		flash('You Don\'t have PID!','warning')
		return redirect(url_for('dashboard'))

	# Create cursor
	cur = conn.cursor()
	ui = session['userId']
	try:
		# Add User into Database
		# query_original = "SELECT * FROM Ride r, users u WHERE r.rideDate = DATE(NOW()) AND r.city = %s AND r.rideStatus = %s AND r.creatorUserId = u.userId",(session['city'],"PENDING")
		#query = "SELECT * FROM Ride r, users u where u.gender = 'FEMALE' and r.creatoruserid != u.userid"
		cur.execute("select * from (SELECT ridetime, fromlocation, tolocation, r.city, r.state, fname, lname, gender, seats, contactno, rideid, r.creatoruserid, u.userid, ridedate  FROM users u, ride r where gender = 'FEMALE' and u.userid=r.creatoruserid and r.ridestatus='PENDING') as A where A.userid != %s",[ui])
	except:
		conn.rollback()
		flash('Something went wrong','danger')
		return redirect(url_for('dashboard'))
	
	rides = cur.fetchall()

	# Comit to DB
	conn.commit()

	# Close connection
	cur.close()

	if rides:
		return render_template('womennearbyRides.html', rides = rides)
	else:
		flash('No Rides in your city with women drivers!','warning')
		return redirect(url_for('dashboard'))



@app.route('/rideRequests', methods=['GET','POST'])
@is_logged_in
@has_driving
def rideRequests():
	if request.method == 'POST':
		if session['userStatus']=='REGISTERED' or session['userStatus'] == 'AADHAR' or session['userStatus'] == 'NONE':
			flash('You Don\'t have Driving License!','warning')
			return redirect(url_for('dashboard'))
		
		rideId = request.form['rideId']
		
		# Create cursor
		cur = conn.cursor()

		
		try:
			# fetching no of seats
			cur.execute("select seats from Ride where RideId = %s",[rideId])
		except:
			conn.rollback()
			flash('Something went wrong','danger')
			return redirect(url_for('dashboard'))

		s = cur.fetchone()
		seats = s[0]
		cur.close()

		cur = conn.cursor()
       
		
		try:
			# fetching the request creater ID
			cur.execute("select requestuserid from sharerequest s,ride r where s.rideid=r.rideid")
		except:
			conn.rollback()
			flash('Something went wrong','danger')
			return redirect(url_for('dashboard'))

		requestUser= cur.fetchall()
		requestUserIds=requestUser
		

	
		
		print(rideId,file=sys.stderr)
		print(session['userId'],file=sys.stderr)
		print(requestUserIds,file=sys.stderr)
		if seats - 1 > 0:
			try:
				# Update User Details into the Database
				cur.execute("UPDATE Ride SET seats = %s",[seats-1])



				for requestUserId in requestUserIds:
					cur.execute("INSERT INTO passenger(rideid, creatoruserid, requestuserid) VALUES (%s,%s,%s);", (rideId, session['userId'] ,requestUserIds[0]))
					cur.execute("delete from sharerequest s where s.requestUserId in (select s.requestUserId from sharerequest s,passenger p where s.requestUserId=p.requestUserId )")
			except:
				conn.rollback()
				flash('Something went wrong','danger')
				return redirect(url_for('dashboard'))
		else:
			try:
				# Update User Details into the Database
				cur.execute("UPDATE Ride SET seats = %s,rideStatus = 'DONE'",[seats-1])
				for requestUserId in requestUserIds:
					cur.execute("INSERT INTO passenger(rideid, creatoruserid, requestuserid) VALUES (%s,%s,%s);", (rideId, session['userId'] ,requestUserId[0]))
					cur.execute("delete from sharerequest s where s.requestUserId in (select s.requestUserId from sharerequest s,passenger p where s.requestUserId=p.requestUserId )")
			except:
				conn.rollback()
				flash('Something went wrong','danger')
				return redirect(url_for('dashboard'))

		# Comit to DB
		conn.commit()

		# Close connection
		cur.close()

		flash('Request accepted for the ride','success')
		return redirect(url_for('dashboard'))

	if session['userStatus']=='REGISTERED' or session['userStatus'] == 'AADHAR' or session['userStatus'] == 'NONE':
			flash('You Don\'t have Driving License!','warning')
			return redirect(url_for('dashboard'))

	# Create cursor
	cur = conn.cursor()

	try:
		# Fetch all the ShareRequests and Details
		cur.execute("SELECT ridetime, fromlocation, tolocation, r.city, r.state, fname, lname, gender, seats, contactno, r.rideid, r.creatoruserid, u.userid, ridedate  FROM ShareRequest s, Ride r, users u WHERE r.RideId = s.RideID AND r.rideStatus = 'PENDING' AND r.creatorUserId = %s AND s.requestUserId = u.userId",[session['userId']])
	except:
		conn.rollback()
		flash('Something went wrong','danger')
		return redirect(url_for('dashboard'))

	rideRequests = cur.fetchall()

	# Comit to DB
	conn.commit()

	# Close connection
	cur.close()

	if rideRequests:
		return render_template('rideRequests.html', rideRequests = rideRequests)
	else:
		flash('No Requests for Your Ride!','warning')
		return redirect(url_for('dashboard'))

	return render_template('rideRequests.html')

@app.route('/acceptedRides', methods=['GET','POST'])
@is_logged_in
@has_driving
def acceptedRides():
	if request.method == 'POST':
		if session['userStatus']=='REGISTERED' or session['userStatus'] == 'AADHAR' or session['userStatus'] == 'NONE':
			flash('You Don\'t have Driving License!','warning')
			return redirect(url_for('dashboard'))
		
		rideId = request.form['rideId']
		
		# Create cursor
		cur = conn.cursor()

		
		if session['userStatus']=='REGISTERED' or session['userStatus'] == 'AADHAR' or session['userStatus'] == 'NONE':
				flash('You Don\'t have Driving License!','warning')
				return redirect(url_for('dashboard'))

	# Create cursor
	cur = conn.cursor()

	try:
		# Fetch all the ShareRequests and Details
		#cur.execute("SELECT * FROM passenger p, ride r, users u WHERE r.RideId = p.rideid AND p.creatoruserid = %s AND p.requestUserId = u.userId",[session['userId']])
		cur.execute("SELECT DISTINCT r.ridedate, r.ridetime,r.fromlocation, r.tolocation, r.city, r.state,  u.fname, u.lname, u.gender, u.contactno, p.rideid FROM passenger p, ride r, users u WHERE r.RideId = p.rideid AND p.creatoruserid = %s AND p.requestUserId = u.userId",[session['userId']])

	except:
		conn.rollback()
		flash('Something went wrong','danger')
		return redirect(url_for('dashboard'))

	acceptedRides = cur.fetchall()

	# Comit to DB
	conn.commit()

	# Close connection
	cur.close()

	if rideRequests:
		return render_template('acceptedRides.html', acceptedRides = acceptedRides)
	else:
		flash('No Passengers for Your Ride!','warning')
		return redirect(url_for('dashboard'))

	return render_template('accepetedRides.html')




@app.route('/shareRide', methods=['GET','POST'])
@is_logged_in
@has_driving
def shareRide():
	if request.method == 'POST':
		if session['userStatus']=='REGISTERED' or session['userStatus'] == 'AADHAR' or session['userStatus'] == 'NONE':
			flash('You Don\'t have Driving License!','warning')
			return redirect(url_for('dashboard'))

		rideDate = request.form['rideDate']	
		rideTime = request.form['rideTime']
		fromLocation = request.form['fromLocation']
		toLocation = request.form['toLocation']
		seats = request.form['seats']			
		city = request.form['city']
		state = request.form['state']
		carStatus = request.form['carState']
		message = request.form['message']

		# Create cursor
		cur = conn.cursor()

		try:
			# Add Ride into the Database
			cur.execute("INSERT INTO Ride(creatorUserId, rideDate, rideTime, fromLocation, toLocation, seats, city, state,carStatus,message) VALUES (%s,%s, %s, %s, %s, %s, %s,%s,%s,%s)", (session['userId'], rideDate, rideTime, fromLocation, toLocation, seats, city, state,carStatus,message))
		except:
			conn.rollback()
			flash('Something went wrong','danger')
			return redirect(url_for('dashboard'))

		# Comit to DB
		conn.commit()

		# Close connection
		cur.close()

		flash('Your ride is shared people around you can now send you request for your ride','success')
		return redirect(url_for('dashboard'))
	
	if session['userStatus']=='REGISTERED' or session['userStatus'] == 'AADHAR' or session['userStatus'] == 'NONE':
		flash('You Don\'t have Driving License!','warning')
		return redirect(url_for('dashboard'))
	return render_template('shareRide.html')


@app.route('/settings', methods=['GET','POST'])
@is_logged_in
def settings():
	if request.method == 'POST':
		contactNo = request.form['contactNo']
		alternateContactNo = ""
		email = request.form['email']
		gender = request.form['gender']
		driving = request.form['driving']
		aadharID = request.form['aadharID']
		addLine1 = request.form['addLine1']
		addLine2 = request.form['addLine2']
		colony = ""
		city = request.form['city']
		state = request.form['state']


		if len(aadharID)==0 and len(driving)==0:
			userStatus = "NONE"
		elif len(aadharID)!=0 and len(driving)==0:
			userStatus = "AADHAR"
		elif len(aadharID)==0 and len(driving)!=0:
			userStatus = "DRIVING"
		elif len(aadharID)!=0 and len(driving)!=0:
			userStatus = "BOTH"

		# Create cursor
		cur = conn.cursor()

		try:
			# Update User Details into the Database
			cur.execute("UPDATE users SET contactNo=%s, alternateContactNo=%s, email=%s, gender = %s, driving=%s, aadhar=%s, addLine1=%s, addLine2= %s, colony= %s, city=%s, state = %s, userStatus = %s WHERE userId = %s",(contactNo, alternateContactNo, email, gender, driving, aadharID, addLine1, addLine2, colony, city, state, userStatus, session['userId']))
		except:
			conn.rollback()
			flash('Something went wrong','danger')
			return redirect(url_for('dashboard'))

		session['userStatus'] = userStatus

		# Comit to DB
		conn.commit()

		# Close connection
		cur.close()


		flash('Profile Updated Successfully','success')
		return redirect(url_for('dashboard'))

	# Create cursor
	cur = conn.cursor()

	try:
		# Fetch User Details from the Database
		cur.execute("SELECT * FROM users WHERE userId = %s", [session['userId']])
	except:
		conn.rollback()
		flash('Something went wrong','danger')
		return redirect(url_for('dashboard'))

	userData = cur.fetchone()

	# Close connection
	cur.close()

	if userData:
		return render_template('settings.html', userData = userData)
	else:
		return "Something went wrong"

if __name__ == '__main__':
	app.secret_key = 'secret123'
	port = int(os.environ.get("PORT",7070))
	app.run(host='0.0.0.0', port=port, debug=True)