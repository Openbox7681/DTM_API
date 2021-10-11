from app import db
from flask_bcrypt import Bcrypt
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






    @staticmethod
    def is_user_exist_by_account(account):
        return User.query.filter(User.account == account).first()

    @staticmethod
    def is_user_exist_by_id(id):
        return User.query.filter(User.id == id).first() is not None

    @staticmethod
    def authenticate(account, password):
        flag_user_exist = True
        flag_password_correct = True


        user = User.query.filter(User.account == account).first()

        check_password = bcrypt.check_password_hash(user.password, password)

        if user and user.isEnable == 1 :
            if not check_password:
                flag_password_correct = False
        else:
            flag_user_exist = False

        return flag_user_exist, flag_password_correct, user

    #取得全部啟用之使用者資料
    @staticmethod
    def get_users():
        return User.query.filter(User.isEnable == 1).all()
    #利用id 取得帳號資料
    @staticmethod
    def get_users_by_id(id):
        return User.query.filter(User.id == id).first()
    
    #新增帳號資料
    @staticmethod
    def insert_user(user):
        db.session.add(user)
        db.session.commit()
        return user

    #更新帳號資料
    @staticmethod
    def update_user(user):
        db.session.merge(user)
        db.session.commit()
        return user
    
    #刪除帳號資料
    @staticmethod
    def delete_user(user):
        db.session.delete(user)
        db.session.commit()

    
    #設定帳號啟用狀態
    @staticmethod
    def set_user_isEnable(isEnable, id):
        user = get_users_by_id(id)
        user.isEnable = isEnable
        db.session.commit()
        
        
    #給定查詢條件查詢帳號資料
    # @param 
    #    id : 帳號id
    #    account : 帳號名稱
    #    isEnable : 是否啟用
    #    id_role : 角色id 關聯
    # @return 
    #    User
    # 
    @staticmethod
    def get_list(start=0, maxRows=5, dir=False, sort='id', id=0, account=None, isEnable=None, id_role = None):

        user = User.query
        if id != 0 :
            user = user.filter(User.id == id)
        if account is not None :
            user = user.filter(User.account.like( "%" + account + "%"))
        if isEnable is not None :
            user = user.filter(User.isEnable == isEnable)
        if id_role is not None :
            user = user.filter(User.id_role == id_role)

        return user.order_by(User.id).limit(maxRows).offset(start)
    
    
    #利用ID 查詢角色資料
    # @param 
    #    id : 帳號id
    #    account : 帳號名稱
    #    isEnable : 是否啟用
    #    id_role : 角色id 關聯
    # @return 
    #    User
    # 
    @staticmethod
    def get_list_size(id=0, account=None, isEnable=None, id_role = None) :
        user = User.query
        if id != 0 :
            user = user.filter(User.id == id)
        if account is not None :
            user = user.filter(User.account.like( "%" + account + "%"))
        if isEnable is not None :
            user = user.filter(User.isEnable == isEnable)
        if id_role is not None :
            user = user.filter(User.id_role == id_role)
        return len(user.all())


