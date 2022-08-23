from flask_restful import Resource, reqparse
from model.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required
from blocklist import BLOCKLIST
from passlib.hash import bcrypt
import flask_jwt_extended


atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help='The field "login" cannot be left blank')
atributos.add_argument('senha', type=str, required=True, help='The field "senha" cannot be left blank')

class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return{'message': 'User not found.'}, 404

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An internal error ocurred trying to delete user.'},500 #Erro de servidor
            return {'message':' User deleted.'}
        return {'message': 'User not found.'}, 404

class UserRegister(Resource):

    def post(self):
        
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message':'The login \'{}\' already exists.'.format(dados['login'])}

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User created successfully.'}, 201 #Created


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        hasher = bcrypt.using(rounds=13)
        user = UserModel.find_by_login(dados['login'])
        hashed_password = hasher.hash(dados['senha'])

        if user and hasher.verify(dados['senha'], hashed_password):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_de_acesso}, 200
        return {'message': 'The username or password is incorrect.'}, 401 # Unauthorized


class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = flask_jwt_extended.get_jwt()['jti'] #jwt Token Identifier
        BLOCKLIST.add(jwt_id)
        return {'message' : 'Logged out successfully!'}, 200