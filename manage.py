# Flask-SocketIO 不是 WebSocket 服务器。它是一个 Socket.IO 服务器。
# Socket.IO 是建立在 WebSocket 之上的协议，要连接到它，您需要一个 Socket.IO 客户端。
# 有一个可能适用于 Arduino 的 C++：https ://github.com/socketio/socket.io-client-cpp 。

import os



from myflask import create_app, db
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
manager.add_command("runserver", Server(host='0.0.0.0', use_debugger=True))

migrate = Migrate(app, db)
# def make_shell_context():
#     return dict(app=app, db=db, User=User, Role=Role)
#
# manager.add_command("shell", Shell(make_context=make_shell_context))
# 添加迁移命令集 到脚本命令
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
