from django.contrib.sites.models import Site
from django.shortcuts import reverse
from .models import Page, Organization


def is_care():
    care = Organization.objects.actived().count()
    if care >0:
        return True
    return False

def site(request):  # make site gloable
    urls = {
            'site': Site.objects.get_current(),
            'get_home_url': reverse('org_home'),
            'get_administration_url': reverse(
                'django.contrib.flatpages.views.flatpage',
                kwargs={'url': 'administration/'}),
            'get_org_list_url': reverse('org-list'),
            'get_news_list_url': reverse('news-list'),
            'get_login_url': reverse('account_login'),
            'get-register_url': reverse('account_signup'),
            'get_logout_url': reverse('account_logout'),
            'managements': Page.objects.filter(tags__name='management',
                                               is_active=True),
            'cares': Organization.objects.actived().multi_random(5),
            'is_care': is_care(),

        }

    return urls
