from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/stud_login')
def stud_login():
    return render_template('stud_login.html', signup=request.args.get('signup', False))

@app.route('/profile', methods=['GET', "POST"])
def profile():
    if request.method == "POST":
        data = dict(request.form)
        
        ssc= request.files['10ms']
        hsc= request.files['12ms']
        fe= request.files['fe']
        se= request.files['se']
        te= request.files['te']
        be= request.files['be']
        data.update({
            "fe": fe.filename,
            "se": se.filename,
            "te": te.filename,
            "be": be.filename,
            "10ms": ssc.filename,
            "12ms": hsc.filename
        })
        print(data)
        return render_template('profile.html', data=data)
    else:
        return render_template('profile.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():      
    return render_template('dashboard.html')

@app.route('/coordinator')
def coordinator():
    return render_template('coordinator.html')

@app.route('/stat')
def stat():
    return render_template('stat.html')

@app.route('/register', methods=['POST'])
def register():
    print(request.form)
    return redirect(url_for('stud_login', signup=True))

@app.route('/coordinatordash', methods=['GET','POST'])
def coordinatordash():
    return render_template('coordinatordash.html')

@app.route('/careers', methods=['GET','POST'])
def careers():
    return render_template('careers.html')

@app.route('/faq', methods=['GET','POST'])
def faq():
    return render_template('faq.html')

@app.route('/testimonials', methods=['GET','POST'])
def test():
    return render_template('test.html')






if __name__ == '__main__':
    app.run(debug=True)
