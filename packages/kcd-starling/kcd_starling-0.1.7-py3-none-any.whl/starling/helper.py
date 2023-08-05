import dataclasses
import json
from typing import Callable

from starling.config import CONFIG
from starling.exception import RetryTaskExitError, RetryTaskSkipAuthError, RetryTaskError


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


def retry_task() -> Callable:
    def decorator(fn: Callable) -> Callable:
        def fn_retry(*args, **kwargs):
            attempt = 0
            is_auth = True
            times = CONFIG.get('task_retry_times')
            while attempt < times - 1:
                try:
                    return fn(*args, **kwargs, is_auth=is_auth)
                except RetryTaskExitError as e:
                    raise e
                except RetryTaskSkipAuthError as e:
                    is_auth = False
                    attempt += 1
                except RetryTaskError as e:
                    attempt += 1
            return fn(*args, **kwargs, is_auth=is_auth)

        return fn_retry

    return decorator


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)
