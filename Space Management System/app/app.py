
import re  
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, current_user, login_required, logout_user, UserMixin

import MySQLdb.cursors
import bcrypt
from datetime import datetime

#test
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
        if user and password == user['password']:
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
                # Insert new user into User table
                cursor.execute('INSERT INTO User (username, name, password, email) VALUES (%s, %s, %s, %s)',
                               (username, name, password, email))
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
                cursor.execute('INSERT INTO Astronaut (user_id, company_id, date_of_birth, nationality, role_id) VALUES (%s, %s, %s, %s, %s)',
                               (user_id, company_id, date_of_birth, nationality, None))
                mysql.connection.commit()
                message = 'Astronaut successfully registered!'

    return render_template('register_astronaut.html', message=message, companies=companies, roles=ROLES)


@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Username and password must not be empty
        if not username or not password:
            flash('Please enter both username and password!', 'danger')
            return redirect(url_for('login_admin'))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Corrected SQL query to match the schema you've provided
        cursor.execute('SELECT User.user_id, User.name, User.password, Admin.permission_level FROM User INNER JOIN Admin ON User.user_id = Admin.user_id WHERE User.username = %s', (username,))
        
        user = cursor.fetchone()
        if user and password == user['password']:
            session['admin'] = user['permission_level']
            session['loggedin'] = True
            session['userid'] = user['user_id'] 
            session['username'] = user['name']
            return redirect(url_for('main_page'))
        else:
            flash('Incorrect username/password!', 'danger')

    # If unsuccessful then remain in login
    return render_template('login_admin.html')

@app.route('/managed_admins', methods=['GET', 'DELETE'])
def managed_admins(user_id):
    if 'admin' not in session:
            flash('You need to login as an admin to view this page.', 'danger')
            return redirect(url_for('login_admin'))
    elif session['admin'] != 'SuperAdmin':
        flash('You need to be a superadmin to view this page.', 'danger')
        return redirect(url_for('main_page'))
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM Admin WHERE user_id = %s', (user_id,))
        mysql.connection.commit()
        return 'Admin deleted successfully'
    elif request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT User.user_id, User.username, Admin.permission_level FROM User INNER JOIN Admin ON User.user_id = Admin.user_id')
        admins = cursor.fetchall()
        return render_template('managed_admins.html', admins=admins)

@app.route('/managed_companies', methods=['GET', 'POST'])
def managed_companies():
    if 'admin' not in session:
            flash('You need to login as an admin to view this page.', 'danger')
            return redirect(url_for('login_admin'))
    elif session['admin'] != 'SuperAdmin':
        flash('You need to be a superadmin to view this page.', 'danger')
        return redirect(url_for('main_page'))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Company INNER JOIN User ON User.user_id = Company.user_id')
    companies = cursor.fetchall()
    return render_template('managed_companies.html', companies=companies)

@app.route('/managed_astronauts', methods=['GET', 'POST'])
def managed_astronauts():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Astronaut INNER JOIN User ON User.user_id = Astronaut.user_id INNER JOIN Company ON Astronaut.company_id = Company.user_id INNER JOIN Role ON Astronaut.role_id = Role.role_id')
    astronauts = cursor.fetchall()
    return render_template('managed_astronauts.html', astronauts=astronauts)

@app.route('/managed_ships', methods=['GET', 'POST'])
def managed_ships():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Spaceship INNER JOIN Company ON Spaceship.owner_comp_id = Company.user_id')
    ships = cursor.fetchall()
    return render_template('managed_ships.html', ships=ships)

@app.route('/managed_biddings', methods=['GET', 'POST'])
def managed_biddings():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM bid INNER JOIN space_mission ON bid.mission_id = space_mission.mission_id')
    bids = cursor.fetchall()
    return render_template('managed_biddings.html', bids=bids)




