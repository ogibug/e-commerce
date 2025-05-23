from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.mysql_models import mysql, create_user, get_user_by_email
from models.mongodb_models import mongo, get_all_products
from flask_bcrypt import Bcrypt
from config import *
import MySQLdb.cursors

app = Flask(__name__)
app.config.from_object('config')

mysql.init_app(app)
mongo.init_app(app)
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        user = get_user_by_email(cursor, email)
        
        if user and bcrypt.check_password_hash(user['password'], password):
            session['loggedin'] = True
            session['email'] = email
            return redirect(url_for('products'))
        else:
            flash('Hatalı giriş!')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        cursor = mysql.connection.cursor()
        create_user(cursor, email, password)
        mysql.connection.commit()

        flash('Başarıyla kayıt oldunuz!')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/products')
def products():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    products = get_all_products()
    return render_template('products.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
