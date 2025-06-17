from django.db import models
from django.conf import settings


class UserRoleChange(models.Model):
    """
    Tracks changes in user role assignments and removals.

    This model records when roles are added to or removed from users,
    storing who made the change and when it occurred.

    Attributes:
        user (User): The user whose roles were changed
        changed_by (User): The administrator who made the change
        changed_at (DateTime): When the change was made
        action (str): The type of change - either 'added' or 'removed'
        role (Role): The role that was added or removed
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='role_changes_affected',
        help_text="User whose roles were modified"
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='role_changes_made',
        help_text="Administrator who made the change"
    )
    changed_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the change was made"
    )
    action = models.CharField(
        max_length=20,
        choices=[('added', 'Added'), ('removed', 'Removed')],
        help_text="Whether the role was added or removed"
    )
    role = models.ForeignKey(
        'user.Role',
        on_delete=models.CASCADE,
        help_text="The role that was added or removed"
    )

    class Meta:
        app_label = 'history'
        verbose_name = "User Role Change"
        verbose_name_plural = "User Role Changes"
        db_table = 'history_user_role_changes'
        ordering = ['-changed_at']
        indexes = [
            models.Index(fields=['user', '-changed_at']),
            models.Index(fields=['role', '-changed_at'])
        ]


class UserChangeHistory(models.Model):
    """
    Tracks changes to user profile information.

    Records modifications to core user data like username, email, and institution,
    storing both the old and new values for audit purposes.

    Attributes:
        user (User): The user whose data was changed
        changed_by (User): The administrator who made the change
        changed_at (DateTime): When the change occurred
        old_username (str): Previous username before change
        new_username (str): New username after change
        old_email (str): Previous email before change
        new_email (str): New email after change
        old_institution (str): Previous institution before change
        new_institution (str): New institution after change
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='changes_affected',
        help_text="User whose data was modified"
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='changes_made',
        help_text="Administrator who made the change"
    )
    changed_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the change occurred"
    )
    old_username = models.CharField(
        max_length=255,
        null=True,
        help_text="Previous username"
    )
    new_username = models.CharField(
        max_length=255,
        null=True,
        help_text="New username"
    )
    old_email = models.EmailField(
        null=True,
        help_text="Previous email address"
    )
    new_email = models.EmailField(
        null=True,
        help_text="New email address"
    )
    old_institution = models.CharField(
        max_length=255,
        null=True,
        help_text="Previous institution name"
    )
    new_institution = models.CharField(
        max_length=255,
        null=True,
        help_text="New institution name"
    )
    old_is_active = models.BooleanField(
        null=True,
        help_text="Previous active status"
    )
    new_is_active = models.BooleanField(
        null=True,
        help_text="New active status"
    )

    class Meta:
        app_label = 'history'
        verbose_name = "User Change History"
        verbose_name_plural = "User Change Histories"
        db_table = 'history_user_changes'
        ordering = ['-changed_at']
        indexes = [
            models.Index(fields=['user', '-changed_at']),
            models.Index(fields=['changed_by', '-changed_at'])
        ]

    def __str__(self):
        """Returns a string representation of the change record."""
        return f"Change to {self.user.username} by {self.changed_by.username} on {self.changed_at}"
