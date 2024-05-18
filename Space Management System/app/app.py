
import re  
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
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
            session['user_id'] = user['user_id'] 
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
    if 'loggedin' not in session or 'user_id' not in session:
        flash('You need to login to view this page.', 'danger')
        return redirect(url_for('login_company'))

    company_id = session['user_id']
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

    manager_id = session['user_id']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch missions managed by the logged-in company along with the creator company name and allocated spaceship name
    cursor.execute("""
        SELECT sm.mission_id, sm.mission_name, sm.status, sm.spaceship_id, sm.creator_comp_id, u.name AS creator_company_name, s.spaceship_name AS allocated_spaceship_name
        FROM space_mission sm
        JOIN User u ON sm.creator_comp_id = u.user_id
        LEFT JOIN Spaceship s ON sm.spaceship_id = s.spaceship_id
        WHERE sm.manager_comp_id = %s
    """, (manager_id,))

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

    owner_id = session['user_id']
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

    owner_id = session['user_id']
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

    # Inform user.
    flash('You have been logged out.', 'success')
    
    return redirect(url_for('login_company'))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
