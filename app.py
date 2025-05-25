from flask import Flask, render_template, request, redirect, session, abort
import pandas as pd
import os
import bcrypt

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')

# Replace with database interaction later
users = {
    'Andrew S': bcrypt.hashpw('password1'.encode('utf-8'), bcrypt.gensalt()),
    'SAV LLC': bcrypt.hashpw('password2'.encode('utf-8'), bcrypt.gensalt()),
    'HCM Crew LLC': bcrypt.hashpw('password3'.encode('utf-8'), bcrypt.gensalt()),
    'Sonny': bcrypt.hashpw('password4'.encode('utf-8'), bcrypt.gensalt()),
    'GD Laboratory': bcrypt.hashpw('password5'.encode('utf-8'), bcrypt.gensalt()),
    'HOUSE': bcrypt.hashpw('password6'.encode('utf-8'), bcrypt.gensalt())
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        if username in users and bcrypt.checkpw(password, users[username]):
            session['username'] = username
            return redirect('/dashboard')
        else:
            abort(401, "Invalid username or password")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    rep = session['username']
    try:
        df = pd.read_csv('data.csv')
        rep_data = df[df['Rep'] == rep]
        return render_template('dashboard.html', data=rep_data.to_dict(orient='records'), rep=rep)
    except FileNotFoundError:
         abort(500, "Data file not found.")
    except Exception as e:
        abort(500, f"An error occurred: {str(e)}")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.errorhandler(401)
def unauthorized(error):
    return render_template('error.html', message=error.description), 401

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', message=error.description), 500

if __name__ == '__main__':
    app.run(debug=True)
