
from datetime import datetime
import re  
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import bcrypt


app = Flask(__name__) 

app.secret_key = 'abcdefgh'
  
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'spaceapp'
  
mysql = MySQL(app)  

@app.route('/')

@app.route('/login_company', methods=['GET', 'POST'])
def login_company():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Username and password must not be empty
        if not username or not password:
            flash('Please enter both username and password!', 'danger')
            return redirect(url_for('login_company'))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Corrected SQL query to match the schema you've provided
        cursor.execute('SELECT User.user_id, User.name, User.password FROM User INNER JOIN Company ON User.user_id = Company.user_id WHERE User.username = %s', (username,))
        
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['loggedin'] = True
            session['userid'] = user['user_id'] 
            session['username'] = user['name']
            return redirect(url_for('main_page'))
        else:
            flash('Incorrect username/password!', 'danger')

    # If unsuccessful then remain in login
    return render_template('login_company.html')

@app.route('/register_company', methods=['GET', 'POST'])
def register_company():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        address = request.form['address']
        industry_sector = request.form['industry_sector']
        website = request.form['website']  # This field is optional


        # Check if any required field is empty
        if not (username and name and password and email and address and industry_sector):
            message = 'Please fill out all required fields!'
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Check if username already exists
            cursor.execute('SELECT user_id FROM User WHERE username = %s', (username,))
            if cursor.fetchone():
                message = 'Username already taken. Please choose a different username.'
            else:
                # Hash password before storing it
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                # Insert new user into User table
                cursor.execute('INSERT INTO User (username, name, password, email) VALUES (%s, %s, %s, %s)',
                               (username, name, hashed_password, email))
                user_id = cursor.lastrowid  # Fetch the last inserted id

                # Insert new company into Company table
                cursor.execute('INSERT INTO Company (user_id, address, industry_sector, website) VALUES (%s, %s, %s, %s)',
                               (user_id, address, industry_sector, website))
                mysql.connection.commit()
                message = 'Company successfully registered!'

    return render_template('register_company.html', message=message)


@app.route('/missions', methods=['GET'])
def missions():
    missions = []
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = """
            SELECT mission_name, description, status, launch_date, destination, cost, duration, crew_size 
            FROM space_mission
        """
        cursor.execute(query)
        missions = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching missions: {e}")
    finally:
        cursor.close()
    
    return render_template('missions.html', missions=missions)


@app.route('/main')
def main_page():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        return render_template('main.html', username=session['username']) 

    # if not logged in redirect to login
    return redirect(url_for('login_company'))

@app.route('/logout')
def logout():
    # Clear the session
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('username', None)

    # Inform user.
    flash('You have been logged out.', 'success')
    
    return redirect(url_for('login_company'))

@app.route('/create_space_mission', methods=['GET', 'POST'])
def create_space_mission():
	if 'loggedin' in session:
		if request.method == 'POST':
			mission_name = request.form.get('mission_name')
			description = request.form.get('description')
			launch_date = request.form.get('launch_date')
			destination = request.form.get('destination')
			cost = request.form.get('cost')
			duration = request.form.get('duration')
			crew_size = request.form.get('crew_size')
			required_roles = request.form.get('required_roles')
			bid_deadline = request.form.get('bid_deadline')
			creator_comp_id = session['userid']
			status = 'Bidding'

			if not (mission_name and description and launch_date and destination and cost and duration and crew_size and required_roles and bid_deadline):
				flash('Please fill out all required fields!', 'danger')
				return redirect(url_for('create_space_mission'))

			if len(mission_name) > 255:
				flash('Mission name exceeds maximum length (255 characters)!', 'danger')
				return redirect(url_for('create_space_mission'))
			if len(description) > 4096:
				flash('Description exceeds maximum length (4096 characters)!', 'danger')
				return redirect(url_for('create_space_mission'))
			if len(destination) > 100:
				flash('Destination exceeds maximum length (100 characters)!', 'danger')
				return redirect(url_for('create_space_mission'))
			if len(required_roles) > 255:
				flash('Required roles exceeds maximum length (255 characters)!', 'danger')
				return redirect(url_for('create_space_mission'))

			try:
				bid_deadline = datetime.strptime(bid_deadline, '%Y-%m-%d')
				launch_date = datetime.strptime(launch_date, '%Y-%m-%d')
			except ValueError:
				flash('Invalid date format! Please use YYYY-MM-DD.', 'danger')
				return redirect(url_for('create_space_mission'))

			if bid_deadline <= datetime.now():
				flash('Bid deadline must be in the future!', 'danger')
				return redirect(url_for('create_space_mission'))

			if launch_date <= bid_deadline:
				flash('Launch date must be after the bid deadline!', 'danger')
				return redirect(url_for('create_space_mission'))

			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('INSERT INTO space_mission (mission_name, description, status, launch_date, destination, cost, duration, crew_size, required_roles, bid_deadline, creator_comp_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
						(mission_name, description, status, launch_date, destination, cost, duration, crew_size, required_roles, bid_deadline, creator_comp_id))
			mysql.connection.commit()

			flash('Space mission created successfully!', 'success')
			return redirect(url_for('main_page'))

		companies, spaceships = get_companies_and_spaceships()
		return render_template('create_space_mission.html', companies=companies, spaceships=spaceships)
	else:
		return redirect(url_for('login_company'))

