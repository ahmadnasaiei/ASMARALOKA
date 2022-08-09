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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost:3306/asmaraloka'
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


# @login_manager.user_loader
# def load_user(user_id):
#     return Client.query.filter_by(client_ID=user_id).first()


@login_manager.user_loader
def load_user(user_id):
    return Agent.query.filter_by(agent_ID=user_id).first()


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
    property_Address = db.Column(db.String(255))
    property_City = db.Column(db.String(255))
    property_State = db.Column(db.String(255))
    property_Zip = db.Column(db.String(255))
    property_Description = db.Column(db.String(255))
    property_Type = db.Column(db.String(255))
    property_Tenure = db.Column(db.String(255))
    property_Price = db.Column(db.Integer)
    property_Sqft = db.Column(db.String(255))
    property_Bedroom = db.Column(db.String(255))
    property_Bathroom = db.Column(db.String(255))
    agent_ID = db.Column(db.Integer, db.ForeignKey(
        'agent.agent_ID'), nullable=False)

    def __init__(self, property_Title, property_Address, property_City, property_Zip, property_Description, property_Type, property_Tenure, property_State, property_Price, property_Sqft, property_Bedroom, property_Bathroom, agent_ID):
        self.property_Title = property_Title
        self.property_Address = property_Address
        self.property_City = property_City
        self.property_State = property_State
        self.property_Zip = property_Zip
        self.property_Description = property_Description
        self.property_Type = property_Type
        self.property_Tenure = property_Tenure
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
    property_Image = db.Column(db.String(255))
    property_Origin_URL = db.Column(db.String(255))

    def __init__(self, property_Title, property_District, property_State, property_Price, property_Sqft, property_Bedroom, property_Bathroom, property_Image, property_Origin_URL):
        self.property_Title = property_Title
        self.property_District = property_District
        self.property_State = property_State
        self.property_Price = property_Price
        self.property_Sqft = property_Sqft
        self.property_Bedroom = property_Bedroom
        self.property_Bathroom = property_Bathroom
        self.property_Image = property_Image
        self.property_Origin_URL = property_Origin_URL


class Appointment(db.Model):
    appointment = "children"
    appointment_ID = db.Column(db.Integer, primary_key=True)
    appointment_Date = db.Column(db.DateTime, default=datetime.utcnow)
    client_ID = db.Column(db.Integer, db.ForeignKey(
        'client.client_ID'), nullable=False)
    property_ID = db.Column(db.Integer, db.ForeignKey(
        'property.property_ID'), nullable=False)

    def __init__(self, appointment_Date, client_ID, property_ID):
        self.appointment_Date = appointment_Date
        self.client_ID = client_ID
        self.property_ID = property_ID


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/agentDashboard')
def agentDashboard():
    return render_template('agentDashboard.html')



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


