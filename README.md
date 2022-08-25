# flask-socket
venv\Scripts\activate
# 创建迁移存储库 只执行一次
.\manage.py db init

# 生成迁移文件  只要模型更改了就执行
.\manage.py db migrate -m "Initial migration."

# 更新 同上
python manage.py db upgrade

每次我们部署后，我们重启服务后，原来的定时任务都需要重启，这样对我们经常迭代的项目肯定是不行的
