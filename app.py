# Third Party Library Imports
from functools import wraps
from flask import Flask, render_template, redirect, url_for, request, session, flash

# Local Package Imports
from models import studio_soupify, fave_soupify, sign_up, clean_class, check_upcoming

# create the application object
app = Flask(__name__)

# Encryption key used to access data
app.secret_key = "my precious"
# Sessions use cookies to store information about a user (e.g. if they are logged in)
# Session stores actual data on server side, cookie/secret_key is on client side
# SECURITY: you want this to be generated randomly, and kept in a secret file

# login required decorator
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap

# define views -- use decorators to link the function to a url
@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
@login_required
def index():
	studio_dict = session['studio_dict']
	if request.method == 'GET':
		return render_template('index.html', studio_list=studio_dict.keys())
	else:
		# request was a POST
		session['venue_name'] = request.form['selected_studio']
		session['venue_id'] = studio_dict[session['venue_name']]
		return redirect(url_for('studio_sched'))

@app.route('/studio', methods=['GET','POST'])
@login_required
def studio_sched():
	if request.method == 'GET':
		## TO DO: add a decorator that will check if studio information has already been retrieved this session-- look at fibonnaci example
		# Feed venue_id into function to retrieve html 
		session['class_deets'] = studio_soupify(session['venue_id'])
		if len(session['class_deets']) == 0:
			return render_template('noclass.html', venue_name=session['venue_name'])
		else:
			return render_template(
				'studio.html',
				venue_name=session['venue_name'],
				class_deets=session['class_deets']
			)
	else:
		# If the request is a POST, it means someone was trying to add a class to cart
		# Class details come in as a string, so they need to be converted back to a list
		final = clean_class(request.form['selected_class'])
		# Add class to cart
		session['classes_in_cart'].append(final)
		session['active_class'] = final

		return redirect(url_for('look_cart'))

@app.route('/cart', methods=['GET','POST'])
@login_required
def look_cart():
	if request.method == 'GET':
		return render_template(
			'cart.html', 
			active_class=session['active_class'], 
			cart_contents=session['classes_in_cart']
			)
	else:
		classy = clean_class(request.form['remove_class'])
		for i, workout in enumerate(session['classes_in_cart']):
			if workout[2] == classy[2]:
				break
		session['classes_in_cart'].pop(i)
		return redirect(url_for('look_cart'))

@app.route('/noclass')
@login_required
def classes_error():
	return render_template('noclass.html', venue_name=session['venue_name'])

@app.route('/signup', methods=['GET','POST'])
@login_required
def signup():
	if request.method == 'GET':
		return render_template('signup.html', cart_contents=session['classes_in_cart'])
	else:
		sign_up(session['classes_in_cart'])
		session['reserved'] = check_upcoming(session['classes_in_cart'])
		session['classes_in_cart'] = []
		return redirect(url_for('check'))

@app.route('/done')
@login_required
def check():
	return render_template('done.html', reserved_classes=session['reserved'])

# route for handling the login page logic
# note, GET is the default method for routes in flask http://flask.pocoo.org/docs/0.10/quickstart/#http-methods
# So here we need to specifiy the POST method as well as GET so that end users can send a 
# POST request with their login credentials to that /login endpoint.
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		# tests to see if credentials are correct
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'

		# if credentials are correct, user is redirected to main route '/' (defined as index)
		else:
			session['logged_in'] = True
			flash('Login successful!')
			session['studio_dict'] = fave_soupify()
			session['classes_in_cart'] = []

			# url_for function generates an endpoint for the provided method (behind scenes)
			return redirect(url_for('index'))

	return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None) # Q - why use pop instead of resetting value to False?
	flash('Logout successful!')
	return redirect(url_for('login'))

# start the server with the 'run()' method
# (note: when flask is in debug mode, an auto-reload mechanism adds code changes)
if __name__ == '__main__':
	app.run(debug=True)