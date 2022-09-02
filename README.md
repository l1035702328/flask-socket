# flask-socket
venv\Scripts\activate
# 创建迁移存储库 只执行一次
.\manage.py db init

# 生成迁移文件  只要模型更改了就执行
.\manage.py db migrate -m "Initial migration."

# 更新 同上
python manage.py db upgrade

每次我们部署后，我们重启服务后，原来的定时任务都需要重启，这样对我们经常迭代的项目肯定是不行的

# redis 命令
info clients 查看当前最大连接数


四、连接池的实现细节
要实现一个连接池，首先需要梳理清楚连接池的工作内容以及连接池会遇到的问题。实现连接池大致需要实现的功能大致如下:

4.1、连接容器的实现?
既然是连接池,所以就需要有池子的概念,创建了连接之后需要有一个容器用于存放连接,一般可采用的方式是数组或者是链表这两种数据结构.但是由于连接池的特性是增删连接较少,而查询获取连接的场景较多,所以采用数组的方式是最适合的。

4.2、连接池的连接初始化?
对于连接池而言，初始化的时候通常会初始化指定数量的连接，这样在连接池初始化之后就能立即可以提供连接给客户端使用，否则在初始化启动之后客户端访问的时候还是需要走创建连接的流程

4.3、连接池连接数的动态变化？
对于客户端访问资源的频率通常不是一成不变的。比如淘宝网站，用户访问的频率通常是周末访问频率比工作日访问频率要高，工作日中上班期间访问频率较低而下班期间访问较高。
所以客户端对于连接的需求也会随着用户使用习惯的规律而动态变化。如果连接池的连接数量一成不变就会导致高峰期间连接不够用，低峰期间连接长时间空闲。
所以连接池需要随着需求量的增长而动态增加连接，随着需求量的下降而动态删除连接

4.4、连接空闲检测机制？
当连接池中的连接长时间空闲，就应该将空闲的连接进行关闭，避免造成不必要的资源浪费，所以连接池需要有一个定时任务定期对所有连接进行是否为空闲的检测，并且需要检测空闲的时长，
因为如果仅判断空闲不判断空闲时长的话，很容易将刚刚被释放的连接当作是空闲的连接给关闭。所以需要对于空闲的连接要判断下当前连接空闲了多长时间，只有空闲了较长时间的连接才应该被关闭

4.5、强制回收机制？
当客户端获取连接之后，如果占用时间较长或者忘记关闭连接，就会导致连接一直被占用的，这样就会导致连接池中的连接很快被消耗完。所以需要有一种强制回收连接的机制，当连接被客户端占用的时间较长
时强制回收该连接。被回收连接的客户端如果需要连接的话就需要重新申请连接。

4.6、多线程下的并发问题？
连接池的维护需要考虑到诸多的并发问题，比如：
1.初始化连接池的并发问题,初始化连接池需要保证只能由一个线程来初始化,避免多个线程同时初始化连接池
2.创建连接的并发问题,动态创建连接时,需要并发控制,避免同时创建过多连接且超过了连接池上限,比如连接池上限为100个连接,当前共有99个连接正在被使用,此时又两个客户端来创建连接,如果不做并发控制就会导致两个客户端都创建连接成功导致连接数超过来了上限
3.销毁连接的并发问题,和创建连接问题类似,销毁连接如果不做并发控制容易导致连接数被销毁的少于连接池的最小连接数
4.获取连接的并发问题,获取连接的并发是连接池最重要的并发控制,因为需要避免两个客户端同时获取到了同一个连接的问题

五、总结