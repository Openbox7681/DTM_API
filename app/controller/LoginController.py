from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required ,get_jwt_identity
from flask_jwt_extended import create_refresh_token
from app.model.User import User
from app.model.Role import Role
from app.model.RoleForm import RoleForm


from app import jwt


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'code': 201,
        'message': "token expired"
        # 'msg' : jwt_payload
    })


class Refresh(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def post(self):
        status = None
        message = None
        data = None
        userId = get_jwt_identity()


        # refresh_token = create_refresh_token(identity=userId)

        refresh_token = create_access_token(identity=userId)

        data = {
            "RefreshToken": refresh_token
        }


        return jsonify({
            "code": 200,
            "message": "success",
            "data": data
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
        flag_user_exist = False
        flag_password_correct = False
            
        try:
            flag_user_exist, flag_password_correct, user = User.authenticate(args['account'], args['password'])
        except Exception as e :
            print(str(e))
            status = 500
            message = "user not exist"
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
            account = user.account
            roleId =  user.id_role
            roleName = user.role.name

            roleFormList = user.role.db_role_roleForm


            roleFormJson = list()
            for roleForm in roleFormList:
                roleFormData = {
                    "FormId" : roleForm.formId,
                    "FormName" : roleForm.form.name,
                    "ActionRead" : roleForm.actionRead
                }

                roleFormJson.append(roleFormData)


            data = {
                "Token": token,
                "Account" : account,
                "Id": id,
                "RoleId" : roleId, 
                "RoleName" : roleName,
                "RoleFormList" : roleFormJson
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
