# DTM_API


## Database 資料庫設定方式
參考 /app/config.py檔案

```

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'mysql+pymysql://<account>:<password>@<ip>:<port>/<databasename>'


設定範例
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'mysql+pymysql://root:root123@192.168.0.226:3306/DTM'

```

### 初步資料庫建立方式

參考scripts 下 table 建立方式 執行以下程式

```

python3 dbInitialize.py
python3 RoleFOrmdbInitialize.py

```

### python 套件安裝方式
```

pip3 install -r requirements.txt

```

### api server 啟動方式
預設開在5000 port 欲修改port 可進入 manage.py 改寫
```
python3 manage.py
```


欲修改port 可進入 manage.py 改寫
```

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    #修改以上設定即可更換port
```