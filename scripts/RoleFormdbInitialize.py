import hashlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime



app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root123@59.127.199.98:3306/DTM'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt()






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

#     #一對一
#     #通過 relationship 與 role form 綁定資料
#     db_form_role = db.relationship("RoleForm", backref="product")




    def __init__(self, roleId, formId, actionRead, createId , createTime , modifyId , modifyTime):
        self.roleId = roleId
        self.formId = formId
        self.actionRead = actionRead
        self.createId = createId
        self.createTime = createTime
        self.modifyId = modifyId
        self.modifyTime = modifyTime


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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    isEnable = db.Column(db.Boolean, default=True, nullable=False)
    enableTime = db.Column(db.DateTime , nullable=False)
    createId = db.Column(db.Integer, nullable=False)
    createTime = db.Column(db.DateTime , nullable=False)
    modifyId = db.Column(db.Integer, nullable=False)
    modifyTime = db.Column(db.DateTime , nullable=False)
    #角色資料ID關聯
    id_role = db.Column(db.Integer, db.ForeignKey("role.id"), default=1) #角色id
    

    def __init__(self, account, password, email, isEnable, enableTime, createId, createTime, modifyId, modifyTime, id_role):
        self.account = account
        self.password = password
        self.email = email
        self.isEnable = isEnable
        self.enableTime = enableTime
        self.createId = createId
        self.createTime = createTime
        self.modifyId = modifyId
        self.modifyTime = modifyTime
        self.id_role = id_role


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
    db_role_roleForm = db.relationship("RoleForm", backref="role")




    def __init__(self, name, isEnable, sort, createId , createTime , modifyId , modifyTime):
        self.name = name
        self.isEnable = isEnable
        self.sort = sort
        self.createId = createId
        self.createTime = createTime
        self.modifyId = modifyId
        self.modifyTime = modifyTime

#建立初始schema
db.create_all()


##新增表單資料
#==================================#
#首頁表單
DashboardForm = Form(
    name= "Dashboard",
    code= "Dashboard",
    isEnable = True,  
    createId = 1 , 
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now()
    )
#監控表單
MonitoringScreenForm = Form(
    name= "MonitoringScreen",
    code= "MonitoringScreen",
    isEnable = True,  
    createId = 1 , 
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now()
    )

MonitoringInterFaceForm = Form(
    name= "MonitoringInterFace",
    code= "MonitoringInterFace",
    isEnable = True,  
    createId = 1 , 
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now()
    )

#系統資訊
SystemForm = Form(
    name= "System",
    code= "System",
    isEnable = True,  
    createId = 1 , 
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now()
)
#服務啟用查看表單
ServiceForm = Form(
    name = "Service",
    code = "Service",
    isEnable = True,
    createId = 1 , 
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now() 
)
#使用者表單
UserForm = Form(
    name = "User",
    code = "User",
    isEnable = True,
    createId = 1 , 
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now() 
)

#角色設定表單
RoleFormt = Form(
    name = "Role",
    code = "Role",
    isEnable = True,
    createId = 1 , 
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now() 
)

#角色權限設定表單
RoleFormForm = Form(
    name = "RoleForm",
    code = "RoleForm",
    isEnable = True,
    createId = 1 , 
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now() 
)

#報表設定表單
ReportForm = Form(
    name = "Report",
    code = "Report",
    isEnable = True,
    createId = 1 , 
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now() 
)


db.session.add(DashboardForm)
db.session.add(MonitoringScreenForm)
db.session.add(MonitoringInterFaceForm)
db.session.add(SystemForm)
db.session.add(ServiceForm)
db.session.add(UserForm)
db.session.add(RoleFormt)
db.session.add(RoleFormForm)
db.session.add(ReportForm)
#==================================#

##新增表單資料權限給SuperAdmin
AdminDashboardRoleForm = RoleForm(
    roleId = 1,
    formId = 1,
    actionRead = True,
    createId = 1,
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now()
)

AdminMonitoringScreenRoleForm = RoleForm(
    roleId = 1,
    formId = 2,
    actionRead = True,
    createId = 1,
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now()
)


AdminMonitoringInterFaceRoleForm = RoleForm(
    roleId = 1,
    formId = 3,
    actionRead = True,
    createId = 1,
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now()
)


AdminSystemRoleForm = RoleForm(
    roleId = 1,
    formId = 4,
    actionRead = True,
    createId = 1,
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now()
)

AdminServiceRoleForm = RoleForm(
    roleId = 1,
    formId = 5,
    actionRead = True,
    createId = 1,
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now()
)

AdminUserRoleForm = RoleForm(
    roleId = 1,
    formId = 6,
    actionRead = True,
    createId = 1,
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now()
)

AdminRoleRoleForm = RoleForm(
    roleId = 1,
    formId = 7,
    actionRead = True,
    createId = 1,
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now()
)

AdminRoleFormRoleForm = RoleForm(
    roleId = 1,
    formId = 8,
    actionRead = True,
    createId = 1,
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now()
)


AdminReportRoleForm = RoleForm(
    roleId = 1,
    formId = 9,
    actionRead = True,
    createId = 1,
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now()
)



db.session.add(AdminDashboardRoleForm)
db.session.add(AdminMonitoringScreenRoleForm)
db.session.add(AdminMonitoringInterFaceRoleForm)
db.session.add(AdminSystemRoleForm)
db.session.add(AdminServiceRoleForm)
db.session.add(AdminUserRoleForm)
db.session.add(AdminRoleRoleForm)
db.session.add(AdminRoleFormRoleForm)
db.session.add(AdminReportRoleForm)



#==================================#








db.session.commit()


db.session.close()