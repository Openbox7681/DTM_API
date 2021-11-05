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


class QueryForm(Resource):
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
        
        forms = Form.get_list(start, maxRows, dir, sort , id, name, isEnable)
        total = Form.get_list_size(id,name,isEnable)
        
        
        data = list()

        if forms is not None :
            status = 200
            message = "success"
            for form in forms :
                datatable = dict()

                # roleFormTable = form.db_form_roleForm
                # for roleForm in roleFormTable:
                #     print(roleForm.id)
                #     print(roleForm.role.name)


                datatable = {
                        "Id": form.id,
                        "Name": form.name,
                        "Code" : form.code,
                        "IsEnable" : form.isEnable , 
                        "CreateId" : form.createId,
                        "CreateTime" : form.createTime.strftime("%m-%d-%Y %H:%M:%S"),
                        "ModifyId" : form.modifyId,
                        "ModifyTime" : form.modifyTime.strftime("%m-%d-%Y %H:%M:%S")
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

class QueryFormById(Resource):
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

        form = Form.get_form(id)
        if form is not None:
            status = 200
            message = "success"
            data = {
                        "Id": form.id,
                        "Name": form.name,
                        "Code" : form.code,
                        "IsEnable" : form.isEnable, 
                        "CreateId" : form.createId,
                        "CreateTime" : form.createTime.strftime("%m-%d-%Y %H:%M:%S"),
                        "ModifyId" : form.modifyId,
                        "ModifyTime" : form.modifyTime.strftime("%m-%d-%Y %H:%M:%S")
                    }
        else : 
            status = 201
            message = "查無此表單Id"

        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })
        

class CreateForm(Resource):
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
            .add_argument("Code", type=str, location='json', required=False) \
            .parse_args()
            
        name = None if args["Name"] is None else args["Name"]
        isEnable = True if args["IsEnable"] is None else args["IsEnable"]
        code = None if args["Code"] is None else args["Code"]


        if name is not None and code is not None :
            if Form.is_name_exist(name):
                status = 202 
                message = "角色名稱已存在"
            else:
                form = Form(
                    name= name,
                    code = code ,
                    isEnable = isEnable, 
                    createId =  createId , 
                    createTime = datetime.now(),
                    modifyId = createId ,
                    modifyTime = datetime.now()  
                    )
                form = Form.insert_form(form)
                
                if form is not None :
                    status = 200 
                    message = "新增資料成功"
                    data = {
                    "Id" : form.id
                }   
                else :
                    status = 200 
                    message = "新增資料失敗"  
                         
        else :
            status = 201
            message = "名字或編碼不能為空"      
        
        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })
    
    
class UpdateForm(Resource):
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
            .add_argument("CodeName", type=str, location='json', required=False) \
            .parse_args()
            
        id = None if args["Id"] is None else args["Id"]
        name = None if args["Name"] is None else args["Name"]
        isEnable = True if args["IsEnable"] is None else args["IsEnable"]
        codeName = None if args["CodeName"] is None else args["CodeName"]
        
        form = Form.get_form(id)
        
        
        if form is not None :
            if Form.is_name_exist(name) and name != form.name:
                status = 202 
                message = "表單名稱已存在"
            else:
                form.isEnable = isEnable
                form.name = name
                form.modifyTime = datetime.now() 
                form.modifyId = modifyId
                form = Form.update_form(form)
                if form is not None :
                    status = 200 
                    message = "更新資料成功"
                    data = {
                        "Id" : form.id
                    }   
                else :
                    status = 200 
                    message = "更新資料失敗"    
        else :
            status = 201
            message = "查無此表單ID"
            
        
        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })
        
        
class DeleteForm(Resource):
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


        if Form.is_id_exist(id):
            form = Form.get_form(id)
            try:
                Form.delete_form(form)
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
            
        
    



    