@app.route('/manage_missions', methods=['GET', 'POST'])
def manage_missions():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		user_id = session['userid']

		if request.method == 'POST':
			company_type = request.form.get('company_type')
			
			if company_type == 'creator':
				cursor.execute('SELECT * FROM space_mission WHERE creator_comp_id = %s', (user_id,))
			elif company_type == 'manager':
				cursor.execute('SELECT * FROM space_mission WHERE manager_comp_id = %s', (user_id,))
			else:
				flash('Invalid company type selected', 'danger')
				return redirect(url_for('manage_missions'))

			missions = cursor.fetchall()
			return render_template('manage_missions.html', missions=missions, company_type=company_type)
		
		return render_template('manage_missions.html', missions=None)
	else:
		return redirect(url_for('login_company'))

@app.route('/edit_mission/<int:mission_id>', methods=['GET', 'POST'])
def edit_mission(mission_id):
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		
		# Fetch the mission details
		cursor.execute('SELECT * FROM space_mission WHERE mission_id = %s', (mission_id,))
		mission = cursor.fetchone()

		# Fetch the company's spaceships
		creator_comp_id = session['userid']
		cursor.execute('''
			SELECT s.spaceship_id, s.spaceship_name 
			FROM Spaceship s
			JOIN owns o ON s.spaceship_id = o.spaceship_id
			WHERE o.company_id = %s
		''', (creator_comp_id,))
		spaceships = cursor.fetchall()

		if request.method == 'POST':
			mission_name = request.form.get('mission_name')
			description = request.form.get('description')
			status = request.form.get('status')
			launch_date = request.form.get('launch_date')
			destination = request.form.get('destination')
			cost = request.form.get('cost')
			duration = request.form.get('duration')
			crew_size = request.form.get('crew_size')
			required_roles = request.form.get('required_roles')
			bid_deadline = request.form.get('bid_deadline')
			spaceship_id = request.form.get('spaceship_id')

			cursor.execute('''
				UPDATE space_mission 
				SET mission_name=%s, description=%s, status=%s, launch_date=%s, destination=%s, 
					cost=%s, duration=%s, crew_size=%s, required_roles=%s, bid_deadline=%s, spaceship_id=%s 
				WHERE mission_id=%s
			''', (mission_name, description, status, launch_date, destination, cost, duration, crew_size, required_roles, bid_deadline, spaceship_id, mission_id))
			mysql.connection.commit()

			flash('Mission updated successfully!', 'success')
			return redirect(url_for('manage_missions'))

		return render_template('edit_mission.html', mission=mission, spaceships=spaceships)
	else:
		return redirect(url_for('login_company'))

def get_companies_and_spaceships():
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

	cursor.execute('''
		SELECT Company.user_id, User.username AS name 
		FROM Company 
		JOIN User ON Company.user_id = User.user_id
	''')
	companies = cursor.fetchall()

	user_id = session['userid']
	cursor.execute('SELECT spaceship_id, spaceship_name FROM Spaceship WHERE owner_comp_id = %s', (user_id,))
	spaceships = cursor.fetchall()

	return companies, spaceships

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
