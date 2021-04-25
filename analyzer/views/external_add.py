from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.shortcuts import redirect, render

from analyzer.defaults import defaults
from analyzer.forms import AddExternalTaskForm
from analyzer.models import TaskList
from analyzer.utils import staff_check


@login_required
@user_passes_test(staff_check)
def external_add(request) -> HttpResponse:
    """Allow authenticated users who don't have access to the rest of the ticket system to file a ticket
    in the list specified in settings.

    Publicly filed tickets are unassigned unless settings.DEFAULT_ASSIGNEE exists.
    """

    if not settings.DEFAULT_LIST_SLUG:
        # We do NOT provide a default in defaults
        raise RuntimeError("This feature requires DEFAULT_LIST_SLUG: in settings. See documentation.")

    if not TaskList.objects.filter(slug=settings.DEFAULT_LIST_SLUG).exists():
        raise RuntimeError("There is no TaskList with slug specified for DEFAULT_LIST_SLUG in settings.")

    if request.POST:
        form = AddExternalTaskForm(request.POST)

        if form.is_valid():
            current_site = Site.objects.get_current()
            task = form.save(commit=False)
            task.task_list = TaskList.objects.get(slug=settings.DEFAULT_LIST_SLUG)
            task.created_by = request.user
            if defaults("DEFAULT_ASSIGNEE"):
                task.assigned_to = get_user_model().objects.get(username=settings.DEFAULT_ASSIGNEE)
            task.save()

            messages.success(request, "Your trouble ticket has been submitted. We'll get back to you soon.")
            return redirect(defaults("PUBLIC_SUBMIT_REDIRECT"))

    else:
        form = AddExternalTaskForm(initial={"priority": 999})

    context = {"form": form}

    return render(request, "analyzer/add_task_external.html", context)
