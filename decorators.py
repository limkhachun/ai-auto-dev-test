"""
装饰器模块 - 提供通用装饰器
"""
import functools
import logging
import time

logger = logging.getLogger(__name__)


def require_auth(f):
    """
    认证装饰器：检查请求是否携带有效的认证信息
    使用示例: @require_auth
    """

    @functools.wraps(f)
    def decorated(*args, **kwargs):
        # 在实际应用中，这里会从 request 中提取 token/session
        # 这里简化为从 kwargs 中检查 user 参数
        user = kwargs.get('user')
        if user is None:
            raise PermissionError('Authentication required')
        return f(*args, **kwargs)

    return decorated


def require_role(required_role):
    """
    角色权限装饰器：限制只有特定角色可以访问
    使用示例: @require_role('admin')
    """

    def decorator(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            user = kwargs.get('user')
            if user is None:
                raise PermissionError('Authentication required')

            # 角色层级: admin > moderator > user
            role_hierarchy = {'admin': 3, 'moderator': 2, 'user': 1}
            user_level = role_hierarchy.get(user.role, 0)
            required_level = role_hierarchy.get(required_role, 0)

            if user_level < required_level:
                raise PermissionError(
                    f'Insufficient role. Required: {required_role}, '
                    f'got: {user.role}'
                )
            return f(*args, **kwargs)

        return decorated

    return decorator


def log_execution(f):
    """
    日志装饰器：记录函数执行时间和参数
    使用示例: @log_execution
    """

    @functools.wraps(f)
    def decorated(*args, **kwargs):
        func_name = f.__name__
        logger.debug('Starting %s with args=%s kwargs=%s',
                     func_name, args, kwargs)
        start_time = time.time()
        try:
            result = f(*args, **kwargs)
            elapsed = time.time() - start_time
            logger.debug('%s completed in %.3f seconds', func_name, elapsed)
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error('%s failed after %.3f seconds: %s',
                         func_name, elapsed, str(e))
            raise

    return decorated


def validate_input(*required_fields):
    """
    输入验证装饰器：确保必需的参数不为空
    使用示例: @validate_input('title', 'content')
    """

    def decorator(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            missing = []
            for field in required_fields:
                value = kwargs.get(field)
                if value is None or (isinstance(value, str) and not value.strip()):
                    missing.append(field)
            if missing:
                raise ValueError(
                    f'Missing required fields: {", ".join(missing)}'
                )
            return f(*args, **kwargs)

        return decorated

    return decorator


def retry_on_failure(max_retries=3, delay=1.0, exceptions=(Exception,)):
    """
    重试装饰器：在函数抛出指定异常时自动重试
    使用示例: @retry_on_failure(max_retries=3, delay=1.0)
    """

    def decorator(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_retries + 1):
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    logger.warning(
                        'Attempt %d/%d failed for %s: %s',
                        attempt, max_retries, f.__name__, str(e)
                    )
                    if attempt < max_retries:
                        time.sleep(delay)
            raise last_exception

        return decorated

    return decorator
