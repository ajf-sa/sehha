from django.shortcuts import (render, HttpResponse, Http404, get_object_or_404,
                              redirect, reverse)
from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views import View, generic
from django.views.generic.edit import ModelFormMixin
from django.contrib import messages
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from alfuhigi.distance import Address
from apps.images.models import Image
from .models import Organization, Unit, Page
from .forms import OrgModelForm, NewsModelForm, ImageModelForm
from .choices import KIND_CHOICES
# from wadibyte.wadicore.models import Menu
# Create your views here.


class OrgCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                    generic.CreateView):

    model = Organization
    permission_required = 'sehha.add_organization'
    form_class = OrgModelForm
    # def handle_no_permission(self):
    #     return HttpResponse('no pperm')

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.is_authenticated():
        #     return redirect(reverse('org-list'))
            # raise PermissionDenied(self.get_permission_denied_message())
        if not self.has_permission():
            raise PermissionDenied(self.get_permission_denied_message())
        return super(OrgCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
            # save cleaned post data
            clean = form.cleaned_data
            context = {}
            # if self.object is None:
            # return
            # TODO add create_by method
            self.object = form.save(clean)
            self.object.is_active = True
            try:
                add = Address(self.object.lat, self.object.lng)
                self.object.address = add.get_address()
            except Exception:
                self.object.address = ''
            return super(OrgCreateView, self).form_valid(form)


class OrgListView(generic.ListView):
    model = Organization
    paginate_by = 6

    def get_queryset(self):
        qs = self.model.objects.filter(is_active=True).order_by('id')
        return qs

    def get_context_data(self, **kwargs):
        context = super(OrgListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class OrgDetailView(generic.TemplateView):
    model = Organization
    template_name = 'sehha/organization_detail.html'
    # pk_url_kwarg ='pk'

    def get_context_data(self, **kwargs):
        context = super(OrgDetailView, self).get_context_data(**kwargs)
        context['object'] = self.model.objects.filter(
                            uuid=self.kwargs.get('uuid')).first()
        context['now'] = timezone.now()
        return context


class OrgUpdateView(PermissionRequiredMixin, LoginRequiredMixin,
                    generic.UpdateView):
    model = Organization
    permission_required = 'sehha.change_organization'
    form_class = OrgModelForm
    # fields = ['name']
    # template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        context = super(OrgUpdateView, self).get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        obj = self.model.objects.get(uuid=self.kwargs['uuid'])
        return obj

    def form_valid(self, form):
            # save cleaned post data
            clean = form.cleaned_data
            context = {}
            self.object = form.save(clean)
            try:
                add = Address(self.object.lat, self.object.lng)
                self.object.address = add.get_address()
            except Exception:
                self.object.address = ''
            return super(OrgUpdateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.is_authenticated():
        #     return redirect(reverse('org-list'))
            # raise PermissionDenied(self.get_permission_denied_message())
        if not self.has_permission():
            raise PermissionDenied(self.get_permission_denied_message())
        return super(OrgUpdateView, self).dispatch(request, *args, **kwargs)


class OrgDeleteView(PermissionRequiredMixin, LoginRequiredMixin,
                    generic.DeleteView):
    login_required = True
    model = Organization
    permission_required = 'sehha.delete_organization'
    success_message = "Deleted Successfully"
    success_url = reverse_lazy('org-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(OrgDeleteView, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = self.model.objects.get(uuid=self.kwargs['uuid'])
        return obj

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(OrgDeleteView, self).form_valid(form)

    def get_queryset(self):
        qs = super(OrgDeleteView, self).get_queryset()
        return qs.filter(uuid=self.kwargs['uuid'])

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.is_authenticated():
        #     return redirect(reverse('org-list'))
            # raise PermissionDenied(self.get_permission_denied_message())
        if not self.has_permission():
            raise PermissionDenied(self.get_permission_denied_message())
        return super(OrgDeleteView, self).dispatch(request, *args, **kwargs)


class NewsCreateView(PermissionRequiredMixin,
                     LoginRequiredMixin, generic.CreateView):
    model = Page
    # login_url ='/lgin'
    permission_required = 'sehha.add_page'
    form_class = NewsModelForm
    init_tags = None

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            raise PermissionDenied(self.get_permission_denied_message())
        return super(NewsCreateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(NewsCreateView, self).get_initial()
        initial = initial.copy()
        initial['create_by'] = self.request.user
        initial['tags'] = self.init_tags
        return initial

    def form_valid(self, form):
        # form.cleaned_data['create_by'] =self.request.user
        self.object = form.save(commit=False)
        self.object.is_active = True
        # self.object.tags.add(*list(self.init_tags))
        self.object.save()

        return super(NewsCreateView, self).form_valid(form)


class NewsListView(generic.ListView):
    model = Page
    tag_name = 'news'

    def get_queryset(self):
        qs = self.model.objects.filter(tags__name=self.tag_name,
                                       is_active=True).order_by('-create_at')
        return qs

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class NewsDetailView(generic.TemplateView):
    model = Page
    template_name = 'sehha/page_detail.html'

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['object'] = Page.objects.get(
                pk=self.kwargs.get('pk'),
                )
        context['now'] = timezone.now()
        return context


class NewsRedirectView(generic.RedirectView):
    def get(self, request, *args, **kwargs):
        uuid = self.kwargs.get('uuid', None)
        page = Page.objects.get(uuid=uuid)
        self.url = f"/sehha/news/{page.pk}/{page.slug}/"
        return super(NewsRedirectView, self).get(request, *args, **kwargs)


class NewsUpdateView(PermissionRequiredMixin, LoginRequiredMixin,
                     generic.UpdateView):
    model = Page
    permission_required = 'sehha.change_page'
    form_class = NewsModelForm
    # fields = ['name']
    # template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        context = super(NewsUpdateView, self).get_context_data(**kwargs)

        return context

    def get_object(self, queryset=None):
        obj = self.model.objects.get(pk=self.kwargs['pk'])
        return obj

    def form_valid(self, form):
            # save cleaned post data
            clean = form.cleaned_data
            context = {}
            self.object = form.save(clean)
            return super(NewsUpdateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.is_authenticated():
        #     return redirect(reverse('org-list'))
            # raise PermissionDenied(self.get_permission_denied_message())
        if not self.has_permission():
            raise PermissionDenied(self.get_permission_denied_message())
        return super(NewsUpdateView, self).dispatch(request, *args, **kwargs)


class NewsDeleteView(PermissionRequiredMixin, generic.DeleteView):
    login_required = True
    model = Page
    permission_required = 'sehha.delete_page'
    success_message = "Deleted Successfully"
    success_url = reverse_lazy('news-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(NewsDeleteView, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = self.model.objects.get(pk=self.kwargs['pk'])
        return obj

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(NewsDeleteView, self).form_valid(form)

    def get_queryset(self):
        qs = super(NewsDeleteView, self).get_queryset()
        return qs.filter(pk=self.kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.is_authenticated():
        #     return redirect(reverse('org-list'))
            # raise PermissionDenied(self.get_permission_denied_message())
        if not self.has_permission():
            raise PermissionDenied(self.get_permission_denied_message())
        return super(NewsDeleteView, self).dispatch(request, *args, **kwargs)


class HomeView(generic.TemplateView):

    template_name = 'sehha/homepage.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['news'] = Page.objects.filter(
                          tags__name='news').multi_random(4)
        floatpage_qs = None
        try:
            floatpage_qs = FlatPage.objects.get(url='/home/')
            content_type = ContentType.objects.get(model='flatpage')
            context['images'] = Image.objects.filter(content_type=content_type,
                                                     object_id=floatpage_qs.id)
            context['flatpage'] = floatpage_qs
        except FlatPage.DoesNotExist:
            floatpage_qs = 'pls update flatpage /home/'
            context['flatpage'] = {
                'content': 'pls update flatpage /home/'
                }

        context['now'] = timezone.now()
        return context


@login_required(redirect_field_name='next')
def dashboard(request, mod=None, id=None):
    if request.method == 'POST':
        if request.POST.get('btn-news'):
            if request.POST.get('pk') != '':
                model = get_object_or_404(Page, id=request.POST.get('pk'))
                form = NewsModelForm(request.POST or None, instance=model)
                if form.is_valid():
                    form.save()
                    return redirect(
                        reverse('org-mod-id-dashboard',
                                kwargs={'mod': 'edit_news',
                                        'id': request.POST.get('pk')}))
                form = NewsModelForm()
                return render(request,
                              'sehha/dashboard/news_new.html',
                              {'form': form, 'model': model})

            else:
                form = NewsModelForm(request.POST or None)
                if form.is_valid():
                    form.save()
                    return HttpResponse('save')
                else:
                    form = NewsModelForm()
                    return render(request,
                                  'sehha/dashboard/news_new.html',
                                  {'form': form})

        if request.POST.get('pk') != '':
            model = get_object_or_404(Organization, id=request.POST.get('pk'))
            form = OrgModelForm(request.POST or None, instance=model)
            if form.is_valid():
                form.save()
                return redirect(reverse('org-mod-id-dashboard',
                                        kwargs={'mod': 'edit_org',
                                                'id': request.POST.get('pk')}))
            form = OrgModelForm()
            return render(request,
                          'sehha/dashboard/org_dashboard.html',
                          {'form': form, 'model': model})
        else:
            form = OrgModelForm(request.POST or None)
            if form.is_valid():
                form.save()
                return redirect(reverse('org-dashboard'))

    if mod == 'org_new':
        form = OrgModelForm()
        return render(request, 'sehha/dashboard/org_new.html', {'form': form})
    if mod == 'org_list':
        models = Organization.objects.all()
        return render(request, 'sehha/dashboard/org_list.html',
                               {'models': models})
    if mod == 'edit_org':
        model = Organization.objects.filter(id=id).exists()
        if model:
            model = Organization.objects.get(id=id)
        else:
            model = None
            return HttpResponse('not found')
        form = OrgModelForm(instance=model)
        return render(request, 'sehha/dashboard/org_new.html',
                               {'form': form, 'model': model})

    if mod == 'news_new':
        form = NewsModelForm(initial={'tags': 'news,'})
        return render(request, 'sehha/dashboard/news_new.html', {'form': form})
    if mod == 'news_list':
        return HttpResponse('show')
    if mod == 'edit_news':
        model = Page.objects.filter(id=id).exists()
        if model:
            model = Page.objects.get(id=id)
        else:
            model = None
            return HttpResponse('not found')
        form = NewsModelForm(instance=model)
        return render(request, 'sehha/dashboard/news_new.html', {
            'form': form, 'model': model})
    if mod is None:
        return render(request, 'sehha/dashboard/dashboard.html')


def dashboard_upload_image(request):
    if request.method == 'POST':
        file_ = request.POST.get('images')
        name = request.POST.get('name')
        return HttpResponse(file_+''+name)
    return render(request, 'sehha/dashboard/upload.html', {})


def dashboard_upload_image_bootstrip(request):
    return render(request, 'sehha/dashboard/uploadbootstrip.html', {})


@csrf_exempt
def ajax(request):
    import json
    response_data = {'status': 'failed', 'message': 'unknown error'}
    # if request.is_ajax():
    if request.method == 'POST':
        id_ = request.POST.get('id')
        response_data = {'status': 'success',
                         'message': f'deleted private message {id_}'}
    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")


@csrf_exempt
def org_create(request):
    import json
    response_data = {'status': 'failed', 'message': 'unknown error'}
    if request.method == 'POST':
        name = request.POST.get('name')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        tags = request.POST.get('tags').split(',')
        # if name and lat and lng and tags is not None:
        org = Organization()
        org.name = name
        org.lat = lat
        org.lng = lng
        org.is_active = True
        org.phone = 0
        org.fax = 0
        org.address = 0
        org.email = 'email@email.com'
        org.save()
        tags_model = org.tags
        for tag in tags:
            tags_model.add(tag)
            # tags_model.save()
        org.save()

        response_data = {'status': 'success', 'message': {
            'name': org.name, 'lat': org.lat, 'lng': org.lng}
            }
    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")


def get_all_org_api(request):
    import json
    org_api = Organization.objects.all()
    api = '['

    for org in org_api:
        api += "{'name':'"+org.name+"',"
        api += "'lat':'"+org.lat+"',"
        api += "'lng':'"+org.lng+"',"
        api += "'phone':'"+org.phone+"',"
        api += "'fax':'"+org.fax+"',"
        api += "'email':'"+org.email+"',"
        api += "'address':'"+str(org.address)+"',"
        api += "'working_time':'"+str(org.working_time)+"',"
        # api +="'lat':'"+org.lat+"',"
        tag_api = '['
        for tag in org.tags.all():
            tag_api += tag.name+','
        tag_api += ']'
        api += "'tags':'"+tag_api+"',"
        api += "},"
    api += ']'

    return HttpResponse(api)


def api_care(request):
    pass


def api_care_create(request):
    pass


def api_news(request):
    pass


def api_news_create(request):
    pass