@app.route('/missions', methods=['GET'])
def missions():
    # Existing query parameters
    status = request.args.get('status', '')
    cost_min = request.args.get('cost_min', '')
    cost_max = request.args.get('cost_max', '')
    launch_after = request.args.get('launch_after', '')
    launch_before = request.args.get('launch_before', '')
    crew_min = request.args.get('crew_min', '')  # New minimum crew size
    crew_max = request.args.get('crew_max', '')  # New maximum crew size

    # Building the query
    query_parts = ["SELECT mission_id, mission_name, description, status, launch_date, destination, cost, duration, crew_size FROM space_mission WHERE 1=1"]
    query_params = []

    if status:
        query_parts.append("AND status = %s")
        query_params.append(status)
    if cost_min:
        query_parts.append("AND cost >= %s")
        query_params.append(cost_min)
    if cost_max:
        query_parts.append("AND cost <= %s")
        query_params.append(cost_max)
    if launch_after:
        query_parts.append("AND launch_date >= %s")
        query_params.append(launch_after)
    if launch_before:
        query_parts.append("AND launch_date <= %s")
        query_params.append(launch_before)
    if crew_min:
        query_parts.append("AND crew_size >= %s")
        query_params.append(crew_min)
    if crew_max:
        query_parts.append("AND crew_size <= %s")
        query_params.append(crew_max)

    query = " ".join(query_parts)
    
    missions = []
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, tuple(query_params))
        missions = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching missions: {e}")
    finally:
        cursor.close()
    
    return render_template('missions.html', missions=missions, status=status, cost_min=cost_min, cost_max=cost_max, launch_after=launch_after, launch_before=launch_before, crew_min=crew_min, crew_max=crew_max)



