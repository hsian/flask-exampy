# exampy 考试系统  
  
## step

- install python3.x <a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a>
  
- `pip install virtualenv`
  
- create new folder `exam`

- `cd exam` and `git clone https://github.com/hsian/exampy.git`
  
- `cd exampy` create virtualenv `virtualenv venv` and switch to `venv\scripts\activate`
  
- installation dependency `pip install -r requirements.txt`
  
## deploy

- initialization db `python manage.py db init` `python manage.py db migrate` `python manage.py db upgrade`
  
- insert data `python manage.py deploy`
  
- run server `python manage.py runserver` or 'python tornado_server.py`
  
开发使用 python manage.py runserver ,管理员用户名:admin, 密码:123456; <详见配置文件 config.py>
  
  
  
  
  
  
