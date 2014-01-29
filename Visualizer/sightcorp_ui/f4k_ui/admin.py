#from f4k_ui.db.models import SummaryCamera37, SummaryCamera38, SummaryCamera39, SummaryCamera40, SummaryCamera41, SummaryCamera42, SummaryCamera43, SummaryCamera44, SummaryCamera46, Species
from f4k_ui.db.models import Source, Dataset, Session, Person, Person_img
from django.contrib import admin

######################################################

class PersonAdmin(admin.ModelAdmin):
    list_display = ("id_person", "id_source", "start", "end", "gender_av", "gender_sd", "age_av", "age_sd", "mood_av", "mood_sd", "happy_av", "happy_sd", "surprised_av", "surprised_sd", "angry_av", "angry_sd", "disgusted_av", 'disgusted_sd', "afraid_av", "afraid_sd", "sad_av", "sad_sd")
    search_fields = ['id_person']
    date_hierarchy = 'start'

class SourceAdmin(admin.ModelAdmin):
    list_display = ("id_source", "label")
    search_fields = ['id_source']

admin.site.register(Person, PersonAdmin)
admin.site.register(Source, SourceAdmin)

######################################################

'''
class SummaryCamera37Admin(admin.ModelAdmin):
    list_display = ("fish_id", "species_id", "det_certainty", "tracking_certainty", "rec_certainty", 'det_component_id',
                    'rec_component_id', "date")
    search_fields = ['fish_id']
    date_hierarchy = 'date'
    list_filter = ['species_id']


class SummaryCamera38Admin(admin.ModelAdmin):
    list_display = ("fish_id", "species_id", "det_certainty", "tracking_certainty", "rec_certainty", 'det_component_id',
                    'rec_component_id', "date")
    search_fields = ['fish_id']
    date_hierarchy = 'date'
    list_filter = ['species_id']


class SummaryCamera39Admin(admin.ModelAdmin):
    list_display = ("fish_id", "species_id", "det_certainty", "tracking_certainty", "rec_certainty", 'det_component_id',
                    'rec_component_id', "date")
    search_fields = ['fish_id']
    date_hierarchy = 'date'
    list_filter = ['species_id']


class SummaryCamera40Admin(admin.ModelAdmin):
    list_display = ("fish_id", "species_id", "det_certainty", "tracking_certainty", "rec_certainty", 'det_component_id',
                    'rec_component_id', "date")
    search_fields = ['fish_id']
    date_hierarchy = 'date'
    list_filter = ['species_id']


class SummaryCamera41Admin(admin.ModelAdmin):
    list_display = ("fish_id", "species_id", "det_certainty", "tracking_certainty", "rec_certainty", 'det_component_id',
                    'rec_component_id', "date")
    search_fields = ['fish_id']
    date_hierarchy = 'date'
    list_filter = ['species_id']


class SummaryCamera42Admin(admin.ModelAdmin):
    list_display = ("fish_id", "species_id", "det_certainty", "tracking_certainty", "rec_certainty", 'det_component_id',
                    'rec_component_id', "date")
    search_fields = ['fish_id']
    date_hierarchy = 'date'
    list_filter = ['species_id']


class SummaryCamera43Admin(admin.ModelAdmin):
    list_display = ("fish_id", "species_id", "det_certainty", "tracking_certainty", "rec_certainty", 'det_component_id',
                    'rec_component_id', "date")
    search_fields = ['fish_id']
    date_hierarchy = 'date'
    list_filter = ['species_id']


class SummaryCamera44Admin(admin.ModelAdmin):
    list_display = ("fish_id", "species_id", "det_certainty", "tracking_certainty", "rec_certainty", 'det_component_id',
                    'rec_component_id', "date")
    search_fields = ['fish_id']
    date_hierarchy = 'date'
    list_filter = ['species_id']


class SummaryCamera46Admin(admin.ModelAdmin):
    list_display = ("fish_id", "species_id", "det_certainty", "tracking_certainty", "rec_certainty", 'det_component_id',
                    'rec_component_id', "date")
    search_fields = ['fish_id']
    date_hierarchy = 'date'
    list_filter = ['species_id']


class SpeciesAdmin(admin.ModelAdmin):
    list_display = ("species_id", "name")
    search_fields = ['name']


admin.site.register(SummaryCamera37, SummaryCamera37Admin)
admin.site.register(SummaryCamera38, SummaryCamera38Admin)
admin.site.register(SummaryCamera39, SummaryCamera39Admin)
admin.site.register(SummaryCamera40, SummaryCamera40Admin)
admin.site.register(SummaryCamera41, SummaryCamera41Admin)
admin.site.register(SummaryCamera42, SummaryCamera42Admin)
admin.site.register(SummaryCamera43, SummaryCamera43Admin)
admin.site.register(SummaryCamera44, SummaryCamera44Admin)
admin.site.register(SummaryCamera46, SummaryCamera46Admin)
admin.site.register(Species, SpeciesAdmin)

'''
