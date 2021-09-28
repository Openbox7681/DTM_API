# from app import db
# from flask_bcrypt import Bcrypt


# #全部表單名稱
# class RoleForm(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)

#     roleId = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
#     formId = db.Column(db.Integer, db.ForeignKey('form.id'), nullable=False)

#     actionCreate = db.Column(db.Boolean, nullable=False)
    
    


    
    
#     createId = db.Column(db.Integer, nullable=False)
#     createTime = db.Column(db.DateTime , nullable=False)
#     modifyId = db.Column(db.Integer, nullable=False)
#     modifyTime = db.Column(db.DateTime , nullable=False)

#     #一對一
#     #通過 relationship 與 role form 綁定資料
#     db_form_role = db.relationship("RoleForm", backref="product")




#     def __init__(self, code, name, isEnable, createId , createTime , modifyId , modifyTime):
#         self.code = code
#         self.name = name
#         self.isEnable = isEnable
#         self.createId = createId
#         self.createTime = createTime
#         self.modifyId = modifyId
#         self.modifyTime = modifyTime
