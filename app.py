from flask import Flask, render_template, request, redirect, url_for, flash
from db_connection import get_users, add_user, users_table, session, get_events_type, insert_event, get_meetings
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
    return render_template('index.html', employees=employees, events=events)

# Start/End meeting logic
@app.route('/toggle_meeting', methods=['POST'])
def toggle_meeting():
    if app.meeting_state:
        # End the meeting
        app.meeting_state = False
        session['meeting_end'] = datetime.now()
    else:
        # Start the meeting
        app.meeting_state = True
        session['meeting_start'] = datetime.now()
        session['button_click_times'] = {user['userId']: None for user in get_users()}

    
# Button click (makes button green)
@app.route('/click_button/<int:user_id>', methods=['POST'])
def click_button(user_id):
    if app.meeting_state:
        session['button_click_times'][user_id] = datetime.now()  # Log the click time for the user button
    return redirect(url_for('index'))


# Submit meeting and calculate times
@app.route('/submit_meeting', methods=['POST'])
def submit_meeting():
    meeting_start = session.get('meeting_start')
    meeting_end = session.get('meeting_end')
    button_click_times = session.get('button_click_times', {})

    report_data = []
    
    if meeting_start and meeting_end:
        total_meeting_time = (meeting_end - meeting_start).total_seconds()
        
        # Calculate time each button was green during the meeting
        for user_id, click_time in button_click_times.items():
            if click_time:
                time_green = (meeting_end - click_time).total_seconds()
            else:
                time_green = 0
            report_data.append({
                'user_id': user_id,
                'time_green': time_green
            })
    
    # Redirect to report page
    return render_template('report.html', report_data=report_data)

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

if __name__ == '__main__':
    app.run(debug=True)
