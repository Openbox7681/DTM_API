from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required ,get_jwt_identity
from app.model.User import User
from app.model.Role import Role
from datetime import datetime

from app import jwt
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'status': 201,
        'message': "token expired"
        # 'msg' : jwt_payload
    })


class QueryUser(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def post(self):
        message = None
        total = 0
        status = None
        args = reqparse.RequestParser() \
            .add_argument("Id", type=str, location='json', required=False) \
            .add_argument("Account", type=str, location='json', required=False) \
            .add_argument("IsEnable", type=bool, location='json', required=False) \
            .add_argument("RoleId", type=str, location='json', required=False) \
            .add_argument("Start", type=str, location='json', required=False) \
            .add_argument("MaxRows", type=str, location='json', required=False) \
            .add_argument("Dir", type=bool, location='json', required=False) \
            .add_argument("Sort", type=bool, location='json', required=False) \
            .parse_args()
        id = 0 if args["Id"] is None else args["Id"]
        account = None if args["Account"] is None else args["Account"]
        isEnable = None if args["IsEnable"] is None else args["IsEnable"] 
        roleId = None if args["RoleId"] is None else args["RoleId"] 
        start = 1 if args["Start"] is None else args["Start"]
        maxRows = 1 if args["MaxRows"] is None else args["MaxRows"]
        dir = False if args["Dir"] is None else args["Dir"]
        sort = 'id'if args["Sort"] is None else args["Sort"]
        
        users = User.get_list(start, maxRows, dir, sort , id, account, isEnable, roleId)
        
        total = User.get_list_size(id,account,isEnable,roleId)
        data = list()

        if users is not None :
            status = 200
            message = "success"
            for user in users :
                datatable = dict()

                datatable = {
                        "Id": user.id,
                        "Account": user.account,
                        "Email" : user.email,
                        "IsEnable" : user.isEnable , 
                        "RoleId" : user.id_role,
                        "RoleName" :  user.role.name,
                        "CreateId" : user.createId,
                        "CreateTime" : user.createTime.strftime("%m-%d-%Y %H:%M:%S"),
                        "ModifyId" : user.modifyId,
                        "ModifyTime" : user.modifyTime.strftime("%m-%d-%Y %H:%M:%S")
                    }
                data.append(datatable)
        else : 
            status = 201
            message = "QueryError"

        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data,
            "Total" : total
        })

class QueryUserById(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def post(self):
        status = None
        message = None
        data = dict()
        args = reqparse.RequestParser() \
            .add_argument("Id", type=str, location='json', required=False) \
            .parse_args()
        id = 0 if args["Id"] is None else args["Id"]

        user = User.get_users_by_id(id)
        if user is not None:
            status = 200
            message = "success"
            data = {
                        "Id": user.id,
                        "Account": user.account,
                        "Email" : user.email,
                        "RoleId" : user.id_role,
                        "RoleName" : user.role.name,
                        "IsEnable" : user.isEnable , 
                        "CreateId" : user.createId,
                        "CreateTime" : user.createTime.strftime("%m-%d-%Y %H:%M:%S"),
                        "ModifyId" : user.modifyId,
                        "ModifyTime" : user.modifyTime.strftime("%m-%d-%Y %H:%M:%S")
                    }
        else : 
            status = 201
            message = "查無此角色Id"

        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })
        

class CreateUser(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def post(self):
        message = None
        status = None
        data = None
        createId = get_jwt_identity()

        
        args = reqparse.RequestParser() \
            .add_argument("Account", type=str, location='json', required=False) \
            .add_argument("IsEnable", type=bool, location='json', required=False) \
            .add_argument("Email", type=str, location='json', required=False) \
            .add_argument("Password", type=str, location='json', required=False) \
            .add_argument("RoleId", type=str, location='json', required=False) \
            .parse_args()
            
        account = None if args["Account"] is None else args["Account"]
        isEnable = False if args["IsEnable"] is None else args["IsEnable"]
        email = None if args["Email"] is None else args["Email"]
        roleId = 1 if args["RoleId"] is None else args["RoleId"] 
        password = None if args["Password"] is None else args["Password"]
        


        if account is not None and password is not None:
            hashed_password = bcrypt.generate_password_hash(password=password)
            if User.is_user_exist_by_account(account):
                status = 202
                message = "帳戶名稱已存在"
            else:
                user = User(
                    account= account,
                    isEnable = isEnable, 
                    enableTime = datetime.now(),
                    password = hashed_password,
                    email = email,
                    id_role = roleId,
                    createId =  createId , 
                    createTime = datetime.now(),
                    modifyId = createId ,
                    modifyTime = datetime.now()  
                    )
                user = User.insert_user(user)
                
                if user is not None :
                    status = 200 
                    message = "新增資料成功"
                    data = {
                    "Id" : user.id
                }   
                else :
                    status = 200 
                    message = "新增資料失敗"  
                         
        else :
            status = 201
            message = "帳戶名字或密碼不能為空"      
        
        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })
    
    
class UpdateUser(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def post(self):
        message = None
        status = None
        data = None
        modifyId = get_jwt_identity()
        
        
        args = reqparse.RequestParser() \
            .add_argument("Id", type=int, location='json', required=False) \
            .add_argument("Account", type=str, location='json', required=False) \
            .add_argument("Email", type=str, location='json', required=False) \
            .add_argument("Password", type=str, location='json', required=False) \
            .add_argument("RoleId", type=str, location='json', required=False) \
            .add_argument("IsEnable", type=bool, location='json', required=False) \
            .parse_args()
            
        id = None if args["Id"] is None else args["Id"]
        account = None if args["Account"] is None else args["Account"]
        email = None if args["Email"] is None else args["Email"]
        roleId = 0 if args["RoleId"] is None else args["RoleId"] 
        isEnable = False if args["IsEnable"] is None else args["IsEnable"]
        password = None if args["Password"] is None else args["Password"]

        
        user = User.get_users_by_id(id)
        if account == None:
            account = user.account
        
        if account is not None:
            if user is not None :
                if account is not None :
                    user.account = account
                if email is not None :
                    user.email = email
                if roleId != 0:
                    user.id_role = roleId
                if password is not None:
                    hashed_password = bcrypt.generate_password_hash(password=password)
                    user.password = hashed_password
                user.modifyTime = datetime.now() 
                user.modifyId = modifyId
                user.isEnable = isEnable
                if isEnable :
                    user.enableTime = datetime.now() 
                user = User.update_user(user)
                if user is not None :
                    status = 200 
                    message = "更新資料成功"
                    data = {
                        "Id" : user.id
                    }   
                else :
                    status = 200 
                    message = "更新資料失敗"    
            else :
                status = 201
                message = "查無此帳號ID"
        else :
            status = 201
            message = "帳戶名字或密碼不能為空"      
        
        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })
        
        
class DeleteUser(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def post(self):
        message = None
        status = None
        data = None
        
        args = reqparse.RequestParser() \
            .add_argument("Id", type=str, location='json', required=False) \
            .parse_args()
        id = 0 if args["Id"] is None else args["Id"]


        if User.is_user_exist_by_id(id):
            user = User.get_users_by_id(id)
            try:
                User.delete_user(user)
                status = 200
                message= '刪除成功'
                
                data = {
                    "Id" : id
                }   
            except Exception as e :
                print(e)
                status = 202
                message= '刪除失敗'
                data = {
                    "Id" : id
                }  
        else:
            status = 201
            message= '查無此帳號Id'
            data = {
                    "Id" : id
                }  
        
        
        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })
            
        
    



    