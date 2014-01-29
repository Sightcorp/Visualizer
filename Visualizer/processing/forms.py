from django import forms

class StartSessionForm( forms.Form ):
    source_name = forms.CharField( max_length = 80 )

    source_model = None

    def clean_source_name( self ):
        source_model = Source.objects.get_or_create( label = self.cleaned_data[ 'source_name' ] )

class StopSessionForm( forms.Form ):
    session_key = forms.CharField( max_length = 32 )

    session_model = None

    def clean_session_key( self ):
        try:
            session_model = Session.objects.get( label = self.cleaned_data[ 'session_key' ] )
        except:
            raise forms.ValidationError( 'Session does not exists' )

class PersonDetectionForm( forms.ModelForm ):
    class Meta:
        model = Person_img
        exclude = ( 'id_img', 'id_person', 'timestamp', )

    session_key = forms.CharField( max_length = 32 )
    frame       = models.IntegerField( required = False, min_value = 1 )
    sdk_name    = forms.CharField( max_length = 30 )

    session_model = None
    person_model  = None

    # TODO : Diego : Clean clothing color
    def clean_session_key( self ):
        try:
            session_model = Session.objects.get( label = self.cleaned_data[ 'session_key' ] )
        except:
            raise forms.ValidationError( 'Session does not exists' )

    def clean( self ):
        person_model = self.session_model.person_set.get_or_create( sdk_name = self.cleaned_data[ 'sdk_name' ] )