@app.route('/mission/<int:mission_id>', methods=['GET', 'POST'])
def mission_details(mission_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch mission details
    cursor.execute('SELECT * FROM space_mission WHERE mission_id = %s', (mission_id,))
    mission = cursor.fetchone()

    if not mission:
        flash('Mission not found!', 'error')
        return redirect(url_for('main_page'))

    # Check if the bidding deadline has passed
    bid_deadline_passed = mission['bid_deadline'] < datetime.now().date()

    # Flash messages for status and bid deadline
    if mission['status'] != 'Bidding':
        flash('Bidding is not allowed for this mission!', 'danger')
    if bid_deadline_passed:
        flash('Bidding deadline has passed!', 'danger')

    # Handle bid submission
    if request.method == 'POST' and mission['status'] == 'Bidding' and not bid_deadline_passed:
        bid_amount = request.form.get('bid_amount')
        # Insert bid into database
        cursor.execute('INSERT INTO bid (bid_amount, bid_date, status, company_id, mission_id) VALUES (%s, CURDATE(), %s, %s, %s)',
                       (bid_amount, 'Submitted', session.get('user_id'), mission_id))
        mysql.connection.commit()
        # Flash success message
        flash(f'Bid submitted successfully for mission {mission["mission_name"]}!', 'success')
        return redirect(url_for('mission_details', mission_id=mission_id))

    cursor.close()
    return render_template('mission_details.html', mission=mission, bid_deadline_passed=bid_deadline_passed)


@app.route('/biddings')
def biddings():
    if 'loggedin' not in session or 'userid' not in session:
        flash('You need to login to view this page.', 'danger')
        return redirect(url_for('login_company'))

    company_id = session['userid']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch missions and their bids
    cursor.execute("""
    SELECT sm.mission_id, sm.mission_name, sm.status, b.bid_id, b.bid_amount, b.status AS bid_status, u.name AS bidder_name
    FROM space_mission sm
    LEFT JOIN bid b ON sm.mission_id = b.mission_id
    LEFT JOIN User u ON b.company_id = u.user_id
    WHERE sm.creator_comp_id = %s
    ORDER BY sm.mission_id, b.bid_date DESC
    """, (company_id,))

    missions = {}
    for row in cursor.fetchall():
        if row['mission_id'] not in missions:
            missions[row['mission_id']] = {
                'mission_name': row['mission_name'],
                'status': row['status'],
                'bids': []
            }
        if row['bid_id']:
            missions[row['mission_id']]['bids'].append({
                'bid_id': row['bid_id'],
                'bid_amount': row['bid_amount'],
                'bid_status': row['bid_status'],
                'bidder_name': row['bidder_name']
            })

    cursor.close()
    return render_template('biddings.html', missions=missions)

@app.route('/handle_bid/<int:bid_id>/<int:mission_id>', methods=['POST'])
def handle_bid(bid_id, mission_id):
    if 'loggedin' not in session:
        return redirect(url_for('login_company'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch the accepted bid details
    cursor.execute("SELECT company_id, bid_amount FROM bid WHERE bid_id = %s", (bid_id,))
    bid = cursor.fetchone()

    if not bid:
        flash('Bid not found!', 'danger')
        return redirect(url_for('biddings'))

    # Fetch mission creator's company_id
    cursor.execute("SELECT creator_comp_id FROM space_mission WHERE mission_id = %s", (mission_id,))
    mission = cursor.fetchone()

    if not mission:
        flash('Mission not found!', 'danger')
        return redirect(url_for('biddings'))

    # Update mission status
    #cursor.execute("UPDATE space_mission SET status = 'In Progress' WHERE mission_id = %s", (mission_id,))

    # Update mission status and manager
    cursor.execute("""
        UPDATE space_mission 
        SET status = 'In Progress', manager_comp_id = %s 
        WHERE mission_id = %s
    """, (bid['company_id'], mission_id,))


    # Update accepted bid
    cursor.execute("UPDATE bid SET status = 'Accepted' WHERE bid_id = %s", (bid_id,))

    # Reject other bids
    cursor.execute("UPDATE bid SET status = 'Rejected' WHERE mission_id = %s AND bid_id != %s", (mission_id, bid_id))

    # Create financial transaction
    cursor.execute("""
        INSERT INTO financial_transaction (date, type, amount, status, description, payer_comp, payee_comp, mission_id)
        VALUES (CURDATE(), 'Bid Payment', %s, 'Completed', 'Payment for mission bid', %s, %s, %s)
    """, (bid['bid_amount'], bid['company_id'], mission['creator_comp_id'], mission_id))

    mysql.connection.commit()
    cursor.close()

    flash('Bid accepted, mission updated, and payment processed!', 'success')
    return redirect(url_for('biddings'))


@app.route('/managed_missions')
def managed_missions():
    if 'loggedin' not in session:
        return redirect(url_for('login_company'))

    manager_id = session['userid']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch missions managed by the logged-in company along with the creator company name and allocated spaceship name
    cursor.execute("""
        SELECT sm.mission_id, sm.mission_name, sm.status, sm.spaceship_id, sm.creator_comp_id, u.name AS creator_company_name, s.spaceship_name AS allocated_spaceship_name
        FROM space_mission sm
        JOIN User u ON sm.creator_comp_id = u.user_id
        LEFT JOIN Spaceship s ON sm.spaceship_id = s.spaceship_id
        WHERE sm.manager_comp_id = %s
    """, (manager_id,))
    
    if 'admin' in session: # Admin can view all missions
        cursor.execute("""
            SELECT sm.mission_id, sm.mission_name, sm.status, sm.spaceship_id, sm.creator_comp_id, u.name AS creator_company_name, s.spaceship_name AS allocated_spaceship_name
        """)

    missions = cursor.fetchall()

    # Prepare list to collect company IDs (both manager and creator)
    company_ids = set([manager_id])  # Start with the manager company ID
    for mission in missions:
        company_ids.add(mission['creator_comp_id'])  # Add creator comp IDs

    # Fetch all spaceships owned by the session's company and each mission's creator company
    # Convert set to list for SQL query compatibility
    company_ids = list(company_ids)
    format_strings = ','.join(['%s'] * len(company_ids))  # Create format strings for SQL query
    cursor.execute("""
        SELECT spaceship_id, spaceship_name, type, status, owner_comp_id
        FROM Spaceship
        WHERE owner_comp_id IN (%s)
    """ % format_strings, tuple(company_ids))

    spaceships = cursor.fetchall()

    cursor.close()

    # Organize spaceships by owner for easier access in the template
    spaceship_dict = {}
    for spaceship in spaceships:
        owner_id = spaceship['owner_comp_id']
        if owner_id not in spaceship_dict:
            spaceship_dict[owner_id] = []
        spaceship_dict[owner_id].append(spaceship)

    return render_template('managed_missions.html', missions=missions, spaceships=spaceship_dict)


@app.route('/allocate_spaceship/<int:mission_id>', methods=['POST'])
def allocate_spaceship(mission_id):
    if 'loggedin' not in session:
        return redirect(url_for('login_company'))

    spaceship_id = request.form.get('spaceship_id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Update the mission with the selected spaceship
    cursor.execute("UPDATE space_mission SET spaceship_id = %s WHERE mission_id = %s", (spaceship_id, mission_id))

    mysql.connection.commit()
    cursor.close()
    flash('Spaceship allocated successfully!', 'success')
    return redirect(url_for('managed_missions'))

@app.route('/my_ships')
def my_ships():
    if 'loggedin' not in session:
        return redirect(url_for('login_company'))

    owner_id = session['userid']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT spaceship_id, spaceship_name, type, status FROM Spaceship WHERE owner_comp_id = %s", (owner_id,))
    ships = cursor.fetchall()
    cursor.close()
    return render_template('my_ships.html', ships=ships)

@app.route('/retire_ship/<int:spaceship_id>', methods=['POST'])
def retire_ship(spaceship_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("UPDATE Spaceship SET status = 'Retired' WHERE spaceship_id = %s", (spaceship_id,))
    mysql.connection.commit()
    cursor.close()
    flash('Ship has been retired successfully.', 'success')
    return redirect(url_for('my_ships'))

@app.route('/add_ship', methods=['POST'])
def add_ship():
    if 'loggedin' not in session:
        return redirect(url_for('login_company'))

    owner_id = session['userid']
    spaceship_name = request.form.get('spaceship_name')
    type = request.form.get('type')
    capacity = request.form.get('capacity')
    launch_vehicle_id = request.form.get('launch_vehicle_id')  # Assuming this is optional

    if not (spaceship_name and type and capacity):
        flash('All fields are required except launch vehicle.', 'danger')
        return redirect(url_for('my_ships'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("INSERT INTO Spaceship (spaceship_name, type, status, capacity, owner_comp_id, launch_vehicle_id) VALUES (%s, %s, 'Active', %s, %s, %s)", 
                   (spaceship_name, type, capacity, owner_id, launch_vehicle_id if launch_vehicle_id else None))
    mysql.connection.commit()
    cursor.close()

    flash('New ship added to inventory.', 'success')
    return redirect(url_for('my_ships'))



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
    if 'admin' in session:
        session.pop('admin', None)

    # Inform user.
    flash('You have been logged out.', 'success')
    
    return redirect(url_for('login_company'))


@app.route('/all_astronauts')
def all_astronauts():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT User.user_id, User.username, User.name, User.email, Astronaut.date_of_birth, 
               Astronaut.nationality, Astronaut.experience_level, Role.role_name AS preferred_role, 
               Company.address, Company.industry_sector, Company.website
        FROM User 
        JOIN Astronaut ON User.user_id = Astronaut.user_id 
        LEFT JOIN Company ON Astronaut.company_id = Company.user_id
        LEFT JOIN Role ON Astronaut.role_id = Role.role_id
    ''')
    astronauts = cursor.fetchall()
    return render_template('all_astronauts.html', astronauts=astronauts)

@app.route('/astronaut/<int:user_id>')
def astronaut_profile(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch astronaut details
    cursor.execute('''
        SELECT User.user_id, User.username, User.name, User.email, Astronaut.date_of_birth, 
               Astronaut.nationality, Astronaut.experience_level, Role.role_name AS preferred_role, 
               Company.address, Company.industry_sector, Company.website
        FROM User 
        JOIN Astronaut ON User.user_id = Astronaut.user_id 
        LEFT JOIN Company ON Astronaut.company_id = Company.user_id
        LEFT JOIN Role ON Astronaut.role_id = Role.role_id
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
        SELECT Training_program.program_id, Training_program.name, Training_program.description, Role.role_name AS required_for, 
               astronaut_training.completion_date
        FROM astronaut_training
        JOIN Training_program ON astronaut_training.program_id = Training_program.program_id
        JOIN Role ON Training_program.required_for = Role.role_id
        WHERE astronaut_training.astronaut_id = %s
    ''', (user_id,))
    training_records = cursor.fetchall()

    # Fetch available training programs
    cursor.execute('''
        SELECT Training_program.program_id, Training_program.name, Training_program.description, Role.role_name AS required_for
        FROM Training_program
        JOIN Role ON Training_program.required_for = Role.role_id
        WHERE Training_program.program_id NOT IN (
            SELECT program_id FROM astronaut_training WHERE astronaut_id = %s
        )
    ''', (user_id,))
    available_training_programs = cursor.fetchall()

    # Fetch roles
    cursor.execute('SELECT role_id, role_name FROM Role')
    roles = cursor.fetchall()

    is_own_profile = (session.get('userid') == user_id)

    return render_template('astronaut_profile.html', astronaut=astronaut, roles=roles,
                           past_missions=past_missions, upcoming_missions=upcoming_missions,
                           health_records=health_records, training_records=training_records,
                           available_training_programs=available_training_programs,
                           is_own_profile=is_own_profile)

@app.route('/apply_training/<int:user_id>/<int:program_id>', methods=['POST'])
def apply_training(user_id, program_id):
    if 'userid' in session and session['userid'] == user_id:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            INSERT INTO astronaut_training (astronaut_id, program_id, completion_date)
            VALUES (%s, %s, NULL)
        ''', (user_id, program_id))
        mysql.connection.commit()

        flash('Training program application submitted successfully', 'success')
    else:
        flash('You are not authorized to perform this action', 'danger')

    return redirect(url_for('astronaut_profile', user_id=user_id))

@app.route('/add_health_record/<int:user_id>', methods=['GET', 'POST'])
def add_health_record(user_id):
    if session.get('userid') != user_id:
        flash('You are not authorized to add health records for this astronaut', 'danger')
        return redirect(url_for('astronaut_profile', user_id=user_id))
    
    if request.method == 'POST':
        checkup_date = request.form['checkup_date']
        health_status = request.form['health_status']
        fitness_level = request.form['fitness_level']
        expected_ready_time = request.form['expected_ready_time']
        
        if not (checkup_date and health_status and fitness_level):
            flash('Please fill out all required fields', 'danger')
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            if not expected_ready_time:
                expected_ready_time = None
            cursor.execute('''
                INSERT INTO Health_record (checkup_date, health_status, fitness_level, expected_ready_time, astronaut_id)
                VALUES (%s, %s, %s, %s, %s)
            ''', (checkup_date, health_status, fitness_level, expected_ready_time, user_id))
            mysql.connection.commit()
            flash('Health record added successfully', 'success')
            return redirect(url_for('astronaut_profile', user_id=user_id))

    return render_template('add_health_record.html', user_id=user_id)

@app.route('/change_role/<int:user_id>', methods=['POST'])
def change_role(user_id):
    if session.get('userid') != user_id:
        flash('You are not authorized to change the role for this astronaut', 'danger')
        return redirect(url_for('astronaut_profile', user_id=user_id))

    new_role_id = request.form.get('role_id')
    if new_role_id:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            UPDATE Astronaut
            SET role_id = %s
            WHERE user_id = %s
        ''', (new_role_id, user_id))
        mysql.connection.commit()
        flash('Preferred role updated successfully', 'success')
    else:
        flash('Please select a valid role', 'danger')

    return redirect(url_for('astronaut_profile', user_id=user_id))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
