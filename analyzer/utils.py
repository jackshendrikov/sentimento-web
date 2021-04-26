import logging
import os

from analyzer.defaults import defaults
from analyzer.models import Attachment, Task

log = logging.getLogger(__name__)


def staff_check(user):
    """If STAFF_ONLY is set to True, limit view access to staff users only."""

    if defaults("STAFF_ONLY"):
        return user.is_staff
    else:
        # If unset or False, allow all logged in users
        return True


def user_can_read_task(task, user):
    return task.task_list.group in user.groups.all() or user.is_superuser


def toggle_task_analyzed(task_id: str) -> bool:
    """Toggle the `analyzed` bool on Task from True to False or vice versa."""
    try:
        task = Task.objects.get(id=task_id)
        task.analyzed = not task.analyzed
        task.save()
        return True

    except Task.DoesNotExist:
        log.info(f"Task {task_id} not found.")
        return False


def remove_attachment_file(attachment_id: int) -> bool:
    """Delete an Attachment object and its corresponding file from the filesystem."""
    try:
        attachment = Attachment.objects.get(id=attachment_id)
        if attachment.file:
            if os.path.isfile(attachment.file.path):
                os.remove(attachment.file.path)

        attachment.delete()
        return True

    except Attachment.DoesNotExist:
        log.info(f"Attachment {attachment_id} not found.")
        return False
