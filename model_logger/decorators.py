from functools import wraps
from django.contrib.contenttypes.models import ContentType
from .models import ModelLog

def log_action(name=None, description=None):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Execute the original function/method
            result = func(self, *args, **kwargs)
            
            # Create the log entry
            content_type = ContentType.objects.get_for_model(self.__class__)
            ModelLog.objects.create(
                name=name or func.__name__,
                description=description or f"Action performed: {func.__name__}",
                content_type=content_type,
                object_id=self.id
            )
            
            return result
        return wrapper
    return decorator
