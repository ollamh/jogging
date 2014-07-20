# encoding: utf-8
import datetime

from tastypie.resources import ModelResource
from tastypie.models import ApiKey
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import SessionAuthentication, ApiKeyAuthentication, MultiAuthentication

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from .models import JoggingEntry


class TemplateIndexView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateIndexView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class TemplateListView(TemplateView):
    template_name = 'core/list.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateListView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class JoggingEntryFormView(TemplateView):
    template_name = 'core/add.html'


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        authentication = MultiAuthentication(
            SessionAuthentication(),
            ApiKeyAuthentication()
        )
        authorization = Authorization()



class EntryResource(ModelResource):

    user = fields.ToOneField(UserResource, 'user')

    class Meta:
        queryset = JoggingEntry.objects.all().order_by('-date')
        resource_name = 'entries'
        authentication = MultiAuthentication(
            SessionAuthentication(),
            ApiKeyAuthentication()
        )
        authorization = Authorization()

    def hydrate_duration(self, bundle):
        """
        Need convert data from raw minutes to timedelta
        """
        bundle.data['duration'] = datetime.timedelta(minutes=bundle.data['duration_minutes'])
        return bundle

    def dehydrate(self, bundle):
        """
        Need additional data due to slider
        """
        bundle.data['duration_minutes'] = int(bundle.obj.duration.total_seconds()/60)
        bundle.data['average_speed'] = bundle.obj.average_speed
        return bundle

    def obj_create(self, bundle, **kwargs):
        return super(EntryResource, self).obj_create(bundle, user=bundle.request.user)

    def get_object_list(self, request):
        return super(EntryResource, self).get_object_list(request).filter(user=request.user)



def register_user(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        username = form.clean_username()
        password = form.clean_password2()
        form.save()
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect(reverse('core:index'))
    return render(request, 'core/register.html', {'form': form})
