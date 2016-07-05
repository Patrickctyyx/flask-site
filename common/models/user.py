# -*- coding: utf-8 -*-

from flask import g, current_app

db = g.db

import uuid # UUID 的目的，是让分布式系统中的所有元素，都能有唯一的辨识资讯，而不需要透过中央控制端来做辨识资讯的指定。
import datetime

class Account(db.Model): # 用户账户,用户名密码之类的
    __tablename__ = current_app.config["TABLE_PREFIX"] + 'account'

    uid = db.Column(db.String(36), primary_key=True,
            default=lambda: str(uuid.uuid4())) # 用uuid应该是为了防止用户名冲突
    passwd = db.Column(db.String(32), default="")
    created_at = db.Column(db.DateTime, default=datetime.datetime.now) # 创建时间

    credentials = db.relationship("Credential", back_populates="account")
    user_info = db.relationship("UserInfo",
            back_populates="account", uselist=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.uid)

class Credential(db.Model): # 登录信息,邮箱电话之类的
    __tablename__ = current_app.config["TABLE_PREFIX"] + 'credential'
    __table_args__ = (
            db.PrimaryKeyConstraint('cred_type', 'cred_value'),
        )

    cred_type = db.Column(db.Enum("email", "phone", "name"))
    cred_value = db.Column(db.String(64))
    uid = db.Column(db.String(36), db.ForeignKey(Account.uid))

    account = db.relationship(Account,
            back_populates="credentials", uselist=False)

class UserInfo(db.Model): # 用户信息,学号部门之类的
    __tablename__ = current_app.config["TABLE_PREFIX"] + 'user_info'

    uid = db.Column(db.String(36), db.ForeignKey(Account.uid), primary_key=True)
    student_id = db.Column(db.Integer)
    department = db.Column(db.String(128))
    school = db.Column(db.String(128))
    introduction = db.Column(db.Text)

    account = db.relationship(Account,
            back_populates="user_info", uselist=False)



