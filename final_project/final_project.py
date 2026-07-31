from flask import Flask, request, render_template, redirect, url_for, flash, session
import pandas as pd
from sqlalchemy import create_engine
import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key'

ENTRIES_ENGINE = create_engine('sqlite:///final_project/static/entries.db')
ACCOUNTS_ENGINE = create_engine('sqlite:///final_project/static/accounts.db')
existing_usernames = pd.read_sql('SELECT username FROM accounts', con=ACCOUNTS_ENGINE)['username'].astype(str).tolist()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])

        existing_usernames.append(username)
        if len(existing_usernames) != len(set(existing_usernames)):
            existing_usernames.pop(-1)
            flash('That username is already taken. Please choose another one.')
            return redirect(url_for('signup'))       

        new_account = pd.DataFrame([{
            'username': username,
            'password': password
        }])

        new_account.to_sql('accounts', con=ACCOUNTS_ENGINE, if_exists='append', index=False)

        session['username'] = username
        return redirect(url_for('journal'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = str(request.form.get('username'))
        password = str(request.form.get('password'))
    
        DATABASE_DF = pd.read_sql("SELECT * FROM accounts", con=ACCOUNTS_ENGINE)
    
        correct_user = DATABASE_DF[(DATABASE_DF['username'] == username) & (DATABASE_DF['password'] == password)]

        if not correct_user.empty:
            session['username'] = username
            return redirect(url_for('journal'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/journal')
def journal():
    if 'username' not in session:
        flash('Please log in first')
        return redirect(url_for('login'))

    username = session['username']
    entries_df = pd.read_sql('SELECT rowid as id, * FROM entries', con = ENTRIES_ENGINE.connect())
    user_entries = entries_df[entries_df['username'].astype(str) == username].to_dict('records')

    return render_template('journal.html',
                           username = username,
                           entries = user_entries)

@app.route('/create', methods=['GET', 'POST'])
def create_entry():
    if 'username' not in session:
        flash('Please log in first')
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('entry')
        username = session['username']
        datestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        new_entry = pd.DataFrame([{
            'username': username,
            'title': title,
            'entry': content,
            'datestamp': datestamp
        }])

        new_entry.to_sql('entries', con=ENTRIES_ENGINE.connect(), if_exists='append', index=False)
        return redirect(url_for('journal'))

    return render_template('create_entry.html')

@app.route('/entry/<int:entry_id>')
def view_entry(entry_id):
    if 'username' not in session:
        flash('Please log in first')
        return redirect(url_for('login'))

    entries_df = pd.read_sql('SELECT rowid as id, * FROM entries', con=ENTRIES_ENGINE.connect())
    matched = entries_df[entries_df['id'] == entry_id]

    if matched.empty:
        flash('Entry not found.')
        return redirect(url_for('journal'))

    entry_data = matched.iloc[0].to_dict()
    return render_template('view_entry.html', entry=entry_data)

if __name__ == '__main__':
    app.run(port = 3000, debug=True)