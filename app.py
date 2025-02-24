from flask import Flask, render_template, request, redirect, url_for, flash,session, send_file
import pandas as pd
import os

app = Flask(__name__)
FILE_PATH = "/tmp/user_data.xlsx"

app.secret_key = "your_secret_key"
def save_to_excel(data):
    if os.path.exists(FILE_PATH):
        df = pd.read_excel(FILE_PATH, engine='openpyxl')
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    else:
        df = pd.DataFrame([data])

    df.to_excel(FILE_PATH, index=False, engine='openpyxl')


@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_data = {
            "Name": request.form['name'],
            "Email": request.form['email'],
            "Phone": request.form['phone']
        }
        save_to_excel(user_data)  # Call only once

        return render_template('registration.html', data="Saved Successfully!")

    return render_template('registration.html')

@app.route('/data')
def view_data():
    if os.path.exists(FILE_PATH):
        df = pd.read_excel(FILE_PATH)
        data = df.to_dict(orient='records')
    else:
        data = []
    return render_template('data.html', data=data)

@app.route('/download')
def download():
    if os.path.exists(FILE_PATH):
        return send_file(FILE_PATH, as_attachment=True)
    return "No data available to download", 404
    
ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "admin123"
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['user'] = {"Name": "Admin", "Email": ADMIN_EMAIL}
            # flash("Admin Login Successful!", "success")
            return redirect(url_for('view_data'))
        else:
            return render_template('login.html',inavlid_message="Invalid email or password!")
    
    return render_template('login.html')
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
