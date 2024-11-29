from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class ModelLog(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='model_logs'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=512, null=True, blank=True)
    
    action_type = models.CharField(
        max_length=20,
        choices=[
            ('CREATE', 'Create'),
            ('UPDATE', 'Update'),
            ('DELETE', 'Delete'),
            ('OTHER', 'Other')
        ],
        default='OTHER'
    )
    previous_state = models.JSONField(null=True, blank=True)
    current_state = models.JSONField(null=True, blank=True)
    execution_time = models.FloatField(null=True, blank=True, help_text='Execution time in milliseconds')
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['action_type']),
            models.Index(fields=['user']),
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        user_info = f" by {self.user.username}" if self.user else ""
        return f"{self.action_type} - {self.name}{user_info} at {self.timestamp}"
    
    def save_changes(self, previous_instance=None, current_instance=None):
        """
        Save changes to the model log
        """
        if previous_instance:
            self.previous_state = self._get_instance_data(previous_instance)
        if current_instance:
            self.current_state = self._get_instance_data(current_instance)
        self.save()
    
    def _get_instance_data(self, instance):
        """
        Get data from an instance
        """
        data = {}
        for field in instance._meta.fields:
            if not field.is_relation:
                data[field.name] = str(getattr(instance, field.name))
        return data
