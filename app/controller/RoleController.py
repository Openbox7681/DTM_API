from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required ,get_jwt_identity
from app.model.User import User
from app.model.Role import Role
from app.model.Form import Form
from app.model.RoleForm import RoleForm
from datetime import datetime

from app import jwt

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'status': 201,
        'message': "token expired"
        # 'msg' : jwt_payload
    })


class QueryRole(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def post(self):
        message = None
        total = 0
        status = None
        args = reqparse.RequestParser() \
            .add_argument("Id", type=str, location='json', required=False) \
            .add_argument("Name", type=str, location='json', required=False) \
            .add_argument("IsEnable", type=bool, location='json', required=False) \
            .add_argument("Start", type=str, location='json', required=False) \
            .add_argument("MaxRows", type=str, location='json', required=False) \
            .add_argument("Dir", type=bool, location='json', required=False) \
            .add_argument("Sort", type=bool, location='json', required=False) \
            .parse_args()
        id = 0 if args["Id"] is None else args["Id"]
        name = None if args["Name"] is None else args["Name"]
        isEnable = True if args["IsEnable"] is None else args["IsEnable"]  
        start = 1 if args["Start"] is None else args["Start"]
        maxRows = 1 if args["MaxRows"] is None else args["MaxRows"]
        dir = False if args["Dir"] is None else args["Dir"]
        sort = 'id'if args["Sort"] is None else args["Sort"]
        roles = Role.get_list(start, maxRows, dir, sort , id, name, isEnable)
        total = Role.get_list_size(id,name,isEnable)
        data = list()

        if roles is not None :
            status = 200
            message = "success"
            for role in roles :
                datatable = dict()

                datatable = {
                        "Id": role.id,
                        "Name": role.name,
                        "IsEnable" : role.isEnable , 
                        "Sort" : role.sort,
                        "CreateId" : role.createId,
                        "CreateTime" : role.createTime.strftime("%m-%d-%Y %H:%M:%S"),
                        "ModifyId" : role.modifyId,
                        "ModifyTime" : role.modifyTime.strftime("%m-%d-%Y %H:%M:%S")
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

class QueryRoleById(Resource):
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

        role = Role.get_role(id)
        if role is not None:
            status = 200
            message = "success"
            data = {
                        "Id": role.id,
                        "Name": role.name,
                        "IsEnable" : role.isEnable , 
                        "Sort" : role.sort,
                        "CreateId" : role.createId,
                        "CreateTime" : role.createTime.strftime("%m-%d-%Y %H:%M:%S"),
                        "ModifyId" : role.modifyId,
                        "ModifyTime" : role.modifyTime.strftime("%m-%d-%Y %H:%M:%S")
                    }
        else : 
            status = 201
            message = "查無此角色Id"

        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })
        

class CreateRole(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def post(self):
        message = None
        status = None
        data = None
        createId = get_jwt_identity()

        
        args = reqparse.RequestParser() \
            .add_argument("Name", type=str, location='json', required=False) \
            .add_argument("IsEnable", type=bool, location='json', required=False) \
            .add_argument("Sort", type=int, location='json', required=False) \
            .parse_args()
            
        name = None if args["Name"] is None else args["Name"]
        isEnable = True if args["IsEnable"] is None else args["IsEnable"]
        sort = 1 if args["Sort"] is None else args["Sort"] 


        if name is not None :
            if Role.is_name_exist(name):
                status = 202 
                message = "角色名稱已存在"
            else:
                role = Role(
                    name= name,
                    isEnable = isEnable, 
                    sort = sort, 
                    createId =  createId , 
                    createTime = datetime.now(),
                    modifyId = createId ,
                    modifyTime = datetime.now()  
                    )

                #寫入角色資料
                role = Role.insert_role(role)
                #寫入角色權限資料
                forms = Form.get_all_forms()
                for form in forms:
                    FormId = form.id
                    RoleId = role.id
                    roleForm = RoleForm(
                        roleId = RoleId,
                        formId = FormId,
                        actionRead = False,
                        createId = 1,
                        createTime = datetime.now(),
                        modifyId = 1,
                        modifyTime = datetime.now()
                        )
                    RoleForm.insert_roleForm(roleForm)

                if role is not None :
                    status = 200 
                    message = "新增資料成功"
                    data = {
                    "Id" : role.id
                }   
                else :
                    status = 200 
                    message = "新增資料失敗"  
                         
        else :
            status = 201
            message = "名字不能為空"      
        
        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })
    
    
class UpdateRole(Resource):
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
            .add_argument("Name", type=str, location='json', required=False) \
            .add_argument("IsEnable", type=bool, location='json', required=False) \
            .add_argument("Sort", type=int, location='json', required=False) \
            .parse_args()
            
        id = None if args["Id"] is None else args["Id"]
        name = None if args["Name"] is None else args["Name"]
        isEnable = True if args["IsEnable"] is None else args["IsEnable"]
        sort = 1 if args["Sort"] is None else args["Sort"]
        
        role = Role.get_role(id)
        
        
        if role is not None :
            if Role.is_name_exist(name):
                status = 202 
                message = "角色名稱已存在"
            else:
                role.isEnable = isEnable
                role.name = name
                role.sort = sort
                role.modifyTime = datetime.now() 
                role.modifyId = modifyId
                role = Role.update_role(role)
                if role is not None :
                    status = 200 
                    message = "更新資料成功"
                    data = {
                        "Id" : role.id
                    }   
                else :
                    status = 200 
                    message = "更新資料失敗"    
        else :
            status = 201
            message = "查無此角色ID"
            
        
        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })
        
        
class DeleteRole(Resource):
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


        if Role.is_id_exist(id):
            role = Role.get_role(id)
            try:
                Role.delete_role(role)
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
            message= '查無此角色Id'
            data = {
                    "Id" : id
                }  
        
        
        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })
            
        
    



    