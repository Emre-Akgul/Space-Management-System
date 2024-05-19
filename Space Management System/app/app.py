
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


ROLES = ['Commander', 'Pilot', 'Mission Specialist', 'Flight Engineer', 'Medical Doctor']


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


@app.route('/login_astronaut', methods=['GET', 'POST'])
def login_astronaut():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Username and password must not be empty
        if not username or not password:
            flash('Please enter both username and password!', 'danger')
            return redirect(url_for('login_astronaut'))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Corrected SQL query to match the schema you've provided
        cursor.execute('SELECT User.user_id, User.name, User.password FROM User INNER JOIN Astronaut ON User.user_id = Astronaut.user_id WHERE User.username = %s', (username,))
        
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['loggedin'] = True
            session['userid'] = user['user_id'] 
            session['username'] = user['name']
            return redirect(url_for('main_page'))
        else:
            flash('Incorrect username/password!', 'danger')

    # If unsuccessful then remain in login
    return render_template('login_astronaut.html')


@app.route('/register_astronaut', methods=['GET', 'POST'])
def register_astronaut():
    message = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('SELECT Company.user_id AS company_id, User.name AS company_name FROM Company JOIN User ON Company.user_id = User.user_id')
    companies = cursor.fetchall()

    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        date_of_birth = request.form['date_of_birth']
        nationality = request.form['nationality']
        company_id = request.form['company_id']

        # Check if any required field is empty
        if not (username and name and password and email and date_of_birth and nationality):
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

                # Insert new astronaut into Astronaut table
                cursor.execute('INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, preferred_role) VALUES (%s, %s, %s, %s, %s)',
                               (user_id, company_id, date_of_birth, nationality, None))
                mysql.connection.commit()
                message = 'Astronaut successfully registered!'

    return render_template('register_astronaut.html', message=message, companies=companies, roles=ROLES)




@app.route('/missions', methods=['GET'])
def missions():
    missions = []
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = """
            SELECT mission_id, mission_name, description, status, launch_date, destination, cost, duration, crew_size 
            FROM space_mission
        """
        cursor.execute(query)
        missions = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching missions: {e}")
    finally:
        cursor.close()
    
    return render_template('missions.html', missions=missions)


@app.route('/mission/<int:mission_id>', methods=['GET', 'POST'])
def mission_details(mission_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch mission details
    cursor.execute('SELECT * FROM space_mission WHERE mission_id = %s', (mission_id,))
    mission = cursor.fetchone()

    if not mission:
        flash('Mission not found!', 'error')
        return redirect(url_for('main_page'))

    # Check if bidding is allowed for the mission
    if mission['status'] != 'Bidding':
        flash('Bidding is not allowed for this mission!', 'error')
        return redirect(url_for('main_page'))

    # Check if the bidding deadline has passed
    cursor.execute('SELECT COUNT(*) AS is_deadline_passed FROM space_mission WHERE mission_id = %s AND bid_deadline < CURRENT_DATE()', (mission_id,))
    deadline_check = cursor.fetchone()

    if deadline_check['is_deadline_passed'] > 0:
        flash('Bidding deadline has passed!', 'error')
        return redirect(url_for('main_page'))

    # Check if company has any conflicting missions
    current_company_id = session.get('user_id')  # Assuming company ID is stored in session
    cursor.execute('''
        SELECT COUNT(*) AS existing_missions
        FROM space_mission
        WHERE company_id = %s
        AND (
            (launch_date < %s AND DATE_ADD(launch_date, INTERVAL duration DAY) > %s)
            OR (launch_date BETWEEN %s AND %s)
        )
    ''', (current_company_id, mission['launch_date'], mission['launch_date'], mission['launch_date'], mission['launch_date']))
    conflict_check = cursor.fetchone()

    if conflict_check['existing_missions'] > 0:
        flash('Company has conflicting missions!', 'error')
        return redirect(url_for('main_page'))

    # Handle bidding form submission
    if request.method == 'POST':
        bid_amount = request.form.get('bid_amount')

        # Insert bid into database
        cursor.execute('INSERT INTO bid (bid_amount, bid_date, status, company_id, mission_id) VALUES (%s, CURRENT_DATE(), %s, %s, %s)',
                       (bid_amount, 'Submitted', current_company_id, mission_id))
        mysql.connection.commit()
        flash('Bid submitted successfully!', 'success')
        return redirect(url_for('main_page'))

    return render_template('mission_details.html', mission=mission)


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


@app.route('/all_astronauts')
def all_astronauts():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT User.user_id, User.username, User.name, User.email, Astronaut.date_of_birth, 
               Astronaut.nationality, Astronaut.experience_level, Astronaut.preferred_role, 
               Company.address, Company.industry_sector, Company.website
        FROM User 
        JOIN Astronaut ON User.user_id = Astronaut.user_id 
        LEFT JOIN Company ON Astronaut.company_id = Company.user_id
    ''')
    astronauts = cursor.fetchall()
    return render_template('all_astronauts.html', astronauts=astronauts)

@app.route('/astronaut/<int:user_id>')
def astronaut_profile(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch astronaut details
    cursor.execute('''
        SELECT User.user_id, User.username, User.name, User.email, Astronaut.date_of_birth, 
               Astronaut.nationality, Astronaut.experience_level, Astronaut.preferred_role, 
               Company.address, Company.industry_sector, Company.website
        FROM User 
        JOIN Astronaut ON User.user_id = Astronaut.user_id 
        LEFT JOIN Company ON Astronaut.company_id = Company.user_id
        WHERE User.user_id = %s
    ''', (user_id,))
    astronaut = cursor.fetchone()

    if not astronaut:
        flash('Astronaut not found', 'danger')
        return redirect(url_for('all_astronauts'))

    # Fetch past missions
    cursor.execute('''
        SELECT space_mission.mission_name, space_mission.description, space_mission.status, 
               space_mission.launch_date, space_mission.destination, space_mission.cost, 
               space_mission.duration, space_mission.crew_size, space_mission.required_roles
        FROM participates
        JOIN space_mission ON participates.mission_id = space_mission.mission_id
        WHERE participates.astronaut_id = %s AND space_mission.status = 'Completed'
    ''', (user_id,))
    past_missions = cursor.fetchall()

    # Fetch upcoming missions
    cursor.execute('''
        SELECT space_mission.mission_name, space_mission.description, space_mission.status, 
               space_mission.launch_date, space_mission.destination, space_mission.cost, 
               space_mission.duration, space_mission.crew_size, space_mission.required_roles
        FROM participates
        JOIN space_mission ON participates.mission_id = space_mission.mission_id
        WHERE participates.astronaut_id = %s AND space_mission.status != 'Completed'
    ''', (user_id,))
    upcoming_missions = cursor.fetchall()

    # Fetch health records
    cursor.execute('''
        SELECT checkup_date, health_status, fitness_level, expected_ready_time
        FROM Health_record
        WHERE astronaut_id = %s
    ''', (user_id,))
    health_records = cursor.fetchall()

    # Fetch training records
    cursor.execute('''
        SELECT Training_program.name, Training_program.description, Training_program.required_for, 
               Training_program.completion_date
        FROM astronaut_training
        JOIN Training_program ON astronaut_training.program_id = Training_program.program_id
        WHERE astronaut_training.astronaut_id = %s
    ''', (user_id,))
    training_records = cursor.fetchall()

    return render_template('astronaut_profile.html', astronaut=astronaut, 
                           past_missions=past_missions, upcoming_missions=upcoming_missions,
                           health_records=health_records, training_records=training_records)





if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
