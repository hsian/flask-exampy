# exampy 考试系统 

  python-flask + sqlite 考试系统,可以创建多期题目,题目分为选择题和问答题,
  
  选择题提交答案后可直接匹配答案,问答题在后台预览每道题每个人的回答,
  
  每个人的登录名和当前ip绑定,禁止多次登录;
  
## 开发环境和依赖
 
 本项目开发环境是win7 其他环境自行查找相关安装方法 区别都不大,因为win下是最难的T^T;
 
  
## step

  1. install python3.x <a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a>
  
  2. `pip install virtualenv`
  
  3. create new folder `exam`

  4. `cd exam` and `git clone https://github.com/hsian/exampy.git`
  
  5. `cd exampy` create virtualenv `virtualenv venv` and switch to `venv\scripts\activate`
  
  6. installation dependency `pip install -r requirements.txt`
  
## deploy

  1. initialization db `python manage.py db init` `python manage.py db migrate` `python manage.py db upgrade`
  
  2. insert data `python manage.py deploy`
  
  3. run server `python manage.py runserver` or 'python tornado_server.py`
  
开发使用 python manage.py runserver ,管理员用户名:admin, 密码:123456; <详见配置文件 config.py>
  
  
  
  
  
  
