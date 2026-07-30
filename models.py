"""
数据模型模块 - 定义应用数据模型
"""
import datetime


class User:
    """用户模型"""

    def __init__(self, user_id, username, email, role='user', created_at=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.role = role  # 'user', 'admin', 'moderator'
        self.created_at = created_at or datetime.datetime.utcnow()
        self.is_active = True

    def to_dict(self):
        """将用户对象转为字典"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active,
        }

    @staticmethod
    def from_dict(data):
        """从字典创建用户对象"""
        return User(
            user_id=data.get('user_id'),
            username=data.get('username'),
            email=data.get('email'),
            role=data.get('role', 'user'),
            created_at=datetime.datetime.fromisoformat(data['created_at'])
            if 'created_at' in data else None,
        )

    def __repr__(self):
        return f'<User {self.username!r}>'


class Article:
    """文章模型"""

    def __init__(self, article_id, title, content, author_id,
                 status='draft', created_at=None, updated_at=None):
        self.article_id = article_id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.status = status  # 'draft', 'published', 'archived'
        self.created_at = created_at or datetime.datetime.utcnow()
        self.updated_at = updated_at or self.created_at

    def to_dict(self):
        """将文章对象转为字典"""
        return {
            'article_id': self.article_id,
            'title': self.title,
            'content': self.content,
            'author_id': self.author_id,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    @staticmethod
    def from_dict(data):
        """从字典创建文章对象"""
        return Article(
            article_id=data.get('article_id'),
            title=data.get('title'),
            content=data.get('content'),
            author_id=data.get('author_id'),
            status=data.get('status', 'draft'),
            created_at=datetime.datetime.fromisoformat(data['created_at'])
            if 'created_at' in data else None,
            updated_at=datetime.datetime.fromisoformat(data['updated_at'])
            if 'updated_at' in data else None,
        )

    def publish(self):
        """发布文章"""
        self.status = 'published'
        self.updated_at = datetime.datetime.utcnow()

    def archive(self):
        """归档文章"""
        self.status = 'archived'
        self.updated_at = datetime.datetime.utcnow()

    def __repr__(self):
        return f'<Article {self.title!r}>'


class Comment:
    """评论模型"""

    def __init__(self, comment_id, article_id, author_id, body,
                 created_at=None):
        self.comment_id = comment_id
        self.article_id = article_id
        self.author_id = author_id
        self.body = body
        self.created_at = created_at or datetime.datetime.utcnow()

    def to_dict(self):
        """将评论对象转为字典"""
        return {
            'comment_id': self.comment_id,
            'article_id': self.article_id,
            'author_id': self.author_id,
            'body': self.body,
            'created_at': self.created_at.isoformat(),
        }

    @staticmethod
    def from_dict(data):
        """从字典创建评论对象"""
        return Comment(
            comment_id=data.get('comment_id'),
            article_id=data.get('article_id'),
            author_id=data.get('author_id'),
            body=data.get('body'),
            created_at=datetime.datetime.fromisoformat(data['created_at'])
            if 'created_at' in data else None,
        )

    def __repr__(self):
        return f'<Comment {self.comment_id} on Article {self.article_id}>'
