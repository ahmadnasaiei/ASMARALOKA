from http.client import FORBIDDEN
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from flask_mysqldb import MySQL, MySQLdb
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
import fontawesome as fa


app = Flask(__name__)
app.secret_key = "membuatLOginFlask1"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost:3307/asmaraloka'
db = SQLAlchemy(app)

#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_PORT'] = '3306'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'fypDB'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#mysql = MySQL(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Client(db.Model):
    client = "parents"
    client_ID = db.Column(db.Integer, primary_key=True)
    client_First_Name = db.Column(db.String(255),)
    client_Last_Name = db.Column(db.String(255),)
    client_Email = db.Column(db.String(255))
    client_Password = db.Column(db.String(255))
    client_Phone_No = db.Column(db.String(255))
    client_Address = db.Column(db.String(255))
    childrens = db.relationship("child", backref="parents"),
    cascade = "all, delete"
   #customer = db.relationship('Client', backref='feedback', lazy=True)

    def __init__(self, client_First_Name, client_Last_Name, client_Email, client_Password, client_Phone_No, client_Address):
        self.client_First_Name = client_First_Name
        self.client_Last_Name = client_Last_Name
        self.client_Email = client_Email
        self.client_Password = client_Password
        self.client_Phone_No = client_Phone_No
        self.client_Address = client_Address


class Agent(db.Model):
    agent_ID = db.Column(db.Integer, primary_key=True)
    agent_First_Name = db.Column(db.String(255))
    agent_Last_Name = db.Column(db.String(255))
    agent_Email = db.Column(db.String(255))
    agent_Password = db.Column(db.String(255))
    agent_Phone_No = db.Column(db.String(255))
    agent_REN_No = db.Column(db.String(255))
    agent_Agency = db.Column(db.String(255))

    def __init__(self, agent_First_Name, agent_Last_Name, agent_Email, agent_Password, agent_Phone_No, agent_REN_No, agent_Agency):
        self.agent_First_Name = agent_First_Name
        self.agent_Last_Name = agent_Last_Name
        self.agent_Email = agent_Email
        self.agent_Password = agent_Password
        self.agent_Phone_No = agent_Phone_No
        self.agent_REN_No = agent_REN_No
        self.agent_Agency = agent_Agency


class Booking(db.Model):
    booking_ID = db.Column(db.Integer, primary_key=True)
    booking_Date = db.Column(db.DateTime, default=datetime.utcnow)
    booking_Time = db.Column(db.DateTime)

    def __init__(self, booking_Date, booking_Time):
        self.booking_Date = booking_Date
        self.booking_Time = booking_Time


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registerClient', methods=['POST', 'GET'])
def registerClient():
    if request.method == 'POST':
        try:
            db.session.add(Client(client_First_Name=request.form['client_First_Name'], client_Last_Name=request.form['client_Last_Name'], client_Email=request.form['client_Email'],
                           client_Password=request.form['client_Password'], client_Phone_No=request.form['client_Phone_No'], client_Address=request.form['client_Address']))
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return render_template('index.html')
    else:
        return render_template('agentDashboard.html')


@app.route('/registerAgent', methods=['POST', 'GET'])
def registerAgent():
    if request.method == 'POST':
        try:
            db.session.add(Agent(agent_First_Name=request.form['agent_First_Name'], agent_Last_Name=request.form['agent_Last_Name'], agent_Email=request.form['agent_Email'],
                           agent_Password=request.form['agent_Password'], agent_Phone_No=request.form['agent_Phone_No'], agent_REN_No=request.form['agent_REN_No'], agent_Agency=request.form['agent_Agency']))
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return render_template('index.html')
    else:
        return render_template('agentRegister.html')


@app.route('/home')
def home():
    if session.get('logged_in'):

        print("ID YANG DAH PASS")

        return render_template('home.html')
    else:
        return render_template('index.html')


@app.route('/selfbuildin')
def selfbuildin():
    return render_template("product-self1.html")


