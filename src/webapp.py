from flask import Flask, render_template, url_for, redirect, request, flash, session, send_from_directory
from werkzeug import secure_filename
import os
from errno import EPIPE


try:
    broken_pipe_exception = BrokenPipeError
except NameError:  # Python 2
    broken_pipe_exception = IOError


app = Flask(__name__)
app. secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,? RT '





@app.route("/")
def root():
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            flash("You are now logged in")
            session['logged_in'] = True
            
            return redirect(url_for('root'))
    return render_template('login.html', error=error)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    flash("You have log out, come soon")
    return root()


APP_ROOT = os.path.dirname(os.path.abspath(__file__))



@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'static/uploads')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
    flash("Upload complete.")
    return redirect(url_for('advert'))

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("static/uploads", filename)



@app.route("/advert")
def advert():
    if session['logged_in']:
       return render_template('newAdvert.html')

    else:
        flash("You need to log in to post adverts")
        return redirect(url_for('login'))

@app.route("/takeform", methods=['POST'])
def takeform():
    if request.method == 'POST':
        image_names = os.listdir('static/uploads')
        print(image_names)
        typeAdvert = request.form['typeAdvert']
        city = request.form['city']
        pzip = request.form['pzip']
        price = request.form['price']
        description = request.form['houseDescription']
        return render_template('advert1.html', description=description, typeAdvert=typeAdvert,
            city=city, pzip=pzip, image_names=image_names, price=price)


@app.route("/accountinfo", methods=['POST'])
def accountinfo():
    if request.method == 'POST':

        city = request.form['city']
        name = request.form['name']
        aboutme = request.form['aboutme']
        
        return render_template('accountinfo.html', 
            city=city, name=name, aboutme=aboutme)

@app.route("/advertsCatalogue")
def catalogue():

        return render_template('advertsCatalog.html')

@app.route("/individualAdv")
def individualAdv():
    typeAdvert="Rent"
    city = "Edinburgh"
    pzip = "EH1 1ER"
    price = "1000 pounds/month"
    image= 'flat1.jpg'
    description="This is the description of the flat number 1. This is just a sample without sense, just to test how it will be visible in the adverts subpage."
    return render_template('advertExample.html', description=description, typeAdvert=typeAdvert,
            city=city, pzip=pzip, price=price, image=image)

@app.route("/individualAdv2")
def individualAdv2():
    typeAdvert="Exchange"
    city = "Edinburgh"
    pzip = "EH16 4ER"
    price = "0"
    image= 'flat2.jpg'
    description="This is the description of the flat number 2. This is just a sample without sense, just to test how it will be visible in the adverts subpage."
    return render_template('advertExample.html', description=description, typeAdvert=typeAdvert,
            city=city, pzip=pzip, price=price, image=image)

@app.route("/individualAdv3")
def individualAdv3():
    typeAdvert="Rent"
    city = "Edinburgh"
    pzip = "EH3 1ER"
    price = "1400 pounds/month"
    image= 'flat3.jpg'
    description="This is the description of the flat number 3. This is just a sample without sense, just to test how it will be visible in the adverts subpage."
    return render_template('advertExample.html', description=description, typeAdvert=typeAdvert,
            city=city, pzip=pzip, price=price, image=image)




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


try:

    @app.route("/account1", methods=['POST','GET'])
    def account1():
        try:
            if session['logged_in']: 
                return render_template('account.html')
        except KeyError:
            pass
        flash("You need to log in to go to My Account")
        return redirect(url_for('login'))
        

        

except broken_pipe_exception as exc:
    if broken_pipe_exception == IOError:
        if exc.errno != EPIPE:
            raise

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
