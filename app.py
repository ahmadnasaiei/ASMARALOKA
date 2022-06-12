from http.client import FORBIDDEN
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_paginate import Pagination, get_page_args
from flask_mysqldb import MySQL, MySQLdb
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
import fontawesome as fa


app = Flask(__name__)
app.secret_key = "membuatLOginFlask1"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost:3307/asmaraloka'
db = SQLAlchemy(app)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


# @login_manager.user_loader
# def load_user(user_id):
#     if session['account_type'] == 'client':
#         return Client.query.filter_by(client_ID=user_id).first()
#     elif session['account_type'] == 'agent':
#         return Agent.query.filter_by(agent_ID=user_id).first()
#     else:
#         return None


@login_manager.user_loader
def load_user(user_id):
    return Client.query.filter_by(client_ID=user_id).first()


# @login_manager.user_loader
# def load_user(user_id):
#     return Agent.query.filter_by(agent_ID=user_id).first()


class Client(db.Model, UserMixin):
    client = "parents"
    client_ID = db.Column(db.Integer, primary_key=True)
    client_First_Name = db.Column(db.String(255),)
    client_Last_Name = db.Column(db.String(255),)
    client_Email = db.Column(db.String(255))
    client_Password = db.Column(db.String(255))
    client_Phone_No = db.Column(db.String(255))
    client_Address = db.Column(db.String(255))
    account_type = db.Column(db.String(255))
    childrens = db.relationship("child", backref="parents"),
    cascade = "all, delete"
    #customer = db.relationship('Client', backref='feedback', lazy=True)

    def get_id(self):
        return (self.client_ID)

    def __init__(self, client_First_Name, client_Last_Name, client_Email, client_Password, client_Phone_No, client_Address, account_type):
        self.client_First_Name = client_First_Name
        self.client_Last_Name = client_Last_Name
        self.client_Email = client_Email
        self.client_Password = client_Password
        self.client_Phone_No = client_Phone_No
        self.client_Address = client_Address
        self.account_type = account_type


class Agent(db.Model, UserMixin):
    agent = "parents"
    agent_ID = db.Column(db.Integer, primary_key=True)
    agent_First_Name = db.Column(db.String(255))
    agent_Last_Name = db.Column(db.String(255))
    agent_Email = db.Column(db.String(255))
    agent_Password = db.Column(db.String(255))
    agent_Phone_No = db.Column(db.String(255))
    agent_REN_No = db.Column(db.String(255))
    agent_Agency = db.Column(db.String(255))
    account_type = db.Column(db.String(255))
    childrens = db.relationship("child", backref="parents"),
    cascade = "all, delete"

    def get_id(self):
        return (self.agent_ID)

    def __init__(self, agent_First_Name, agent_Last_Name, agent_Email, agent_Password, agent_Phone_No, agent_REN_No, agent_Agency, account_type):
        self.agent_First_Name = agent_First_Name
        self.agent_Last_Name = agent_Last_Name
        self.agent_Email = agent_Email
        self.agent_Password = agent_Password
        self.agent_Phone_No = agent_Phone_No
        self.agent_REN_No = agent_REN_No
        self.agent_Agency = agent_Agency
        self.account_type = account_type


class Property(db.Model):
    property = "children"
    property_ID = db.Column(db.Integer, primary_key=True)
    property_Title = db.Column(db.String(255))
    property_District = db.Column(db.String(255))
    property_State = db.Column(db.String(255))
    property_Price = db.Column(db.Integer)
    property_Sqft = db.Column(db.String(255))
    property_Bedroom = db.Column(db.String(255))
    property_Bathroom = db.Column(db.String(255))
    agent_ID = db.Column(db.Integer, db.ForeignKey(
        'agent.agent_ID'), nullable=False)

    def __init__(self, property_Title, property_District, property_State, property_Price, property_Sqft, property_Bedroom, property_Bathroom, agent_ID):
        self.property_Title = property_Title
        self.property_District = property_District
        self.property_State = property_State
        self.property_Price = property_Price
        self.property_Sqft = property_Sqft
        self.property_Bedroom = property_Bedroom
        self.property_Bathroom = property_Bathroom
        self.agent_ID = agent_ID


