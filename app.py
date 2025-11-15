import sqlite3
from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'your_super_secret_and_random_key'

# --- Helper Function to connect to the database ---
def get_db_connection():
    conn = sqlite3.connect('passwords.db')
    # This allows us to access columns by name (like a dictionary)
    conn.row_factory = sqlite3.Row
    return conn

# --- Existing Routes (from Part 3) ---
@app.route('/')
def home():
    if 'user_authenticated' in session:
        # If the session exists, ask for PIN verification instead of a full login
        return render_template('pin_refresh.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['user_authenticated'] = True
            session['user_pin'] = user['pin'] # Store the user's PIN in the session
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/login_success')
def login_success():
    session['pin_verified'] = True # Mark that the PIN was just verified
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear() # Clear all session data
    return redirect(url_for('login'))

# --- New/Updated Routes for Functionality ---
@app.route('/dashboard')
def dashboard():
    # Protect the dashboard
    if not session.get('user_authenticated') or not session.get('pin_verified'):
        return redirect(url_for('home'))

    conn = get_db_connection()
    # Fetch all passwords from the database
    passwords = conn.execute('SELECT * FROM passwords').fetchall()
    conn.close()

    # Pass the list of passwords to the template
    return render_template('dashboard.html', passwords=passwords)

@app.route('/verify_pin_refresh', methods=['POST'])
def verify_pin_refresh():
    submitted_pin = request.form['pin']
    if session.get('user_pin') and submitted_pin == session['user_pin']:
        session['pin_verified'] = True # Re-verify the PIN for this session
        return redirect(url_for('dashboard'))
    else:
        # If the PIN is wrong, log them out for security
        session.clear()
        return redirect(url_for('login'))



@app.route('/add_password', methods=['POST'])
def add_password():
    if not session.get('user_authenticated'):
        return redirect(url_for('home'))

    service = request.form['service_name']
    password = request.form['password_value']

    conn = get_db_connection()
    conn.execute('INSERT INTO passwords (service_name, password_value) VALUES (?, ?)',
                 (service, password))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))

@app.route('/delete/<int:entry_id>')
def delete(entry_id):
    if not session.get('user_authenticated'):
        return redirect(url_for('home'))

    conn = get_db_connection()
    conn.execute('DELETE FROM passwords WHERE id = ?', (entry_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

# --- Route for Handling PIN on Refresh ---
@app.route('/verify_pin_refresh', methods=['POST'])
def verify_pin_refresh():
    submitted_pin = request.form['pin']
    if submitted_pin == '078123':
        session['pin_verified'] = True # Re-verify the PIN for this session
        return redirect(url_for('dashboard'))
    else:
        # If the PIN is wrong, log them out for security
        return redirect(url_for('logout'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)