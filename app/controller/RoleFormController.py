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

class GetAllRoles(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def get(self):
        message = None
        total = 0
        status = None
        data = dict()
        dataList = list()

        userId = get_jwt_identity()
        
        roleList = Role.get_all_roles()

        for role in roleList:
            dataList.append({"roleId": role.id, "roleName" : role.name})
        data["RoleList"]= dataList

        return jsonify({
            "code": 200,
            "message": "success",
            "data": data
        })
class UpdateRoleForm(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def post(self):
        message = None
        total = 0
        status = None
        data = list()
        userId = get_jwt_identity()
        args = reqparse.RequestParser() \
            .add_argument('RoleFormList', type=list,location='json')\
            .parse_args()
        
        roleFormList = args.get('RoleFormList')


        for roleFormJson in roleFormList:
            roleId = roleFormJson["RoleId"]
            formId = roleFormJson["FormId"]
            actionRead = roleFormJson["ActionRead"]
            roleForm = RoleForm.get_roleForms_by_roleId_and_formId(roleId,formId)
            if roleForm is not None:
                roleForm.actionRead = actionRead
                roleForm.modifyId = userId
                roleForm.modifyTime = datetime.now()
                RoleForm.update_roleForm(roleForm)
        
        status = 200
        message = "更新成功"


        return jsonify({
            "Status": status,
            "Message": message,
        })

class QueryRoleFormByRoleId(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def post(self):
        message = None
        total = 0
        status = None
        data = list()
        args = reqparse.RequestParser() \
            .add_argument("RoleId", type=str, location='json', required=False) \
            .parse_args()
        roleId = 0 if args["RoleId"] is None else args["RoleId"]

        roleForms = RoleForm.get_roleForms_by_roleId(roleId)

        if roleForms is not None:
            for roleForm in roleForms:
                responseJson = dict()
                responseJson = {
                    "RoleId" : roleForm.roleId,
                    "FormId" : roleForm.formId,
                    "FormName" : roleForm.form.name,
                    "ActionRead" : roleForm.actionRead,
                    "CreateId" : roleForm.createId,
                    "CreateId" : roleForm.createId,
                    "CreateTime" : roleForm.createTime.strftime("%m-%d-%Y %H:%M:%S"),
                    "ModifyId" : roleForm.modifyId,
                    "ModifyTime" : roleForm.modifyTime.strftime("%m-%d-%Y %H:%M:%S")
                }
                data.append(responseJson)
            status = 200
            message = "success"
        else :
            status = 201
            message = "查無此角色Id"



        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })
