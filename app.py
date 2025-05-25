
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
            return redirect('/dashboard')
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    rep = session['username']
    df = pd.read_csv('data.csv')
    rep_data = df[df['Rep'] == rep]
    return render_template('dashboard.html', data=rep_data.to_dict(orient='records'), rep=rep)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
