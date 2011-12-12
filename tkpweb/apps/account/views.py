from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Use this for class-based views instead of @login_required
# Alternatively, we could do
# login_required(TemplateView.as_view())
# in urls.py, but then we can't sublass Templateview
# See http://groups.google.com/group/django-users/browse_thread/thread/5239e284b5c285d5,
# http://stackoverflow.com/questions/6069070/how-to-use-permission-required-decorators-on-django-class-based-views
# and https://docs.djangoproject.com/en/dev/topics/class-based-views/#decorating-the-class
class AccountView(TemplateView):
    template_name = 'account/index.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AccountView, self).dispatch(*args, **kwargs)
