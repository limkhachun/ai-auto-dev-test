"""
工具函数模块 - 提供通用工具函数
"""
import hashlib
import re
import uuid
from datetime import datetime, timedelta


def generate_id():
    """生成唯一标识符"""
    return str(uuid.uuid4())


def hash_password(password, salt=None):
    """
    对密码进行哈希处理
    返回格式: salt$hashed_password
    """
    if salt is None:
        salt = uuid.uuid4().hex[:16]
    hashed = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
    return f'{salt}${hashed}'


def verify_password(password, hashed_password):
    """
    验证密码是否与哈希匹配
    输入格式应为: salt$hashed_password
    """
    if '$' not in hashed_password:
        return False
    salt, stored_hash = hashed_password.split('$', 1)
    computed_hash = hashlib.sha256(
        (salt + password).encode('utf-8')
    ).hexdigest()
    return computed_hash == stored_hash


def validate_email(email):
    """验证电子邮件格式是否有效"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_username(username):
    """验证用户名是否有效（字母数字下划线，3-20个字符）"""
    if not username or len(username) < 3 or len(username) > 20:
        return False
    pattern = r'^[a-zA-Z0-9_]+$'
    return bool(re.match(pattern, username))


def sanitize_html(text):
    """简易的 HTML 净化，移除危险标签"""
    if not text:
        return ''
    # 移除 script 和 style 标签及其内容
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # 移除 on 开头的属性事件处理器
    text = re.sub(r'\son\w+\s*=\s*["\'][^"\']*["\']', '', text, flags=re.IGNORECASE)
    return text.strip()


def truncate_text(text, max_length=100, suffix='...'):
    """截断文本到指定长度"""
    if not text:
        return ''
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + suffix


def format_datetime(dt, fmt='%Y-%m-%d %H:%M:%S'):
    """格式化日期时间对象"""
    if dt is None:
        return ''
    return dt.strftime(fmt)


def parse_datetime(date_str, fmt='%Y-%m-%d %H:%M:%S'):
    """解析日期时间字符串"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, fmt)
    except (ValueError, TypeError):
        return None


def time_ago(dt):
    """返回人类可读的相对时间描述"""
    if dt is None:
        return '未知'

    now = datetime.utcnow()
    diff = now - dt

    if diff < timedelta(seconds=60):
        return '刚刚'
    elif diff < timedelta(minutes=60):
        minutes = diff.seconds // 60
        return f'{minutes}分钟前'
    elif diff < timedelta(hours=24):
        hours = diff.seconds // 3600
        return f'{hours}小时前'
    elif diff < timedelta(days=30):
        days = diff.days
        return f'{days}天前'
    elif diff < timedelta(days=365):
        months = diff.days // 30
        return f'{months}个月前'
    else:
        years = diff.days // 365
        return f'{years}年前'


def paginate(items, page=1, per_page=20):
    """
    对列表进行分页
    返回: (当前页数据, 分页信息字典)
    """
    total = len(items)
    total_pages = max(1, (total + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))

    start = (page - 1) * per_page
    end = start + per_page
    page_items = items[start:end]

    pagination = {
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': total_pages,
        'has_prev': page > 1,
        'has_next': page < total_pages,
    }
    return page_items, pagination
