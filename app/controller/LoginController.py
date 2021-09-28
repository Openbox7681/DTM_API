from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required ,get_jwt_identity
from app.model.User import User
from app.model.Role import Role

from app import jwt


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'code': 201,
        'message': "token expired"
    })


class Login(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    def post(self):
        status = None
        message = None
        token = None
        userId = None
        roleId = None
        roleName = None
        data = None

        args = reqparse.RequestParser() \
            .add_argument('account', type=str, location='json', required=True, help="用戶名不能為空") \
            .add_argument("password", type=str, location='json', required=True, help="密碼不能為空") \
            .parse_args()

        flag_user_exist, flag_password_correct, user = User.authenticate(args['account'], args['password'])
        if not flag_user_exist:
            status = 201
            message = "user not exist"
        elif not flag_password_correct:
            status = 202
            message = "wrong password"
        else:
            status = 200
            message = "success"
            token = create_access_token(identity=user.id)
            id = user.id
            roleId =  user.id_role
            roleName = user.role.name

            data = {
                "Token": token,
                "Id": id,
                "RoleId" : roleId , 
                "RoleName" : roleName
            }

        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })


class Users(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def post(self):
        code = None
        message = None
        token = None
        userId = None
        roleId = None
        roleName = None
        status = None

        args = reqparse.RequestParser() \
            .add_argument("AccountId", type=str, location='json', required=True) \
            .parse_args()
        
        AccountId = args['AccountId']
        if User.is_user_exist_by_id(AccountId) :
            user = User.get_users_by_id(AccountId)
            message = "success"
            status = 200

            id = user.id
            account = user.account
            email = user.email
            isEnable = user.isEnable
            roleId =  user.id_role
            roleName = user.role.name
            createId = user.createId
            createTime = user.createTime.strftime("%m-%d-%Y %H:%M:%S")
            modifyId = user.modifyId
            modifyTime = user.modifyTime.strftime("%m-%d-%Y %H:%M:%S")

            data = {
                "Id": id,
                "Account" : account ,
                "Email" : email,
                "IsEnable" : isEnable,
                "RoleId" : roleId,
                "RoleName" : roleName, 
                "CreateId" : createId ,
                "CreateTime" : createTime,
                "ModifyId" : modifyId , 
                "ModifyTime" : modifyTime
                
            }


        else :
            status = 201
            message = "account not exist"

        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })








    @jwt_required()
    def get(self):
        users_list = []
        users = User.get_users()

        userId = get_jwt_identity()
        print(userId)


        for user in users:
            users_list.append({"userid": user.id, "account": user.account})

        return jsonify({
            "code": 200,
            "message": "success",
            "users": users_list
        })
