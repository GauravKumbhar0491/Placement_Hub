from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/stud_login')
def stud_login():
    return render_template('stud_login.html', error_html="<p style='color: red'>ERROR</p>")

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/coordinator')
def coordinator():
    return render_template('coordinator.html')

@app.route('/stat')
def stat():
    return render_template('stat.html')



if __name__ == '__main__':
    app.run(debug=True)
