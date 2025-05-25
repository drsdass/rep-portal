
from flask import Flask, render_template, request, redirect, session
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Google Drive setup
SERVICE_ACCOUNT_FILE = 'path/to/your/service_account_key.json'  # Replace with your JSON key
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
creds = None
if os.path.exists(SERVICE_ACCOUNT_FILE):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

drive_service = build('drive', 'v3', credentials=creds)

# User and entity setup
users = {
    'Andrew S': {'password': 'password1', 'entities': ['financials', 'client_breakdown']},
    'SAV LLC': {'password': 'password2', 'entities': ['financials']},
    'HCM Crew LLC': {'password': 'password3', 'entities': ['client_breakdown']},
    'Sonny': {'password': 'password4', 'entities': []},
    'GD Laboratory': {'password': 'password5', 'entities': ['financials', 'client_breakdown']},
    'HOUSE': {'password': 'password6', 'entities': ['financials']}
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect('/select_report')
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/select_report', methods=['GET', 'POST'])
def select_report():
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    available_entities = users[username]['entities']

    if not available_entities:
         return render_template('unauthorized.html')

    if request.method == 'POST':
        report_type = request.form['report_type']
        if report_type in available_entities:
            session['report_type'] = report_type
            return redirect('/dashboard')
        else:
            return 'Unauthorized report type', 403
    return render_template('select_report.html', available_entities=available_entities)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    rep = session['username']
    report_type = session.get('report_type')
    df = pd.read_csv('data.csv')
    rep_data = df[df['Rep'] == rep]

    if report_type == 'financials':
        folder_id = 'your_google_drive_folder_id'  # Replace with your folder ID
        files = fetch_pdf_files(folder_id)
        return render_template('dashboard.html', data=rep_data.to_dict(orient='records'), rep=rep, report_type=report_type, files=files)
    elif report_type == 'client_breakdown':
        return render_template('dashboard.html', data=rep_data.to_dict(orient='records'), rep=rep, report_type=report_type)
    else:
        return "Invalid report type", 400


def fetch_pdf_files(folder_id):
    results = drive_service.files().list(q=f"'{folder_id}' in parents and mimeType='application/pdf'",
                                        fields="files(id, name, webViewLink)").execute()
    return results.get('files', [])


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)


