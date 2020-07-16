# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2019/9/16 10:21'

Module usage:
参数说明:
-p：指定端口号
-h：指定主机ip
-t：开启的进程数量

Usage:
    >>> pip install -r requirements.txt
    >>> python manage.py start
    >>> python manage.py start -p 5000 -h 0.0.0.0 -t 3

Now, you can input "http://127.0.0.1:5000" in browser to get result
"""

from flask_script import Manager

from app import create_app

app = create_app()
manager = Manager(app)


# python manage.py start -h 127.0.0.1 -p 5000
@manager.option('-p', '--port', help='Server run port', default=5000)
@manager.option('-h', '--host', help='Server run host', default='0.0.0.0')
@manager.option('-t', '--thread', help='Thread count', default=1)
def start(host, port, thread):
    """
    启动服务
    :param host:
    :param port:
    :param thread:
    :return:
    """
    app.run(host=host, port=int(port), processes=int(thread))


if __name__ == '__main__':
    manager.run()
