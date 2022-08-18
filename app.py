from flask import Flask
from flask_socketio import SocketIO

from index.view import index

# Flask-SocketIO 不是 WebSocket 服务器。它是一个 Socket.IO 服务器。
# Socket.IO 是建立在 WebSocket 之上的协议，要连接到它，您需要一个 Socket.IO 客户端。
# 有一个可能适用于 Arduino 的 C++：https ://github.com/socketio/socket.io-client-cpp 。


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


# 注册路由
app.register_blueprint(index, url_prefix='/')


if __name__ == '__main__':
    app.run()
