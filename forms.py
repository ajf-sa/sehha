from django import forms
from pagedown.widgets import PagedownWidget
from apps.images.models import Image
from pure.apps.froala_editor.widgets import FroalaEditor

from .models import Organization,Page

class OrgModelForm(forms.ModelForm):
    # captcha = CaptchaField()
    def __init__(self,*args,**kwargs):
        super(OrgModelForm,self).__init__(*args,**kwargs)


        self.fields['email'].widget.attrs['class']='form-control'
        self.fields['name'].widget.attrs['class']='form-control'
        self.fields['phone'].widget.attrs['class']='form-control'
        self.fields['fax'].widget.attrs['class']='form-control'
        # self.fields['address'].widget.attrs['class']='form-control'
        self.fields['tags'].widget.attrs['class']='form-control'
        # self.fields['lat'].widget.attrs['class']='form-control'
        # self.fields['lng'].widget.attrs['class']='form-control'
        # self.fields['create_by'].widget = forms.HiddenInput()
        self.fields['lat'].widget = forms.HiddenInput()
        self.fields['lng'].widget = forms.HiddenInput()
        self.fields['content'].widget.attrs['class']='form-control'
        self.fields['working_time'].widget.attrs['class']='form-control'


    class Meta:
        model = Organization
        exclude =('is_active','create_by','address')
        labels={
        'name':'اسم المنشأة الصحي',
        'phone':'الهاتف',
        'fax': 'الفاكس',
        'email':'البريد الالكتروني',
        'address':'العنوان',
        'content':'نبذه عن',
        'working_time':'اوقات العمل',
        }




class NewsModelForm(forms.ModelForm):
    #body =forms.CharField(widget=TinyMCE(attrs={'cols': 180, 'rows': 10}))
    #create_by =forms.CharField()
    body = forms.CharField(widget=PagedownWidget)

    def __init__(self,*args,**kwargs):
        super(NewsModelForm,self).__init__(*args,**kwargs)
        self.fields['create_by'].widget = forms.HiddenInput()
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['subtitle'].widget.attrs['class'] = 'form-control'
        self.fields['thumbnail'].widget = forms.HiddenInput()
        self.fields['tags'].widget.attrs['readonly'] = True
        # self.fields['body'].widget.attrs['class'] = 'form-control content-markdown'
    #    self.fields['tags'].widget.attrs['class'] = 'form-control'
    # def save(self,commit=True):
    #     page = super(NewsModelForm,self).save(commit=False)
    #     page.tags.clear()
    #     if commit:
    #         page.save()
    #         page.tags.add(*list(self.cleaned_data['tags']))
    #         page.save()
    class Meta:
        model = Page
        exclude = ('slug','org','is_active',)
        labels ={
            'title':'العنوان',
            'subtitle' : "عنوان ثاني" ,
            'body' : "النص",
        }

class ImageModelForm(forms.ModelForm):


    class Meta:
        model = Image
        fields=('image',)