@app.route('/propertyDetails/<int:property_ID>')
def propertyDetails(property_ID):
    all_data = Property.query.all()
    property_to_view = Property.query.filter_by(
        property_ID=property_ID).first()
    return render_template('propertyDetails.html', property_to_view=property_to_view, property_data=all_data)


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
            db.session.add(Property(property_Title=request.form['property_Title'], property_Address=request.form['property_Address'], property_City=request.form['property_City'], property_State=request.form['property_State'], property_Zip=request.form['property_Zip'], property_Description=request.form['property_Description'], property_Type=request.form['property_Type'], property_Tenure=request.form['property_Tenure'],
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
        property_to_update.property_Address = request.form['property_Address']
        property_to_update.property_City = request.form['property_City']
        property_to_update.property_State = request.form['property_State']
        property_to_update.property_Zip = request.form['property_Zip']
        property_to_update.property_Description = request.form['property_Description']
        property_to_update.property_Type = request.form['property_Type']
        property_to_update.property_Tenure = request.form['property_Tenure']
        property_to_update.property_Price = request.form['property_Price']
        property_to_update.property_Sqft = request.form['property_Sqft']
        property_to_update.property_Bedroom = request.form['property_Bedroom']
        property_to_update.property_Bathroom = request.form['property_Bathroom']
        property_to_update.agent_ID = request.form['agent_ID']
        property_to_update.property = Property(property_Title=property_to_update.property_Title, property_Address=property_to_update.property_Address,
                                               property_City=property_to_update.property_City, property_State=property_to_update.property_State, property_Zip=property_to_update.property_Zip, property_Description=property_to_update.property_Description, property_Type=property_to_update.property_Type, property_Tenure=property_to_update.property_Tenure, property_Price=property_to_update.property_Price, property_Sqft=property_to_update.property_Sqft, property_Bedroom=property_to_update.property_Bedroom, property_Bathroom=property_to_update.property_Bathroom, agent_ID=property_to_update.agent_ID)
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


@app.route('/agentAllAppointment')
def agentAllAppointment():
    agent_ID = current_user.agent_ID
    result = db.engine.execute(
        "SELECT client.client_ID, client.client_First_Name, client.client_Last_Name, client.client_Phone_No, appointment.appointment_ID, appointment.appointment_Date, property.property_Title, property.property_ID, property.agent_ID FROM ((appointment INNER JOIN client ON client.client_ID = appointment.client_ID) INNER JOIN property ON appointment.property_ID = property.property_ID)  WHERE property.agent_ID = %s", agent_ID)
    return render_template("agentAllAppointment.html", agent_appointment=result)


@app.route('/clientAllAppointment')
def clientAllAppointment():
    client_ID = current_user.client_ID
    result = db.engine.execute("SELECT agent.agent_First_Name, agent.agent_Last_Name, agent.agent_Phone_No, property.property_Title, appointment.appointment_Date FROM agent INNER JOIN property ON agent.agent_ID = property.agent_ID INNER JOIN appointment ON property.property_ID = appointment.property_ID WHERE appointment.client_ID = %s", client_ID)
    return render_template("clientAllAppointment.html", client_appointment=result)


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


@app.route('/createAppointment', methods=['POST', 'GET'])
def createAppointment():
    if request.method == 'POST':
        try:
            db.session.add(Appointment(appointment_Date=request.form['appointment_Date'], client_ID=request.form['client_ID'], property_ID=request.form['property_ID']))
            db.session.commit()
            return redirect(url_for('properties'))
        except:
            return redirect(url_for('properties'))
    else:
        return render_template('index.html')


@app.route('/updateAppointment/<int:appointment_ID>', methods=['GET', 'POST'])
def updateAppointment(appointment_ID):
    agent_ID = current_user.agent_ID
    result = db.engine.execute(
        "SELECT client.client_ID, client.client_First_Name, client.client_Last_Name, client.client_Phone_No, appointment.appointment_ID, appointment.appointment_Date, property.property_Title, property.property_ID, property.agent_ID FROM ((appointment INNER JOIN client ON client.client_ID = appointment.client_ID) INNER JOIN property ON appointment.property_ID = property.property_ID)  WHERE property.agent_ID = %s", agent_ID)
    appointment_to_update = Appointment.query.filter_by(appointment_ID=appointment_ID).first()
    if request.method == 'POST':
        appointment_to_update.appointment_Date = request.form['appointment_Date']
        appointment_to_update.client_ID = request.form['client_ID']
        appointment_to_update.property_ID = request.form['property_ID']
        appointment_to_update.appointment = Appointment(appointment_Date=appointment_to_update.appointment_Date, client_ID=appointment_to_update.client_ID, property_ID=appointment_to_update.property_ID)
        db.session.commit()
        return redirect('/agentAllAppointment')

    return render_template('agentUpdateAppointment.html', appointment_to_update=appointment_to_update, client_data=result)


@app.route('/deleteAppointment/<int:appointment_ID>')
def deleteAppointment(appointment_ID):
    appointment_to_delete = Appointment.query.get_or_404(appointment_ID)
    try:
        db.session.delete(appointment_to_delete)
        db.session.commit()
        return redirect('/agentAllAppointment')
    except:
        return "There was a problem deleting the property Please try again."


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
