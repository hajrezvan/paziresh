from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Read employee names from the text file
    with open('employees.txt', 'r') as file:
        employees = [line.strip() for line in file.readlines()]
    return render_template('index.html', employees=employees)

if __name__ == '__main__':
    app.run(debug=True)
