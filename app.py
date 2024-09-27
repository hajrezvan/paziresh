from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from db_connection import get_users, add_user, session ,users_table, get_events_type, insert_event, get_meetings, insert_event_detail
from sqlalchemy import delete
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize meeting state and button timers
app.meeting_state = False  # False means paused, True means running
button_times = {}  # Store the green time for each button

@app.route('/')
def index():
    events = get_events_type()
    employees = [f"{user.firstname} {user.lastname}" for user in get_users()]
    print(employees)
    return render_template('index.html', employees=employees, events=events)
    
@app.route('/click_button/<int:user_id>', methods=['POST'])
def click_button(user_id):
    if app.meeting_state:
        if user_id not in button_times:
            button_times[user_id] = {'start': datetime.now(), 'total_time': 0}  # Log start time
        else:
            # If already clicked, calculate the current time the button was active
            button_times[user_id]['start'] = datetime.now()
    return redirect(url_for('index'))

# When meeting ends, calculate the time the button was green
@app.route('/toggle_meeting', methods=['POST'])
def toggle_meeting():
    if app.meeting_state:
        # End the meeting, calculate time difference for each button
        app.meeting_state = False
        for user_id, times in button_times.items():
            if times['start']:
                times['total_time'] += (datetime.now() - times['start']).seconds
                times['start'] = None
        session['meeting_end'] = datetime.now()
    else:
        # Start the meeting
        app.meeting_state = True
        session['meeting_start'] = datetime.now()
    
    return redirect(url_for('index'))
@app.route('/list')
def list_users():
    users = get_users()
    error = request.args.get('error')
    return render_template('list.html', users=users, error=error)

@app.route('/add_user', methods=['POST'])
def add_user_route():
    userid = request.form['userid']
    firstname = request.form['firstname']
    lastname = request.form['lastname']

    # Try to add the new user
    success, error = add_user(userid, firstname, lastname)
    
    if success:
        return redirect(url_for('list_users'))
    else:
        return redirect(url_for('list_users', error=error))
    

# Route to delete a user
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    # Delete the user from the database
    try:
        delete_query = delete(users_table).where(users_table.c.userId == user_id)
        session.execute(delete_query)
        session.commit()
        flash('User deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting user: {str(e)}', 'danger')
    
    return redirect(url_for('list_users'))


from datetime import datetime

@app.route('/add_meeting', methods=['POST'])
def add_meeting():
    meeting_name = request.form['meeting_name']
    event_id = request.form['event_id']
    event_date = datetime.now()  # Assuming you want to log the current date and time
        
    # Insert event into the database
    
        
    # Flash a success message
    if insert_event(name=meeting_name, event_type=event_id, date=event_date):
        flash("جلسه با موفقیت اضافه شد!")  # "Meeting added successfully!"
    else:
        flash("خطا: رویداد انتخاب شده یافت نشد.")  # "Error: Selected event not found."
    
    return redirect(url_for('index'))


# Report page
@app.route('/report')
def report():
    meetings = get_meetings()  # Fetch meetings from the database
    return render_template('report.html', meetings=meetings)


@app.route('/submit_meeting', methods=['POST'])
def submit_meeting():
    data = request.get_json()
    event_id = data['eventId']
    user_times = data['userTimes']  # This is a dictionary of userId -> time
    
    try:
        for user_id, time in user_times.items():
            insert_event_detail(user_id=user_id, event_id=event_id, time_in_meeting=time)
        
        session.commit()  # Make sure to commit the transaction
        return jsonify(success=True)
    except Exception as e:
        session.rollback()

if __name__ == '__main__':
    app.run(debug=True)
