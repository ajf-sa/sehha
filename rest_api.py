import json
from django.shortcuts import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework import viewsets
from .models import Organization , Page


class CareSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    class Meta :
        model=Organization
        fields =('name','uuid','lat','lng','phone','fax','email','address','content','working_time','tags')
class CareViewSet(viewsets.ModelViewSet):
    queryset= Organization.objects.all().order_by('create_at')
    serializer_class = CareSerializer


class ManageSerializer(serializers.ModelSerializer):
    def save(self,**kwargs):
        obj = super(ManageSerializer,self).save(**kwargs)
        obj.tags.add('management')
        obj.is_active=True
        obj.save()
    class Meta :
        model = Page
        fields = ('pk','title','subtitle','body')


class NewsSerializer(serializers.ModelSerializer):
    def save(self,**kwargs):
        obj = super(NewsSerializer,self).save(**kwargs)
        obj.tags.add('news')
        obj.is_active=True
        obj.save()
    class Meta :
        model = Page
        fields = ('pk','title','subtitle','body')

# class PageViewSet(viewsets.ModelViewSet):
#     intit_tags ='news'
#     queryset = Page.objects.filter(tags__name=intit_tags,is_active=True).order_by('-create_at')
#     serializer_class = PageSerializer

class NewsViewSet(viewsets.ModelViewSet):

    queryset = Page.objects.filter(tags__name='news',is_active=True).order_by('-create_at')
    serializer_class = NewsSerializer

class ManagementViewSet(NewsViewSet):
    queryset = Page.objects.filter(tags__name='management',is_active=True).order_by('-create_at')
    serializer_class = ManageSerializer



@csrf_exempt
def get_all_org(request):

    if request.method == 'POST':
        return HttpResponse('POST')
    elif request.method == 'GET':
        return HttpResponse('GET')
    return HttpResponse('error')
