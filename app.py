from flask import Flask,render_template,request,url_for,redirect,flash
import mysql.connector as connector
import uuid
from mailchimp import Mailchimp
import mailchimp
from flask_mail import Message, Mail
from itsdangerous import URLSafeSerializer, SignatureExpired
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'earvinbaraka@gmail.com'
app.config['MAIL_PASSWORD'] = 'Commandprompt.1'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.secret_key = 'super secret key'
s = URLSafeSerializer('secretthistime!')


db = connector.connect(host="localhost", user="root", passwd="", database="beads")

# @app.route('/')
# def hello_world():
#     return 'Hello World!'


@app.route('/')
def navigation():
    return render_template('Home.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/delivery')
def charges():
    # if session.get('names') == None:
    #     return redirect(url_for('login'))
    cursor = db.cursor(buffered=True)
    sql = "SELECT * FROM `furniture` "
    # sql2 = "UPDATE transactions SET d_returned = CURDATE();"
    cursor.execute(sql)
    delivery = cursor.fetchall()
    return render_template('delivery_output.html', delivery=delivery)


@app.route('/funitureorder', methods=['POST', 'GET'])
def contact():
    # form = ContactForm()
    # if form.validate_on_submit():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            rental = request.form["rental"]
            quantity = request.form['quantity']

            print(name, email, rental, quantity)
            cursor = db.cursor()
            sql = "INSERT INTO `furniture`(`name`, `email`,`rental`, `quantity`) VALUES (%s,%s,%s,%s)"
            val = (name, email,rental,quantity)
            cursor.execute(sql, val)
            db.commit()
            flash("saved in database")
            if sql:
                email = request.form['email']
                phone = request.form['phone']
                apiKey = 'bde35c865cb5d38188ca0a60e3e3e538-us20';
                listID = '38df0e7c26';

                api = mailchimp.Mailchimp(apiKey)
                api.lists.subscribe(listID, {'email': 'earvinbaraka@gmail.com'})


                print(email)
                cursor = db.cursor()
                sql2 = "INSERT INTO `delivery`(`phone`, `email`) VALUES (%s,%s)"
                val = (phone, email)
                cursor.execute(sql2, val)
                db.commit()
                flash("will receive notification")

                flash('Link sent to your Email')
            return redirect(url_for('navigation'))
        return render_template('funiture order.html')



if __name__ == '__main__':
    app.run()
