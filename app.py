from flask import Flask,render_template,request,url_for,redirect,flash
import mysql.connector as connector
import uuid
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


db = connector.connect(host="localhost", user="root", passwd="root", database="Beadsprint")

# @app.route('/')
# def hello_world():
#     return 'Hello World!'


@app.route('/')
def navigation():
    return render_template('Home.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


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
                token = s.dumps(email, salt='email-confirm')
                print(email)
                cursor = db.cursor()
                token = uuid.uuid4().hex.upper()
                sql2 = "INSERT INTO `delivery`(`phone`, `email`) VALUES (%s,%s)"
                val = (phone, email)
                cursor.execute(sql2, val)
                db.commit()
                flash("will receive notification")
                page = render_template('delivery_output.html')

                msg = Message(subject='Order received', sender='earvinbaraka@gmail.com',
                              recipients=[request.form['email']])
                link = url_for('conf_email', token=token,page=page, _external=True)
                msg.body = render_template('sentmail.html', token=token, link=link)
                mail.send(msg)

                flash('Link sent to your Email')
            return redirect(url_for('navigation'))
        return render_template('funiture order.html')


@app.route('/conf_email/<token>')
def conf_email(token):
    try:
        email = s.loads(token, salt='email-confirm')
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    # return '<h1>The token works!</h1>'
    # return render_template('index.html')
    return redirect(url_for('navigation'))

if __name__ == '__main__':
    app.run()
