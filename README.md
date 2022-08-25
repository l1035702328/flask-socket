# flask-socket
venv\Scripts\activate
# 创建迁移存储库 只执行一次
.\manage.py db init

# 生成迁移文件  只要模型更改了就执行
.\manage.py db migrate -m "Initial migration."

# 更新 同上
python manage.py db upgrade
