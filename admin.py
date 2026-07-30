"""
管理后台模块 - 提供管理员操作接口
"""
from functools import wraps

from models import User, Article, Comment
from decorators import require_auth, require_role, log_execution
from utils import generate_id


class AdminService:
    """管理后台服务"""

    def __init__(self):
        # 模拟数据库存储
        self.users = {}
        self.articles = {}
        self.comments = {}
        self._init_sample_data()

    def _init_sample_data(self):
        """初始化示例数据"""
        admin_user = User(
            user_id=generate_id(),
            username='admin',
            email='admin@example.com',
            role='admin',
        )
        self.users[admin_user.user_id] = admin_user

        moderator_user = User(
            user_id=generate_id(),
            username='moderator',
            email='moderator@example.com',
            role='moderator',
        )
        self.users[moderator_user.user_id] = moderator_user

        regular_user = User(
            user_id=generate_id(),
            username='user1',
            email='user1@example.com',
            role='user',
        )
        self.users[regular_user.user_id] = regular_user

    # ── 用户管理 ──────────────────────────────────

    @log_execution
    def list_users(self, page=1, per_page=20):
        """获取用户列表"""
        from utils import paginate
        user_list = list(self.users.values())
        user_dicts = [u.to_dict() for u in user_list]
        items, pagination = paginate(user_dicts, page, per_page)
        return items, pagination

    @log_execution
    def get_user(self, user_id):
        """获取单个用户"""
        user = self.users.get(user_id)
        if user is None:
            raise ValueError(f'User {user_id} not found')
        return user.to_dict()

    @log_execution
    def create_user(self, username, email, role='user'):
        """创建新用户"""
        from utils import validate_email, validate_username

        if not validate_username(username):
            raise ValueError('Invalid username format')
        if not validate_email(email):
            raise ValueError('Invalid email format')

        # 检查用户名和邮箱唯一性
        for existing_user in self.users.values():
            if existing_user.username == username:
                raise ValueError(f'Username {username!r} already exists')
            if existing_user.email == email:
                raise ValueError(f'Email {email!r} already exists')

        user = User(
            user_id=generate_id(),
            username=username,
            email=email,
            role=role,
        )
        self.users[user.user_id] = user
        return user.to_dict()

    @log_execution
    def update_user(self, user_id, **kwargs):
        """更新用户信息"""
        user = self.users.get(user_id)
        if user is None:
            raise ValueError(f'User {user_id} not found')

        allowed_fields = {'username', 'email', 'role'}
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(user, key, value)

        return user.to_dict()

    @log_execution
    def delete_user(self, user_id):
        """删除用户"""
        if user_id not in self.users:
            raise ValueError(f'User {user_id} not found')
        del self.users[user_id]
        # 同时删除该用户的文章和评论
        self.articles = {
            aid: a for aid, a in self.articles.items()
            if a.author_id != user_id
        }
        self.comments = {
            cid: c for cid, c in self.comments.items()
            if c.author_id != user_id
        }
        return True

    # ── 文章管理 ──────────────────────────────────

    @log_execution
    def list_articles(self, status=None, page=1, per_page=20):
        """获取文章列表，可按状态筛选"""
        from utils import paginate
        article_list = list(self.articles.values())
        if status:
            article_list = [a for a in article_list if a.status == status]

        article_list.sort(key=lambda a: a.created_at, reverse=True)
        article_dicts = [a.to_dict() for a in article_list]
        items, pagination = paginate(article_dicts, page, per_page)
        return items, pagination

    @log_execution
    def get_article(self, article_id):
        """获取单篇文章"""
        article = self.articles.get(article_id)
        if article is None:
            raise ValueError(f'Article {article_id} not found')
        return article.to_dict()

    @log_execution
    def create_article(self, title, content, author_id, status='draft'):
        """创建新文章"""
        if author_id not in self.users:
            raise ValueError(f'Author {author_id} not found')
        article = Article(
            article_id=generate_id(),
            title=title,
            content=content,
            author_id=author_id,
            status=status,
        )
        self.articles[article.article_id] = article
        return article.to_dict()

    @log_execution
    def update_article(self, article_id, **kwargs):
        """更新文章"""
        article = self.articles.get(article_id)
        if article is None:
            raise ValueError(f'Article {article_id} not found')

        allowed_fields = {'title', 'content', 'status'}
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(article, key, value)
        article.updated_at = __import__('datetime').datetime.utcnow()
        return article.to_dict()

    @log_execution
    def delete_article(self, article_id):
        """删除文章"""
        if article_id not in self.articles:
            raise ValueError(f'Article {article_id} not found')
        del self.articles[article_id]
        # 同时删除关联评论
        self.comments = {
            cid: c for cid, c in self.comments.items()
            if c.article_id != article_id
        }
        return True

    # ── 评论管理 ──────────────────────────────────

    @log_execution
    def list_comments(self, article_id=None, page=1, per_page=20):
        """获取评论列表，可按文章筛选"""
        from utils import paginate
        comment_list = list(self.comments.values())
        if article_id:
            comment_list = [c for c in comment_list if c.article_id == article_id]

        comment_list.sort(key=lambda c: c.created_at, reverse=True)
        comment_dicts = [c.to_dict() for c in comment_list]
        items, pagination = paginate(comment_dicts, page, per_page)
        return items, pagination

    @log_execution
    def create_comment(self, article_id, author_id, body):
        """创建评论"""
        if article_id not in self.articles:
            raise ValueError(f'Article {article_id} not found')
        if author_id not in self.users:
            raise ValueError(f'Author {author_id} not found')

        comment = Comment(
            comment_id=generate_id(),
            article_id=article_id,
            author_id=author_id,
            body=body,
        )
        self.comments[comment.comment_id] = comment
        return comment.to_dict()

    @log_execution
    def delete_comment(self, comment_id):
        """删除评论"""
        if comment_id not in self.comments:
            raise ValueError(f'Comment {comment_id} not found')
        del self.comments[comment_id]
        return True

    # ── 仪表盘统计 ──────────────────────────────────

    @log_execution
    def get_dashboard_stats(self):
        """获取仪表盘统计信息"""
        total_users = len(self.users)
        total_articles = len(self.articles)
        total_comments = len(self.comments)
        published_articles = sum(
            1 for a in self.articles.values() if a.status == 'published'
        )
        draft_articles = sum(
            1 for a in self.articles.values() if a.status == 'draft'
        )

        return {
            'total_users': total_users,
            'total_articles': total_articles,
            'total_comments': total_comments,
            'published_articles': published_articles,
            'draft_articles': draft_articles,
            'moderators': sum(
                1 for u in self.users.values() if u.role == 'moderator'
            ),
            'admins': sum(
                1 for u in self.users.values() if u.role == 'admin'
            ),
        }
