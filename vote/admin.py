from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ZipCodeResource(resources.ModelResource):
    class Meta:
        model = ZipCode


class ZipCodeAdmin(ImportExportModelAdmin):
    resource_classes = [ZipCodeResource]
    search_fields = ['zip', 'primary_city']
    list_display = ['state', 'zip', 'primary_city', 'county', 'latitude', 'longitude', 'irs_estimated_population']
    list_filter = ['state',]
    ordering = ['state', 'zip', 'primary_city']


admin.site.register(ZipCode, ZipCodeAdmin)
admin.site.register(AgeRange)
admin.site.register(Voter)
admin.site.register(Question)
admin.site.register(QuestionImage)
admin.site.register(Vote)
admin.site.register(VoterQuestion)

