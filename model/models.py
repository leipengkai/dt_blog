# coding: utf-8
import logging
from datetime import datetime
from model.constants import Constants
from sqlalchemy.orm import contains_eager, deferred
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, Boolean, Text, ForeignKey, BigInteger, DATE
from sqlalchemy.orm import relationship, backref
# 创建对象的基类:
DbBase = declarative_base()
# 一对多的关系映射

# sqlalchemy使用ForeignKey来指明一对多的关系，比如一个用户可有多个邮件地址，而一个邮件地址只属于一个用户。那么就是典型的一对多或多对一关系。

# 多方(子类)：在Address类中，我们定义外键，还有对应所属的user对象
    # 在设置外键 使用的是表名和表列
    # user_id = Column(Integer, ForeignKey('users.id'))
    # 在子表类中通过 foreign key (外键)引用父表的参考字段

    # 在设置关联属性的时候 使用的是类名和属性名 和父类中的backref="user"一样的意思
    # user = relationship("User", backref="addresses")
    # 子表将会在多对一的关系中获得父表的属性

# 一方(父类)：User类中，我们定义addresses属性 OTM
    # addresses = relationship("Address", order_by=Address.id, backref="user")
    # 在父表类中通过 relationship() 方法来引用子表的类集合

    # 只需要在一对多关系基础上的父表中使用 uselist 参数来表示 OTO
    # addresses = relationship("Address", uselist=False, order_by=Address.id, backref="user")


class DbInit(object):
    created_at = Column(DateTime, default=datetime.now)


class User(DbBase,DbInit):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True) # 增加字段
    # 以修改novel表格的update_at为ArrowType类型为例
    # op.alter_column('novel', 'update_at', type=sa_utils.ArrowType, existing_type=sa.String(120))
    email = Column(String(64), unique=True, index=True)
    username = Column(String(64), unique=True, index=True)
    password = Column(String(128))

    def verify_password(self, password):
        return self.password == password


class Menu(DbBase):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    types = relationship('ArticleType', backref='menu', lazy='dynamic')
    order = Column(Integer, default=0, nullable=False)

    def fetch_all_types(self, only_show_not_hide=False):
        query = self.types
        if only_show_not_hide:
            query = query.join(ArticleType.setting). \
                filter(ArticleTypeSetting.hide.isnot(True))
            # \
            #     options(contains_eager(ArticleType.setting))
        self.all_types = query.all()

    def __repr__(self):
        return '<Menu %r>' % self.name


class ArticleTypeSetting(DbBase):
    __tablename__ = 'articleTypeSettings'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    protected = Column(Boolean, default=False)
    hide = Column(Boolean, default=False)
    types = relationship('ArticleType', backref='setting', lazy='dynamic')

    @staticmethod
    def return_setting_hide():
        return [(2, u'公开'), (1, u'隐藏')]

    def __repr__(self):
        return '<ArticleTypeSetting %r>' % self.name


class ArticleType(DbBase):
    __tablename__ = 'articleTypes'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    introduction = Column(Text, default=None)
    articles = relationship('Article', backref='articleType', lazy='dynamic')
    menu_id = Column(Integer, ForeignKey('menus.id'), default=None)
    setting_id = Column(Integer, ForeignKey('articleTypeSettings.id'))


    @property
    def is_protected(self):
        if self.setting:
            return self.setting.protected
        else:
            return False

    @property
    def is_hide(self):
        if self.setting:
            return self.setting.hide
        else:
            return False

    def fetch_articles_count(self):
        self.articles_count = self.articles.count()
    # if the articleType does not have setting,
    # its is_hie and is_protected property will be False.

    def __repr__(self):
        return '<Type %r>' % self.name


class Source(DbBase):
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    articles = relationship('Article', backref='source', lazy='dynamic')

    def fetch_articles_count(self):
        self.articles_count = self.articles.count()

    def __repr__(self):
        return '<Source %r>' % self.name


class Comment(DbBase):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    create_time = Column(DateTime, default=datetime.now)
    author_name = Column(String(64))
    author_email = Column(String(64))
    article_id = Column(Integer, ForeignKey('articles.id'))
    disabled = Column(Boolean, default=False)
    comment_type = Column(String(64), default=Constants.COMMENT_TYPE_COMMENT)
    rank = Column(String(64), default=Constants.COMMENT_RANK_NORMAL)
    floor = Column(Integer, nullable=False)
    reply_to_id = Column(Integer)
    reply_to_floor = Column(String(64))


class Article(DbBase):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(64))
    content = deferred(Column(Text))  # 延迟加载,避免在列表查询时查询该字段
    summary = deferred(Column(Text))  # 延迟加载,避免在列表查询时查询该字段
    create_time = Column(DateTime, index=True, default=datetime.now)
    update_time = deferred(Column(DateTime, index=True, default=datetime.now, onupdate=datetime.now))
    num_of_view = Column(Integer, default=0)
    articleType_id = Column(Integer, ForeignKey('articleTypes.id'))
    source_id = Column(Integer, ForeignKey('sources.id'))
    comments = relationship('Comment', backref='article', lazy='dynamic') # foreign_keys='Comment.id'

    def fetch_comments_count(self, count=None):
        self.comments_count = count if count is not None else self.comments.count()

    def __repr__(self):
        return '<Article %r>' % self.title


class BlogInfo(DbBase):
    __tablename__ = 'blog_info'
    id = Column(Integer, primary_key=True)
    title = Column(String(64))
    signature = Column(Text)
    navbar = Column(String(64))


class Plugin(DbBase):
    __tablename__ = 'plugins'
    id = Column(Integer, primary_key=True)
    title = Column(String(64), unique=True)
    note = Column(Text, default='')
    content = Column(Text, default='')
    order = Column(Integer, index=True, default=0)
    disabled = Column(Boolean, default=False)

    def __repr__(self):
        return '<Plugin %r>' % self.title


class BlogView(DbBase):
    __tablename__ = 'blog_view'
    date = Column(DATE, primary_key=True)
    pv = Column(BigInteger, default=0)
    uv = Column(BigInteger, default=0)
