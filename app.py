
from flask import Flask, render_template, request, redirect, session
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simple hardcoded users — replace with DB later
users = {
    'Andrew S': 'password1',
    'SAV LLC': 'password2',
    'HCM Crew LLC': 'password3',
    'Sonny': 'password4',
    'GD Laboratory': 'password5',
    'HOUSE': 'password6'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect('/select_report')  # Redirect to the selection page
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/select_report', methods=['GET', 'POST'])
def select_report():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        report_type = request.form['report_type']
        session['report_type'] = report_type
        return redirect('/dashboard')
    return render_template('select_report.html')


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    rep = session['username']
    report_type = session.get('report_type') #Get report type selected
    df = pd.read_csv('data.csv')
    rep_data = df[df['Rep'] == rep]

    # Logic to handle different report types
    if report_type == 'financials':
        #Modify this to do something specific for financials
        return render_template('dashboard.html', data=rep_data.to_dict(orient='records'), rep=rep, report_type=report_type)
    elif report_type == 'client_breakdown':
        #Modify this to do something specific for client breakdown
        return render_template('dashboard.html', data=rep_data.to_dict(orient='records'), rep=rep, report_type=report_type)
    else:
        return "Invalid report type", 400 #return if report_type is not defined in session

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

