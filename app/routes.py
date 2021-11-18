from app import app, db, users, institutions
from app.dataConsumer import consumingDataPerDate as dpd
from app.initials import initialsToState
from app.news import callGoogle
# from app.models import User as u,Instituicao as inst, UserSchema
from datetime import date, timedelta
import json
import bcrypt
from flask_restful import Api, Resource, reqparse
# from flask_cors import CORS #comment this on deployment
from flask import redirect, url_for, request, jsonify, render_template, session
from sqlalchemy.exc import IntegrityError


defaultDay = date.today()-timedelta(days=1)
defaultDay = defaultDay.strftime("%m-%d-%Y")

# CORS(app) #comment this on deployment
api = Api(app)


@app.route('/', methods=['post', 'get'])
def index():
    print('tezte nyebjfasdjfa feua')
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        user_found = users.find_one({"name": user})
        email_found = users.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            users.insert_one(user_input)
            
            user_data = users.find_one({"email": email})
            new_email = user_data['email']
   
            return render_template('logged_in.html', email=new_email)
    return render_template('index.html')

@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('logged_in.html', email=email)
    else:
        return redirect(url_for("login"))
# @app.route('/api/state/<string:state>')
# @app.route('/api/state/<string:state>/<string:day>')
# def showState(state,day=defaultDay):
#     state = state.upper()
#     data = dpd(day)
#     return str(data[state])

# @app.route('/api/date')
# @app.route('/api/date/<string:day>')
# def showDate(day=defaultDay):
#     data = dpd(day)
#     #import ipdb; ipdb.set_trace()
#     return str(data)


@app.route('/api/news')
@app.route('/api/news/<string:state>')
def showNews(state='Brasil'):
    state = state.upper()
    if state not in initialsToState:
        state = 'Brasil'
    else:
        state = initialsToState[state]
    return str(callGoogle(state))

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class User(Resource):
    def get (self):
        print('teste')
        all_users = u.query.all()
        return jsonify(users_schema.dump(all_users))
        # return jsonify(result)

api.add_resource(User, '/api/user')


class UserById(Resource):
    def get (self,id):
        print('teste')
        user = u.query.filter_by(id=id)
        return jsonify(user_schema.dump(user))

api.add_resource(UserById, '/api/user/<string:id>')


class Instituicao(Resource):
    def get (self):
        instituicao = inst.query.all()
        return instituicao 

    def post (self):
        try:
            name = request.json.get('name', None)
            email = request.json.get('email', None)
            address = request.json.get('address', None)
            url = request.json.get('url', None)
            phone_number = request.json.get('phone_number', None)

            instituicao = inst(name=name, email=email, address=address, url=url, phone_number=phone_number)
            
            db.session.add(instituicao)
            db.session.commit()
            
            return "Registered!"

        except IntegrityError:
            return "Integrity Error",400

api.add_resource(Instituicao, '/api/instituicao')


class InstituicaoById(Resource):
    def get (self, id):
        instituicao = inst.query.filter_by(id=id).first()
        return instituicao 

    def post (self):
        try:
            name = request.json.get('name', None)
            email = request.json.get('email', None)
            address = request.json.get('address', None)
            url = request.json.get('url', None)
            phone_number = request.json.get('phone_number', None)


            instituicao = inst(name=name, email=email, address=address, url=url, phone_number=phone_number)
            
            db.session.add(instituicao)
            db.session.commit()
            
            return "Registered!"
        # melhor forma de fazer o except
        # ele da except tanto quando os mesmos dados são passados, tanto quando falta algum atributo.    
        except IntegrityError:
            return "Integrity Error",400

api.add_resource(InstituicaoById, '/api/instituicao/<string:id>')


class Register(Resource):
    def post (self):
        try:
            name = request.json.get('name', None)
            admin = request.json.get('admin', None)
            email = request.json.get('email', None)
            password = request.json.get('password', None)
            address = request.json.get('address', None)
            gender = request.json.get('gender', None)
            phone_number = request.json.get('phone_number', None)


            user = u(full_name=name, admin=admin, email=email, phone_number = phone_number, password_hash=password, address=address, gender=gender)
            
            db.session.add(user)
            db.session.commit()
            
            return "Registered!"
        # melhor forma de fazer o except
        # ele da except tanto quando os mesmos dados são passados, tanto quando falta algum atributo.    
        except IntegrityError:
            return "Integrity Error",400

api.add_resource(Register, '/api/register')


class Login(Resource):
        def post(self):
            try:
                email = request.json.get('email', None)
                password = request.json.get('password', None)

                if not email:
                    return 'Missing e-mail!', 400
                if not password:
                    return 'Missing Password!', 400
            
                user = u.query.filter_by(email=email).first()

                if not user:
                    return 'User Not Found!', 404
            
                if (password == user.password_hash):
                    return f'Welcome back {user.full_name}'
                return "Wrong Password!"
            except :
               return "Please provide an email and a password", 400

api.add_resource(Login, '/api/login')


@app.route('/api/logout')
def logout():
    return redirect(url_for('index'))