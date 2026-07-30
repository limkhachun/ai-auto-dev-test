"""
主应用模块 - Flask 应用程序入口
"""
import os
import sys
from datetime import datetime

# 确保可以导入同级模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, request

from config import get_config
from models import User, Article, Comment
from decorators import require_auth, require_role, log_execution, validate_input
from utils import generate_id, validate_email, validate_username, sanitize_html
from admin import AdminService


def create_app(config_name=None):
    """应用工厂函数"""
    app = Flask(__name__)
    app_config = get_config(config_name)
    app.config.from_object(app_config)

    # 初始化管理服务（作为全局单例）
    admin_service = AdminService()

    # ── 错误处理器 ──────────────────────────────────

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request', 'message': str(error)}), 400

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Forbidden', 'message': str(error)}), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found', 'message': str(error)}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    # ── API 路由：健康检查 ──────────────────────────

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """健康检查端点"""
        return jsonify({
            'status': 'ok',
            'timestamp': datetime.utcnow().isoformat(),
        })

    # ── API 路由：认证 ──────────────────────────────

    @app.route('/api/auth/login', methods=['POST'])
    def login():
        """用户登录（模拟）"""
        data = request.get_json() or {}
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400

        # 模拟登录验证
        for user in admin_service.users.values():
            if user.username == username:
                return jsonify({
                    'message': 'Login successful',
                    'user': user.to_dict(),
                    'token': f'simulated-token-{user.user_id}',
                })

        return jsonify({'error': 'Invalid credentials'}), 401

    # ── API 路由：用户管理 ──────────────────────────

    @app.route('/api/users', methods=['GET'])
    @log_execution
    def list_users():
        """获取用户列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        try:
            items, pagination = admin_service.list_users(page, per_page)
            return jsonify({'data': items, 'pagination': pagination})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/api/users', methods=['POST'])
    @log_execution
    @validate_input('username', 'email')
    def create_user():
        """创建用户"""
        data = request.get_json() or {}
        try:
            user = admin_service.create_user(
                username=data['username'],
                email=data['email'],
                role=data.get('role', 'user'),
            )
            return jsonify({'data': user, 'message': 'User created'}), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/api/users/<user_id>', methods=['GET'])
    def get_user(user_id):
        """获取单个用户"""
        try:
            user = admin_service.get_user(user_id)
            return jsonify({'data': user})
        except ValueError as e:
            return jsonify({'error': str(e)}), 404

    @app.route('/api/users/<user_id>', methods=['PUT'])
    def update_user(user_id):
        """更新用户"""
        data = request.get_json() or {}
        try:
            user = admin_service.update_user(user_id, **data)
            return jsonify({'data': user, 'message': 'User updated'})
        except ValueError as e:
            return jsonify({'error': str(e)}), 404

    @app.route('/api/users/<user_id>', methods=['DELETE'])
    def delete_user(user_id):
        """删除用户"""
        try:
            admin_service.delete_user(user_id)
            return jsonify({'message': 'User deleted'})
        except ValueError as e:
            return jsonify({'error': str(e)}), 404

    # ── API 路由：文章管理 ──────────────────────────

    @app.route('/api/articles', methods=['GET'])
    def list_articles():
        """获取文章列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        try:
            items, pagination = admin_service.list_articles(status, page, per_page)
            return jsonify({'data': items, 'pagination': pagination})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/api/articles', methods=['POST'])
    @validate_input('title', 'content', 'author_id')
    def create_article():
        """创建文章"""
        data = request.get_json() or {}
        # 净化 HTML 内容
        data['content'] = sanitize_html(data.get('content', ''))
        try:
            article = admin_service.create_article(
                title=data['title'],
                content=data['content'],
                author_id=data['author_id'],
                status=data.get('status', 'draft'),
            )
            return jsonify({'data': article, 'message': 'Article created'}), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/api/articles/<article_id>', methods=['GET'])
    def get_article(article_id):
        """获取单篇文章"""
        try:
            article = admin_service.get_article(article_id)
            return jsonify({'data': article})
        except ValueError as e:
            return jsonify({'error': str(e)}), 404

    @app.route('/api/articles/<article_id>', methods=['PUT'])
    def update_article(article_id):
        """更新文章"""
        data = request.get_json() or {}
        if 'content' in data:
            data['content'] = sanitize_html(data['content'])
        try:
            article = admin_service.update_article(article_id, **data)
            return jsonify({'data': article, 'message': 'Article updated'})
        except ValueError as e:
            return jsonify({'error': str(e)}), 404

    @app.route('/api/articles/<article_id>', methods=['DELETE'])
    def delete_article(article_id):
        """删除文章"""
        try:
            admin_service.delete_article(article_id)
            return jsonify({'message': 'Article deleted'})
        except ValueError as e:
            return jsonify({'error': str(e)}), 404

    # ── API 路由：评论管理 ──────────────────────────

    @app.route('/api/comments', methods=['GET'])
    def list_comments():
        """获取评论列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        article_id = request.args.get('article_id')
        try:
            items, pagination = admin_service.list_comments(article_id, page, per_page)
            return jsonify({'data': items, 'pagination': pagination})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/api/comments', methods=['POST'])
    @validate_input('article_id', 'author_id', 'body')
    def create_comment():
        """创建评论"""
        data = request.get_json() or {}
        try:
            comment = admin_service.create_comment(
                article_id=data['article_id'],
                author_id=data['author_id'],
                body=data['body'],
            )
            return jsonify({'data': comment, 'message': 'Comment created'}), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/api/comments/<comment_id>', methods=['DELETE'])
    def delete_comment(comment_id):
        """删除评论"""
        try:
            admin_service.delete_comment(comment_id)
            return jsonify({'message': 'Comment deleted'})
        except ValueError as e:
            return jsonify({'error': str(e)}), 404

    # ── API 路由：仪表盘 ────────────────────────────

    @app.route('/api/admin/dashboard', methods=['GET'])
    def dashboard():
        """获取仪表盘统计"""
        stats = admin_service.get_dashboard_stats()
        return jsonify({'data': stats})

    # ── 主页 ──────────────────────────────────────

    @app.route('/')
    def index():
        """主页"""
        return jsonify({
            'app': 'Flask Admin API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'users': '/api/users',
                'articles': '/api/articles',
                'comments': '/api/comments',
                'dashboard': '/api/admin/dashboard',
            },
        })

    return app


# ── 启动入口 ──────────────────────────────────────

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
