#### REF
https://hub.docker.com/_/rabbitmq/
https://www.rabbitmq.com/tutorials/tutorial-one-python.html

docker run -d --hostname localhost --name myrabbit -p 15672:15672 -p 5672:5672 rabbitmq
-d 后台进程运行
hostname RabbitMQ主机名称
name 容器名称
-p port:port 本地端口:容器端口
-p 15672:15672 http访问端口
-p 5672:5672 amqp访问端口

--python3
pip install pika
