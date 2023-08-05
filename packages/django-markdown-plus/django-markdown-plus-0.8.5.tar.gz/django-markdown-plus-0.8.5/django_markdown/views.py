""" Supports preview. """
from django.core.files.storage import default_storage
from django.shortcuts import render
import django

from . import settings


def preview(request):
    """ Render preview page.

    :returns: A rendered preview

    """
    if settings.MARKDOWN_PROTECT_PREVIEW:
        user = getattr(request, 'user', None)
        if not user or not user.is_staff:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())

    if django.VERSION < (1, 7):
        content = request.REQUEST.get('data', 'No content posted')
    else:
        content = request.GET.get('data')
        if content is None:
            content = request.POST.get('data', 'No content posted')

    return render(
        request, settings.MARKDOWN_PREVIEW_TEMPLATE, dict(
            content=content,
            css=settings.MARKDOWN_STYLE
        ))
