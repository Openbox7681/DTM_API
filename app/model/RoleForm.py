from app import db
from flask_bcrypt import Bcrypt


#全部表單名稱
class RoleForm(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    roleId = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    formId = db.Column(db.Integer, db.ForeignKey('form.id'), nullable=False)

    #記錄該角色是否對該表單有讀取權限
    actionRead = db.Column(db.Boolean, nullable=False)
    
    createId = db.Column(db.Integer, nullable=False)
    createTime = db.Column(db.DateTime , nullable=False)
    modifyId = db.Column(db.Integer, nullable=False)
    modifyTime = db.Column(db.DateTime , nullable=False)


    def __init__(self, roleId, formId, actionRead, createId , createTime , modifyId , modifyTime):
        self.roleId = roleId
        self.formId = formId
        self.actionRead = actionRead
        self.createId = createId
        self.createTime = createTime
        self.modifyId = modifyId
        self.modifyTime = modifyTime

    #利用id 取得角色權限資料
    @staticmethod
    def get_roleForm(id):
        return RoleForm.query.filter(RoleForm.id == id).first()

    #取得所有角色權限資料
    @staticmethod
    def get_all_roleForms():
        return RoleForm.query.filter(RoleForm.isEnable == 1).all()
    
    #新增角色權限
    @staticmethod
    def insert_roleForm(roleForm):
        db.session.add(roleForm)
        db.session.commit()
        return roleForm
    
    #角色權限資料更新
    @staticmethod
    def update_roleForm(roleForm):
        db.session.merge(roleForm)
        db.session.commit()
        return roleForm

    @staticmethod
    def get_roleForms_by_roleId(roleId):
        roleForm = RoleForm.query
        roleForm = roleForm.filter(RoleForm.roleId == roleId)
        return roleForm.all()

    @staticmethod
    def get_roleForms_by_roleId_and_formId(roleId,  formId):
        roleForm = RoleForm.query
        roleForm = roleForm.filter(RoleForm.roleId == roleId)
        roleForm = roleForm.filter(RoleForm.formId == formId)
        return roleForm.first()

