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


class QueryRole(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
    @jwt_required()
    def post(self):
        code = None
        message = None
        total = 0
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
        code = None
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
            message = "QueryError"

        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })






