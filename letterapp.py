from flask import Flask, request, send_file, redirect, url_for
from flask import render_template
from word import Word
import scraper
import pandas as pd
import offer_logic
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user
import re
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
load_dotenv()
import os
import subprocess
import MySQLdb
import sshtunnel

tunnel = sshtunnel.SSHTunnelForwarder(
    ('ssh.pythonanywhere.com', 22),
    ssh_username='khizar591', ssh_password='118562591.fF',
    remote_bind_address=('khizar591.mysql.pythonanywhere-services.com', 3306)
)
tunnel.start()
local_port = tunnel.local_bind_port

app  = Flask(__name__)
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@127.0.0.1:{hostname}/{databasename}".format(
    username="khizar591",
    password="dunhill246",
    hostname=local_port,
    databasename="khizar591$routes",
)
app.config['SECRET_KEY'] = "118562591"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=120)



db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'

class OfferLetter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_name = db.Column(db.String(50), nullable=False)
    offer_name = db.Column(db.String(200), nullable=False)
    file_name = db.Column(db.String(100), nullable=False)
    offer_type = db.Column(db.String(50), nullable=False)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(250))


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# with app.app_context():
#     df = pd.read_excel("Offers.xlsx")
#     for index, row in df.iterrows():
#         offers = OfferLetter(
#             property_name=row['HotelName'],
#             offer_name = row['OfferName'],
#             file_name = row['FilePath'],
#             offer_type = row['Offer Type']
#             )
#         db.session.add(offers)
#         db.session.commit()



@app.route('/', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    if request.method == "POST":
        user_name = request.form.get("email")
        password = request.form.get("password")
        user  = Users.query.filter_by(username=user_name).first()
        if user:
            correct_password = check_password_hash(user.password,password)
            if correct_password:
                login_user(user)
                return redirect(url_for('homepage'))
            else:
                pass
    return render_template('signin.html')



@app.route('/get_rates')
def rates():
    property_name = request.args.get("hotel")
    check_in = request.args.get("checkin")
    check_out = request.args.get("checkout")
    str_checkin = datetime.strptime(check_in, "%m/%d/%y")
    str_checkout = datetime.strptime(check_out, "%m/%d/%y")
    df = scraper.get_html(property_name,str_checkin, str_checkout)
    rates = df['rate_name'].unique().tolist()
    return {"rates":rates}

@app.route('/home', methods=['GET', 'POST'])
@login_required
def homepage():
    textual_sql_statement = text('Select Distinct offer_name from offer_letter;')
    rate_type = db.session.execute(textual_sql_statement).scalars().all()
    if request.method =='POST':
        guest_name = request.form.get('Guest Name')
        hotel = request.form.get('property')
        check_in_date = datetime.strptime(request.form.get('check-in'),"%Y-%m-%d")
        nights = int(request.form.get('room-nights'))
        check_out_date = check_in_date + timedelta(days=nights)
        offer_type = request.form.get('offer-type')
        rate_name = request.form.get('rate-name')
        discount = request.form.get('discount')
        adults = request.form.get('adults')
        text_sql = text(f'SELECT file_name FROM offer_letter WHERE property_name = "{hotel}" AND offer_name = "{rate_name}" AND offer_type="{offer_type}"')
        path = db.session.execute(text_sql).scalar()
        file = offer_logic.generate(
            hotel,
            check_in_date,
            check_out_date,
            offer_type,
            rate_name,
            discount,
            guest_name,
            "Offer_Letter_Website/"+path,
            adults
        )
        filename= f"{file}.docx"
        cmd = ["libreoffice", "--headless","--convert-to", "pdf","--outdir","/home/khizar591/Offer_Letter_Website/pdf",f"/home/khizar591/Offer_Letter_Website/word/{filename}"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stderr.decode())
        return send_file(f"pdf/{file}.pdf",as_attachment=True)
    return render_template('homepage.html', rates=rate_type)



if __name__ == "__main__":
    app.run(debug=True)