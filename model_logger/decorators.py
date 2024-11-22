from functools import wraps
import time
import inspect
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from .models import ModelLog

def log_action(name=None, description=None, action_type='OTHER'):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            start_time = time.time()
            
            previous_instance = None
            if action_type == 'UPDATE' and hasattr(self, 'pk') and self.pk:
                previous_instance = self.__class__.objects.filter(pk=self.pk).first()
            
            result = func(self, *args, **kwargs)
            
            execution_time = (time.time() - start_time) * 1000
            
            request = None
            for frame_record in inspect.stack():
                if frame_record[3] == 'get_response':
                    request = frame_record[0].f_locals.get('request')
                    break
            
            content_type = ContentType.objects.get_for_model(self.__class__)
            log_entry = ModelLog.objects.create(
                name=name or func.__name__,
                description=description or f"Action performed: {func.__name__}",
                content_type=content_type,
                object_id=self.id,
                action_type=action_type,
                execution_time=execution_time
            )
            
            if request:
                log_entry.user = getattr(request, 'user', None)
                log_entry.ip_address = get_client_ip(request)
                log_entry.user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            log_entry.save_changes(
                previous_instance=previous_instance,
                current_instance=self if hasattr(self, 'pk') and self.pk else None
            )
            
            return result
        return wrapper
    return decorator

def get_client_ip(request):
    """
    İstemci IP adresini al
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
