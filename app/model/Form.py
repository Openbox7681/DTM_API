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
        
    #利用id 取得表單資料
    @staticmethod
    def get_form(id):
        return Form.query.filter(Form.id == id).first()
    
    
    #取得所有啟用表單資料
    @staticmethod
    def get_all_forms():
        return Form.query.filter(Form.isEnable == 1).all()
    
    #新增表單資料
    @staticmethod
    def insert_form(form):
        db.session.add(form)
        db.session.commit()
        return form 
    
     #表單資料更新
    @staticmethod
    def update_form(form):
        db.session.merge(form)
        db.session.commit()
        return form
    
    #刪除表單資料
    @staticmethod
    def delete_form(form):
        db.session.delete(form)
        db.session.commit()
        
        
    #給定查詢條件查詢表單資料
    #@param name 表單名稱
    #       isEnable 是否啟用
    #       id 表單id
    @staticmethod
    def get_list(start=0, maxRows=5, dir=False, sort='id', id=0, name=None, isEnable=None):

        form = Form.query
        if id != 0 :
            form = form.filter(Form.id == id)
        if name is not None :
            form = form.filter(Form.name.like( "%" + name + "%"))
        if isEnable is not None :
            form = form.filter(Form.isEnable == isEnable)

        return form.order_by(Form.id).limit(maxRows).offset(start)
    
    #利用ID 查詢角色資料
    @staticmethod
    def get_list_size(id=0, name=None, isEnable=None) :
        form = Form.query
        if id != 0 :
            form = form.filter(Form.id == id)
        if name is not None :
            form = form.filter(Form.name.like( "%" + name + "%"))
        if isEnable is not None :
            form = form.filter(Form.isEnable == isEnable)
        return len(form.all())
    
    
    #利用ID 查詢表單資料
    @staticmethod
    def is_id_exist(id):
        return Form.query.filter(Form.id == id).first() is not None


    #表單名稱是否存在
    @staticmethod
    def is_name_exist(name):
        return Form.query.filter(Form.name == name).first() is not None


