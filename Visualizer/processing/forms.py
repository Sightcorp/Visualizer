from django import forms
from database.models import *
import datetime

class StartSessionForm( forms.Form ):
    source_name = forms.CharField( max_length = 80 )

    source_model = None

    def clean_source_name( self ):
        ( self.source_model, created ) = Source.objects.get_or_create( label = self.cleaned_data[ 'source_name' ] )
        return self.cleaned_data[ 'source_name' ]

class StopSessionForm( forms.Form ):
    session_key = forms.CharField( max_length = 32 )

    session_model = None

    def clean_session_key( self ):
        self.session_model = Session.objects.get( key = self.cleaned_data[ 'session_key' ] )
        if self.session_model == None:
            raise forms.ValidationError( 'Session does not exists' )
        return self.cleaned_data[ 'session_key' ]

class PersonDetectionForm( forms.ModelForm ):
    class Meta:
        model = Person_img
        exclude = ( 'id_img', 'id_person', 'timestamp', )

    session_key = forms.CharField( max_length = 32 )
    frame       = forms.IntegerField( required = False ) #, min_value = 1 ) # TODO : Diego : Fix this
    sdk_name    = forms.CharField( max_length = 30 )

    session_model = None
    person_model  = None
    sdk_name_cleaned = None

    # TODO : Diego : Clean clothing color
    def clean_session_key( self ):
        self.session_model = Session.objects.get( key = self.cleaned_data[ 'session_key' ] )
        if self.session_model == None:
            raise forms.ValidationError( 'Session does not exists' )
        return self.cleaned_data[ 'session_key' ]

    def clean( self ):
        cleaned_data = super( PersonDetectionForm, self ).clean()
        ( self.person_model, created ) = self.session_model.person_set.get_or_create( sdk_name = self.cleaned_data[ 'sdk_name' ], id_source = self.session_model.id_source )
        if created:
            self.person_model.start = datetime.datetime.now()
        else:
            self.person_model.end = datetime.datetime.now()
        self.person_model.save()  

        return cleaned_data

    def get_validation_error( self ):
        for field in self.errors:
            return field.capitalize() + " is not valid : " + repr( self.errors[ field ] )

        try:
            return self.non_field_errors()[0]
        except:
            return ''
