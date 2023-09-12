#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username'],
            _password_hash=json['password']
        )
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):
    def get(self):
        if not session['user_id']:
            return {},204
        user = User.query.filter(User.id == session['user_id']).first().to_dict()
        return user,200

class Login(Resource):
    def post(self):
        username = request.get_json()
        user_name = username['username']
        
        user = User.query.filter(User.username == user_name).first()
        print(user.id)
        if user:
            session['user_id'] = user.id
            return user.to_dict(), 200
        else:
            return {}, 401

class Logout(Resource):
    def delete(post):
        session['user_id'] = None

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint = 'check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
