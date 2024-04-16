from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response

import requests
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['PROFILE_FOLDER'] = 'profile_data'


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/stud_login', methods=['GET', 'POST'])
def stud_login():
    if request.method == 'POST':
        resp = requests.post(
            url='http://localhost:5000/api/login',
            json={'email': request.form['email'], 'password': request.form['pass']},
        )

        if resp.status_code == 200:
            resp = make_response(redirect(url_for('dashboard')))
            resp.set_cookie('email', request.form['email'])
            return resp
        else:
            return render_template('stud_login.html', login_error=resp.json()['error'])

    return render_template('stud_login.html')


@app.route('/profile', methods=['GET', "POST"])
def profile():
    if not request.cookies.get('email'):
        return redirect(url_for('stud_login'))

    if request.method == "POST":
        data = dict(request.form)

        ssc = request.files['10ms']
        hsc = request.files['12ms']
        fe = request.files['fe']
        se = request.files['se']
        te = request.files['te']
        be = request.files['be']
        data.update({
            "fe": fe.filename,
            "se": se.filename,
            "te": te.filename,
            "be": be.filename,
            "10ms": ssc.filename,
            "12ms": hsc.filename
        })
        try:
            os.mkdir(f"{app.config['PROFILE_FOLDER']}")
        except FileExistsError:
            pass
        try:
            os.mkdir(os.path.join(app.config['PROFILE_FOLDER'], data['email']))
        except FileExistsError:
            pass

        for file in request.files.values():
            file.save(os.path.join(app.config['PROFILE_FOLDER'], data['email'], file.filename))

        db.insert_info(data)
        return render_template('profile.html', data=data)

    info = db.get_info(request.cookies.get('email'))

    if info:
        return render_template('profile.html', data=info)

    return render_template('profile.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not request.cookies.get('email'):
        return redirect(url_for('stud_login'))

    job_offers = db.get_offers()

    return render_template('dashboard.html', offers=job_offers, enumerate=enumerate)


@app.route('/coordinator', methods=['GET', 'POST'])
def coordinator():
    if request.method == "POST":
        try:
            db.checck_user_password_coordinator(request.form['email'], request.form['password'])
        except DBException.UserDoesNotExists:
            return render_template('coordinator.html')

        resp = make_response(redirect(url_for('coordinatordash')))
        resp.set_cookie('coordinatoremail', request.form['email'])

        return resp

    return render_template('coordinator.html')


@app.route('/stat')
def stat():
    return render_template('stat.html')


@app.route('/register', methods=['POST'])
def register():
    try:
        db.insert_user({
            'name': request.form['name'],
            'email': request.form['email'],
            'password': request.form['password']
        })
    except DBException.UserAlreadyExists:
        return render_template('stud_login.html', signup_error="User already exists", sign_up=False)

    resp = make_response(render_template('stud_login.html', signup=True))
    resp.set_cookie('email', request.form['email'])

    return resp


@app.route('/coordinatordash', methods=['GET', 'POST'])
def coordinatordash():
    if request.method == "POST":
        db.insert_job_offer({
            'email': request.cookies.get('coordinatoremail'),
            'name': request.form['companyName'],
            'link': request.form['companyLocation'],
            'description': request.form['companyDescription'],
            'required_cgpa': request.form['previousYearCGPA'],
        })

        return render_template('coordinatordash.html')

    return render_template('coordinatordash.html')


@app.route('/careers', methods=['GET', 'POST'])
def careers():
    return render_template('careers.html')


@app.route('/faq', methods=['GET', 'POST'])
def faq():
    return render_template('faq.html')


@app.route('/testimonials', methods=['GET', 'POST'])
def test():
    return render_template('test.html')


# ===============
# API ROUTES
# ===============

@app.route('/api/login', methods=['POST'])
def api_login():
    email = request.json['email']
    password = request.json['password']

    try:
        db.check_user_password(email, password)
    except DBException.UserDoesNotExists:
        return jsonify({'error': 'Incorrect email or password'}), 401

    resp = make_response(jsonify({'email': email}), 200)
    resp.set_cookie('email', email)

    return resp


@app.route('/api/logout')
def logout():
    resp = make_response(redirect(url_for('stud_login')))
    resp.delete_cookie('email')
    return resp


if __name__ == '__main__':
    app.run(debug=True)
