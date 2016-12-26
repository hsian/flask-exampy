from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager



class Permission:
    #FOLLOW = 0x01
    COMMENT = 0x02
    #WRITE_ARTICLES = 0x04
    #MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.COMMENT, True),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    #posts = db.relationship('Post', backref='author', lazy='dynamic')
    inline = db.Column(db.Boolean, default=False)
    local_ip = db.Column(db.String(64), unique=True, index=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.username == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()        

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    @staticmethod
    def insert_users():

        users = ["chrome","firefox","IE","safari"]

        for u in users:
            user = User(username=u,
                        password= "12345")
            db.session.add(user)
            db.session.commit()
        print("sucessful insert users");

    @staticmethod
    def insert_admin():
        user = User(username="hsian",
                    password= current_app.config["FLASKY_ADMIN_PASSWORD"])
        db.session.add(user)
        db.session.commit()

    def set_local_ip(self,ip):
        self.local_ip = ip;
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username

# must add user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Select(db.Model):
    __tablename__ = 'selects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=True)
    option = db.Column(db.String(256), unique=True)
    answer = db.Column(db.String(64), unique=True)
    period = db.Column(db.Integer, default=255)
    edited_time = db.Column(db.DateTime(), default=datetime.utcnow)


    def __repr__(self):
        return '<Select %r>' % self.title






