from django.db import models
from django.conf import settings


class UserRoleChange(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='role_changes_affected'
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='role_changes_made'
    )
    changed_at = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20, choices=[
        ('added', 'Added'),
        ('removed', 'Removed'),
    ])
    role = models.ForeignKey('user.Role', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-changed_at']
