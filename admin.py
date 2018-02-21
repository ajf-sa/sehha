from django.contrib import admin
from django import forms
from sehha.models import Organization, Unit, Page


class UnitInline(admin.StackedInline):
    fields = ('name', 'phone', 'fax', 'email')
    model = Unit


class CustomOrgForm(forms.ModelForm):
    # create_by = forms.CharField(disabled=True,)

    class Meta:
        model = Organization
        fields = "__all__"


class OrgModelAdmin(admin.ModelAdmin):

    form = CustomOrgForm
    list_filter = ['tags']
    inlines = [UnitInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super(OrgModelAdmin, self).get_form(request, obj, **kwargs)
    #    form.base_fields['create_by'].initial=request.user

        return form


admin.site.register(Organization, OrgModelAdmin)
admin.site.register(Unit)
admin.site.register(Page)
