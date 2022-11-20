from wtforms import Form, StringField, IntegerField, TextAreaField, PasswordField, SelectField,	 validators

# Register Form Class
class RegisterForm(Form):
	fname = StringField('First Name', [validators.Length(min = 1, max = 50)], description='First Name')
	lname = StringField('Last Name', [validators.Length(min = 1, max = 50)], description='Last Name')
	gender = SelectField('Gender', choices=[('MALE', 'Male'), ('FEMALE', 'Female')], description='Gender')
	driving = StringField('Driving License No', description='Driving License No.')
	aadhar = StringField('PID', description='PID')
	contactNo = StringField('Contact Number', [validators.Length(min = 1, max = 15)], description='Contact No')
	emailID = StringField('Email', [validators.Length(min = 0, max = 50)], description='Email')

	password = PasswordField('Password',[
			validators.DataRequired(),
			validators.EqualTo('confirm', message='Passwords do not match')
		], description='Password')
	confirm = PasswordField('Confirm Password', description='Confirm Password')

	addLine1 = StringField('Address Line 1', [validators.Length(min = 1, max = 100)], description='Address Line 1')
	addLine2 = StringField('Address Line 2', [validators.Length(min = 0, max = 100)], description='Address Line 2')

	colony = StringField('Colony', [validators.Length(min = 1, max = 50)], description='Colony')
	city = StringField('City', [validators.Length(min = 1, max = 50)], description='City')
	state = StringField('State', [validators.Length(min = 1, max = 50)], description='State')