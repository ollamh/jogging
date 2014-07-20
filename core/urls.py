from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from django.conf.urls import patterns, include, url
from .views import TemplateIndexView, JoggingEntryFormView, TemplateListView, register_user

urlpatterns = patterns('',
    url(r'^$', login_required(TemplateIndexView.as_view()), name='index'),
    url(r'^list', TemplateListView.as_view(), name="list"),
    url(r'^add_entry/$', JoggingEntryFormView.as_view(), name="add_entry"),
    url(r'^login/$', login, {'template_name':"core/login.html"}, name="login_user"),
    url(r'^logout/$', logout, {'next_page': '/'}, name="logout_user"),
    url(r'^register/$', register_user, name="register_user"),
)
