import hashlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root123@59.127.199.98:3306/DTM'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt()



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



#==================================#


##新增admin 角色資料與一般使用者


AdminRole = Role(
    name= "SuperAdmin",
    isEnable = True, 
    sort = 1, 
    createId = 1 , 
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now()
    )

UserRole = Role(
    name= "User",
    isEnable = True, 
    sort = 2, 
    createId = 1 , 
    createTime = datetime.now(),
    modifyId = 1,
    modifyTime = datetime.now()
    )


db.session.add(AdminRole)
db.session.add(UserRole)



#==================================#

##新增 user 帳號角色資料與一般使用者帳號


password='123'
hashed_password = bcrypt.generate_password_hash(password=password)


admin = User(account="SuperAdmin", 
            password=hashed_password, 
            email = "admin@gmail",
            isEnable = True, 
            enableTime = datetime.now(), 
            createId = 1 , 
            createTime = datetime.now(),
            modifyId = 1,
            modifyTime = datetime.now(),
            id_role=1
            )

db.session.add(admin)


#==================================#


db.session.commit()


db.session.close()