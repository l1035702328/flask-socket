# flask-socket
venv\Scripts\activate
# 创建迁移存储库
.\manage.py db init

# 生成迁移文件
.\manage.py db migrate -m "Initial migration."

# 更新
python manage.py db upgrade
