from flask import Flask, render_template, session, redirect, jsonify, request,url_for,current_app
from functools import wraps
from flask_pymongo import PyMongo
from passlib.hash import pbkdf2_sha256
import uuid

app = Flask(__name__)
app.secret_key = "abcd"
mongo_uri="mongodb+srv://debanjankonar:8vyBKDIuGm6P0vrM@cluster0.72482ea.mongodb.net/user_login_system"

mongo=PyMongo(app,mongo_uri)
# Database
db = mongo.db

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/home/')
def home():
  return render_template('home.html')

@app.route('/contact/')
def contact():
  return render_template('contact.html')

@app.route('/dashboard/')
@login_required
def dashboard():
  user=db.users.find_one({"_id": User().get_session()["_id"]})
  return render_template('dashboard.html',user=user)

@app.route('/user/signup', methods=['POST'])
def signup():
  return User().signup()

@app.route('/user/signout')
def signout():
  return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
  return User().login()


@app.post('/reset_pass/')
def change_wallet_pass():
    new_PIN=request.form.get('new_password')
    user=db.users.find_one({ "email": request.form.get('email') })
    if user!=None:
      db.users.update_one({'email':request.form.get('email')},{'$set':{'password':pbkdf2_sha256.encrypt(new_PIN),'Default':False}})
      return jsonify({"message":"success"}),200
    else:
      return jsonify({"message": "Invalid email address"}), 400
    

@app.post('/transfer/')
def transfer():

    data=request.get_json()
    phone_no=data["number"]
    password=data["pass"]
    amount=data["amount"]
    sender_id =User().get_session()["_id"]
    print(User().get_session()["name"])
    if not sender_id:
        return jsonify({"message": "User not authenticated"}), 405

    # Check if the amount is a valid float
    print(amount)
    print(phone_no)
    try:
        amount = float(amount)
        
    except (ValueError, TypeError):
        return jsonify({"message": "Invalid amount"}), 401

    sender = db.users.find_one({"_id": sender_id})
    receiver = db.users.find_one({"phone_no": phone_no})

    if sender is None or receiver is None:
        return jsonify({"message": "Invalid sender or receiver"}), 402

    if pbkdf2_sha256.verify(password, sender.get("password")):
        if sender["wallet_balance"] >= amount and amount>0 :
            new_sender_balance = sender["wallet_balance"] - amount
            new_receiver_balance = receiver["wallet_balance"] + amount

            # Use a MongoDB transaction to ensure both updates or none
            with db.client.start_session() as session:
                with session.start_transaction():
                    db.users.update_one({"_id": sender_id}, {"$set": {"wallet_balance": new_sender_balance}})
                    db.users.update_one({"phone_no": phone_no}, {"$set": {"wallet_balance": new_receiver_balance}})

            return jsonify({"message": "Success"}), 200
        else:
            return jsonify({"message": "Insufficient balance"}), 403
    else:
        return jsonify({"message": "Invalid password"}), 406



@app.post('/topup/')
def topup():

    data=request.get_json()
    amount=data["amount"]
    sender_id =User().get_session()["_id"]
    print(User().get_session()["name"])
    if not sender_id:
        return jsonify({"message": "User not authenticated"}), 405

    # Check if the amount is a valid float
    print(amount)
    try:
        amount = float(amount)
        
    except (ValueError, TypeError):
        return jsonify({"message": "Invalid amount"}), 401

    sender = db.users.find_one({"_id": sender_id})

    if sender is None:
        return jsonify({"message": "Invalid sender or receiver"}), 402

    new_sender_balance = sender["wallet_balance"] + amount

            # Use a MongoDB transaction to ensure both updates or none
    with db.client.start_session() as session:
          with session.start_transaction():
                    db.users.update_one({"_id": sender_id}, {"$set": {"wallet_balance": new_sender_balance}})
                    return jsonify({"message": "Success"}), 200



class User:

  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200
  
  def get_session(self):
    if 'logged_in' in session and session['logged_in']:
      return session['user']
    else:
      return jsonify({"message": "User not logged in"}), 401


  def signup(self):
    print(request.form)

    # Create the user object
    user = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "email": request.form.get('email'),
      "password": request.form.get('password'),
      "phone_no": request.form.get('phone_no'),
      "wallet_balance":100
    }

    # Encrypt the password
    user['password'] = pbkdf2_sha256.encrypt(user['password'])

    # Check for existing email address
    if db.users.find_one({ "email": user['email'] }):
      return jsonify({ "error": "Email address already in use" }), 400

    if db.users.insert_one(user):
      return self.start_session(user)

    return jsonify({ "error": "Signup failed" }), 400
  
  def signout(self):
    session.clear()
    return redirect('/')
  
  def login(self):

    user = db.users.find_one({
      "email": request.form.get('email')
    })

    if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
      return self.start_session(user)
    
    return jsonify({ "error": "Invalid login credentials" }), 401
  


if __name__ == "__main__":
    app.run(debug=True)