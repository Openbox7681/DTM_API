from app import db
from flask_bcrypt import Bcrypt

#角色資料管理
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)
    isEnable = db.Column(db.Boolean, nullable=False)
    sort = db.Column(db.Integer, default=True, nullable=False)
    createId = db.Column(db.Integer, nullable=False)
    createTime = db.Column(db.DateTime , nullable=False)
    modifyId = db.Column(db.Integer, nullable=False)
    modifyTime = db.Column(db.DateTime , nullable=False)

    #一對一
    #通過 relationship 與User 雙向綁定
    list_user = db.relationship("User" , backref= "role")

    #一對多 一
    #通過 relationship 與 role form 綁定資料
    # db_role_roleForm = db.relationship("RoleForm", backref="role")



    def __init__(self, name, isEnable, sort, createId , createTime , modifyId , modifyTime):
        self.name = name
        self.isEnable = isEnable
        self.sort = sort
        self.createId = createId
        self.createTime = createTime
        self.modifyId = modifyId
        self.modifyTime = modifyTime

    
    #利用id 取得角色資料
    def get_role(id):
        return Role.query.filter(Role.id == id).first()

    #取得角色
    @staticmethod
    def get_all_roles():
        return Role.query.filter(Role.isEnable == 1).all()

    #新增角色
    @staticmethod
    def insert_role(role):
        db.session.add(role)
        db.session.commit()

    #角色資料更新
    @staticmethod
    def update_role(role):
        db.session.merge(role)
        db.session.commit()
    
    #刪除角色
    @staticmethod
    def delete_role(role):
        db.session.delete(role)
        db.session.commit()

    #給定查詢條件查詢角色資料
    @staticmethod
    def get_list(start=0, maxRows=5, dir=False, sort='id', id=0, name=None, isEnable=None):

        role = Role.query
        if id != 0 :
            role = role.filter(Role.id == id)
        if name is not None :
            role = role.filter(Role.name.like( "%" + name + "%"))
        if isEnable is not None :
            role = role.filter(Role.isEnable == isEnable)

        return role.order_by(Role.id).limit(maxRows).offset(start)
    
    #利用ID 查詢角色資料
    @staticmethod
    def get_list_size(id=0, name=None, isEnable=None) :
        role = Role.query
        if id != 0 :
            role = role.filter(Role.id == id)
        if name is not None :
            role = role.filter(Role.name.like( "%" + name + "%"))
        if isEnable is not None :
            role = role.filter(Role.isEnable == isEnable)
        return len(role.all())


    #利用ID 查詢角色資料
    @staticmethod
    def is_name_exist(name):
        return Role.query.filter(Role.name == name).first() is not None







        



