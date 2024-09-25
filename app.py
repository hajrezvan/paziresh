from flask import Flask, render_template, request, redirect, url_for
from db_connection import get_users, add_user

app = Flask(__name__)

@app.route('/')
def index():
    employees = [f"{user.firstname} {user.lastname}" for user in get_users()]
    return render_template('index.html', employees=employees)

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

if __name__ == '__main__':
    app.run(debug=True)
