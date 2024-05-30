from flask import Flask, request, redirect, render_template, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = 'logs.db'
REDIRECT_URL = "https://default.com"
AUTO_REDIRECT = True 

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def log_request(ip, user_agent):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (ip, user_agent, timestamp) VALUES (?, ?, ?)",
                   (ip, user_agent, datetime.now()))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    log_request(ip, user_agent)
    if AUTO_REDIRECT:
        return redirect(REDIRECT_URL)
    else:
        return "Auto-redirect is disabled. Please visit the dashboard to enable it."

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    global REDIRECT_URL, AUTO_REDIRECT
    if request.method == 'POST':
        REDIRECT_URL = request.form['redirect_url']
        AUTO_REDIRECT = 'auto_redirect' in request.form
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    logs = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', logs=logs, redirect_url=REDIRECT_URL, auto_redirect=AUTO_REDIRECT)

if __name__ == '__main__':
    app.run(debug=True)
