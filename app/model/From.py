from app import db
from flask_bcrypt import Bcrypt


#全部表單名稱
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(45), nullable=False)
    name = db.Column(db.String(45), nullable=False)
    isEnable = db.Column(db.Boolean, nullable=False)
    createId = db.Column(db.Integer, nullable=False)
    createTime = db.Column(db.DateTime , nullable=False)
    modifyId = db.Column(db.Integer, nullable=False)
    modifyTime = db.Column(db.DateTime , nullable=False)

    #一對多 一
    #通過 relationship 與 role form 綁定資料
    db_form_roleForm = db.relationship("RoleForm", backref="form")




    def __init__(self, code, name, isEnable, createId , createTime , modifyId , modifyTime):
        self.code = code
        self.name = name
        self.isEnable = isEnable
        self.createId = createId
        self.createTime = createTime
        self.modifyId = modifyId
        self.modifyTime = modifyTime