@app.route('/question')
def question():
    if session.get('logged_in'):
        return render_template('question.html')
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html',)
    else:
        c = request.form['custEmail']
        p = request.form['custPass']
        data = Client.query.filter_by(custEmail=c, custPass=p).first()
        if data is not None:
            session['logged_in'] = True
            print("dah login ke")
            print(session)
            return redirect(url_for('home'))
            return render_template('home.html')
        else:
            return redirect(url_for('login'))
            return render_template('login.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session.pop('customer',None)
#         p = request.form['custPass']
#         data = Client.query.filter_by(custPass =p).first()
#         if request.form['custPass'] == data:
#             session['customer'] = request.form['custEmail']
#             print (session)
#             return redirect(url_for('protected'))

#     return render_template('login.html')

# @app.route('/protected')
# def protected():
#     if g.customer:
#         return render_template('home.html', customer=session['customer'])
#     return redirect(url_for('index'))

# @app.before_request
# def before_request():
#     g.customer = None

#     if 'customer' in session:
#         g.customer = session['customer']


@app.route('/loginAgent', methods=['GET', 'POST'])
def loginAgent():
    if request.method == 'GET':
        return render_template('loginAgent.html')
    else:
        c = request.form['adminEmail']
        p = request.form['adminPass']
        data = Agent.query.filter_by(adminEmail=c, adminPass=p).first()
        if data is not None:
            session['logged_in'] = True
            return redirect(url_for('allcust'))
            return render_template('home.html')
        else:
            return redirect(url_for('loginAgent'))
            return render_template('loginAgent.html')


@app.route('/about')
def about():
    if session.get('logged_in'):
        return render_template('about.html')
    else:
        return render_template('index.html')


@app.route('/aboutbeforelogin')
def aboutbeforelogin():
    return render_template('aboutbeforelogin.html')


@app.route('/contact')
def contact():
    if session.get('logged_in'):
        return render_template('contact.html')
    else:
        return render_template('index.html')


@app.route('/myfeedback')
def myfeedback():

    if session.get('logged_in'):
        result = db.engine.execute(
            "SELECT * FROM feedbacks WHERE custEmail = custemail")
        #all_data = text('SELECT feedbacks.fbID,customer.custID,customer.custName,feedbacks.fbType,feedbacks.fbDesc FROM feedbacks INNER JOIN customer ON (feedbacks.fbID = customer.custID)')
        #all_data = Feedbacks.query.all()
        return render_template("myfeedback.html", feedbacks=result)
    else:
        return render_template('index.html')


@app.route('/contactbeforelogin')
def contactbeforelogin():
    return render_template("contactbeforelogin.html")


@app.route('/insert')
def insert():
    if request.method == 'POST':

        custName = request.form['custName']
        custEmail = request.form['custEmail']
        custPhoneNo = request.form['custPhoneNo']
        custAdd = request.form['custAdd']
        custPass = request.form['custPass']

        my_data = Client(custName, custEmail, custPhoneNo, custAdd, custPass)
        db.session.add(my_data)
        db.session.commit()
        return redirect(url_for('home'))


@app.route('/productself1')
def productself1():
    if session.get('logged_in'):
        return render_template('productself1.html')
    else:
        return render_template('index.html')


@app.route('/allcust')
def allcust():
    if session.get('logged_in'):
        all_data = Client.query.all()
        return render_template("allcust.html", customer=all_data)
    else:
        return render_template('index.html')


@app.route('/feedbacks')
def feedbacks():
    if session.get('logged_in'):
        result = db.engine.execute(
            "SELECT feedbacks.fbID,customer.custEmail,customer.custName,feedbacks.fbType,feedbacks.fbDate,feedbacks.fbDesc FROM feedbacks INNER JOIN customer ON (feedbacks.custEmail = customer.custEmail)")
        #all_data = text('SELECT feedbacks.fbID,customer.custID,customer.custName,feedbacks.fbType,feedbacks.fbDesc FROM feedbacks INNER JOIN customer ON (feedbacks.fbID = customer.custID)')
        #all_data = Feedbacks.query.all()
        return render_template("feedbacks.html", feedbacks=result)
    else:
        return render_template('index.html')


@app.route('/complaints')
def complaints():
    if session.get('logged_in'):
        result = db.engine.execute(
            "SELECT feedbacks.fbID,customer.custEmail,customer.custName,feedbacks.fbType,feedbacks.fbDate,feedbacks.fbDesc FROM feedbacks INNER JOIN customer ON (feedbacks.custEmail = customer.custEmail) WHERE fbType = 'Complain'")
        return render_template("complaints.html", complaints=result)
    else:
        return render_template('index.html')


@app.route('/suggestions')
def suggestions():
    if session.get('logged_in'):
        result = db.engine.execute(
            "SELECT feedbacks.fbID,customer.custEmail,customer.custName,feedbacks.fbType,feedbacks.fbDate,feedbacks.fbDesc FROM feedbacks INNER JOIN customer ON (feedbacks.custEmail = customer.custEmail) WHERE fbType = 'Suggestion'")
        return render_template("suggestions.html", suggestions=result)
    else:
        return render_template('index.html')


@app.route('/reviews')
def reviews():
    if session.get('logged_in'):
        result = db.engine.execute(
            "SELECT feedbacks.fbID,customer.custEmail,customer.custName,feedbacks.fbType,feedbacks.fbDate,feedbacks.fbDesc FROM feedbacks INNER JOIN customer ON (feedbacks.custEmail = customer.custEmail) WHERE fbType = 'Review'")
        return render_template("reviews.html", reviews=result)
    else:
        return render_template('index.html')


@app.route('/component')
def component():
    if session.get('logged_in'):
        result = db.engine.execute(
            "SELECT component.compID,category.catName,component.compName,component.compBrand,component.compPrice FROM component INNER JOIN category ON (component.catID = category.catID) ORDER BY 1 ")
        return render_template("component.html", component=result)
    else:
        return render_template('index.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
