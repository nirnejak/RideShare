from flask import url_for
from flask import flash
from flask import session
from flask import redirect
from functools import wraps

# Check if user is not logged in
def is_not_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if not('logged_in' in session):
			return f(*args, **kwargs)
		else:
			flash('You are already Logged In','warning')
			return redirect(url_for('dashboard'))
	return wrap

# Check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, Please Login','danger')
			return redirect(url_for('login'))
	return wrap

# Check if user has aadhar ID
def has_aadhar(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['userStatus'] in ['BOTH','AADHAR']:
			return f(*args, **kwargs)
		else:
			flash('You Don\'t have PID. Update PID Details goto <a href=\"/settings\">Settings</a>.','warning')
			return redirect(url_for('dashboard'))
	return wrap

# Check if user has driving license
def has_driving(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['userStatus'] in ['BOTH','DRIVING']:
			return f(*args, **kwargs)
		else:
			flash('You Don\'t have Driving License. Update Driving License Details goto <a href=\"/settings\">Settings</a>.','warning')
			return redirect(url_for('dashoard'))
	return wrap