class scrape_property(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    property_Title = db.Column(db.String(255))
    property_District = db.Column(db.String(255))
    property_State = db.Column(db.String(255))
    property_Price = db.Column(db.Integer)
    property_Sqft = db.Column(db.String(255))
    property_Bedroom = db.Column(db.String(255))
    property_Bathroom = db.Column(db.String(255))
    property_Origin_URL = db.Column(db.String(255))

    def __init__(self, property_Title, property_District, property_State, property_Price, property_Sqft, property_Bedroom, property_Bathroom, property_Origin_URL):
        self.property_Title = property_Title
        self.property_District = property_District
        self.property_State = property_State
        self.property_Price = property_Price
        self.property_Sqft = property_Sqft
        self.property_Bedroom = property_Bedroom
        self.property_Bathroom = property_Bathroom
        self.property_Origin_URL = property_Origin_URL


class Booking(db.Model):
    booking = "children"
    booking_ID = db.Column(db.Integer, primary_key=True)
    booking_Date = db.Column(db.DateTime, default=datetime.utcnow)
    booking_Time = db.Column(db.DateTime)
    client_ID = db.Column(db.Integer, db.ForeignKey(
        'client.client_ID'), nullable=False)

    def __init__(self, booking_Date, booking_Time, client_ID):
        self.booking_Date = booking_Date
        self.booking_Time = booking_Time
        self.client_ID = client_ID


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/agentDashboard')
def agentDashboard():
    return render_template('agentDashboard.html')


@app.route('/clientDashboard')
def clientDashboard():
    return render_template('clientDashboard.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/clientLoggedIn')
# @login_required()
def clientLoggedIn():
    return render_template('clientLoggedIn.html', user=current_user)


@app.route('/clientAccount')
def clientAccount():
    return render_template('clientAccount.html')


@app.route('/agentUpdateAccount')
def agentUpdateAccount():
    return render_template('agentUpdateAccount.html')


@app.route('/propertyDetails')
def propertyDetails():
    return render_template('propertyDetails.html')


@app.route('/properties')
def properties():
    property_data = Property.query.all()
    scrape_data = scrape_property.query.all()
    return render_template("properties.html", agent_property=property_data, scrape_property=scrape_data)


@app.route('/registerClient', methods=['POST', 'GET'])
def registerClient():
    if request.method == 'POST':
        try:
            db.session.add(Client(client_First_Name=request.form['client_First_Name'], client_Last_Name=request.form['client_Last_Name'], client_Email=request.form['client_Email'],
                           client_Password=request.form['client_Password'], client_Phone_No=request.form['client_Phone_No'], client_Address=request.form['client_Address'], account_type=request.form['account_type']))
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return render_template('index.html')
    else:
        return render_template('clientRegister.html')


@app.route('/registerAgent', methods=['POST', 'GET'])
def registerAgent():
    if request.method == 'POST':
        try:
            db.session.add(Agent(agent_First_Name=request.form['agent_First_Name'], agent_Last_Name=request.form['agent_Last_Name'], agent_Email=request.form['agent_Email'],
                           agent_Password=request.form['agent_Password'], agent_Phone_No=request.form['agent_Phone_No'], agent_REN_No=request.form['agent_REN_No'], agent_Agency=request.form['agent_Agency'], account_type=request.form['account_type']))
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return render_template('index.html')
    else:
        return render_template('agentRegister.html')


@app.route('/loginClient', methods=['GET', 'POST'])
def loginClient():
    if request.method == 'POST':
        client_Email = request.form['client_Email']
        client_Password = request.form['client_Password']

        client = Client.query.filter_by(client_Email=client_Email).first()
        if client:
            if client.client_Password == client_Password:
                flash('Logged in successfully!', category='success')
                login_user(client)
                return redirect(url_for('clientLoggedIn'))
        else:
            flash('Invalid password or email. Please try again.', category='error')

    return render_template("clientLogin.html")


@app.route('/loginAgent', methods=['GET', 'POST'])
def loginAgent():
    if request.method == 'POST':
        agent_Email = request.form['agent_Email']
        agent_Password = request.form['agent_Password']
        agent = Agent.query.filter_by(agent_Email=agent_Email).first()
        if agent:
            if agent.agent_Password == agent_Password:
                login_user(agent)
                return redirect(url_for('agentDashboard'))
        else:
            return "invalid email or password"
    return render_template("agentLogin.html")


@app.route('/createProperty', methods=['POST', 'GET'])
def createProperty():
    if request.method == 'POST':
        try:
            db.session.add(Property(property_Title=request.form['property_Title'], property_District=request.form['property_District'], property_State=request.form['property_State'],
                           property_Price=request.form['property_Price'], property_Sqft=request.form['property_Sqft'], property_Bedroom=request.form['property_Bedroom'], property_Bathroom=request.form['property_Bathroom'], agent_ID=request.form['agent_ID']))
            db.session.commit()
            return redirect(url_for('createProperty'))
        except:
            return render_template('index.html')
    else:
        return render_template('agentCreateListing.html')


@app.route('/updateClient/<int:client_ID>', methods=['GET', 'POST'])
def updateClient(client_ID):
    all_data = Client.query.all()
    client_to_update = Client.query.filter_by(client_ID=client_ID).first()
    if request.method == 'POST':
        client_to_update.client_First_Name = request.form['client_First_Name']
        client_to_update.client_Last_Name = request.form['client_Last_Name']
        client_to_update.client_Email = request.form['client_Email']
        client_to_update.client_Password = request.form['client_Password']
        client_to_update.client_Phone_No = request.form['client_Phone_No']
        client_to_update.client_Address = request.form['client_Address']
        client_to_update.account_type = request.form['account_type']
        client_to_update.client = Client(client_First_Name=client_to_update.client_First_Name, client_Last_Name=client_to_update.client_Last_Name,
                                         client_Email=client_to_update.client_Email, client_Password=client_to_update.client_Password, client_Phone_No=client_to_update.client_Phone_No, client_Address=client_to_update.client_Address, account_type=client_to_update.account_type)

        db.session.commit()
        return redirect('/clientAccount')

    return render_template('clientUpdateAccount.html', client_to_update=client_to_update, client=all_data)


@app.route('/updateAgent/<int:agent_ID>', methods=['GET', 'POST'])
def updateAgent(agent_ID):
    all_data = Agent.query.all()
    agent_to_update = Agent.query.filter_by(agent_ID=agent_ID).first()
    if request.method == 'POST':
        agent_to_update.agent_First_Name = request.form['agent_First_Name']
        agent_to_update.agent_Last_Name = request.form['agent_Last_Name']
        agent_to_update.agent_Email = request.form['agent_Email']
        agent_to_update.agent_Password = request.form['agent_Password']
        agent_to_update.agent_Phone_No = request.form['agent_Phone_No']
        agent_to_update.agent_REN_No = request.form['agent_REN_No']
        agent_to_update.agent_Agency = request.form['agent_Agency']
        agent_to_update.account_type = request.form['account_type']
        agent_to_update.agent = Agent(agent_First_Name=agent_to_update.agent_First_Name, agent_Last_Name=agent_to_update.agent_Last_Name,
                                      agent_Email=agent_to_update.agent_Email, agent_Password=agent_to_update.agent_Password, agent_Phone_No=agent_to_update.agent_Phone_No, agent_REN_No=agent_to_update.agent_REN_No, agent_Agency=agent_to_update.agent_Agency, account_type=agent_to_update.account_type)

        db.session.commit()
        return redirect('/agentDashboard')

    return render_template('agentUpdateAccount.html', agent_to_update=agent_to_update, agent=all_data)


@app.route('/updateProperty/<int:property_ID>', methods=['GET', 'POST'])
def updateProperty(property_ID):
    all_data = Property.query.all()
    property_to_update = Property.query.filter_by(
        property_ID=property_ID).first()
    if request.method == 'POST':
        property_to_update.property_Title = request.form['property_Title']
        property_to_update.property_District = request.form['property_District']
        property_to_update.property_State = request.form['property_State']
        property_to_update.property_Price = request.form['property_Price']
        property_to_update.property_Sqft = request.form['property_Sqft']
        property_to_update.property_Bedroom = request.form['property_Bedroom']
        property_to_update.property_Bathroom = request.form['property_Bathroom']
        property_to_update.agent_ID = request.form['agent_ID']
        property_to_update.property = Property(property_Title=property_to_update.property_Title, property_District=property_to_update.property_District,
                                               property_State=property_to_update.property_State, property_Price=property_to_update.property_Price, property_Sqft=property_to_update.property_Sqft, property_Bedroom=property_to_update.property_Bedroom, property_Bathroom=property_to_update.property_Bathroom, agent_ID=property_to_update.agent_ID)

        db.session.commit()
        return redirect('/agentAllListing')

    return render_template('agentUpdateProperty.html', property_to_update=property_to_update, agent=all_data)


@app.route('/agentAllListing')
def agentAllListing():
    agent_ID = current_user.agent_ID
    # all_data = scrape_property.query.all()
    result = db.engine.execute(
        "SELECT * FROM property WHERE agent_ID = %s", agent_ID)
    return render_template("agentAllListing.html", agent_property=result)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/deleteProperty/<int:property_ID>')
def deleteProperty(property_ID):
    property_to_delete = Property.query.get_or_404(property_ID)
    try:
        db.session.delete(property_to_delete)
        db.session.commit()
        return redirect('/agentAllListing')
    except:
        return "There was a problem deleting the property Please try again."


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
