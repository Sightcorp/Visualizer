from django.db import models
#from f4k_ui.db.managers import SummaryCameraManager, CamerasManager, SpeciesManager, VideoManager, UserQueryManager
#from f4k_ui.db.managers import PersonManager, SourceManager

import uuid

# End utilities
def generate_hash():
    return uuid.uuid4().hex
# End utilities

class Source( models.Model ):
#    class Meta:
#        app_label = 'f4k_ui'    
    id_source   = models.AutoField(primary_key=True)
    label       = models.CharField( max_length = 80, unique = True )
    description = models.TextField( null = True, blank = True )

#    objects = SourceManager()

class Dataset( models.Model ):
#    class Meta:
#        app_label = 'f4k_ui'    
    id_dataset  = models.AutoField(primary_key=True)
    label       = models.CharField( max_length = 80, unique = True )
    description = models.TextField( null = True, blank = True )

class Session( models.Model ):
#    class Meta:
#        app_label = 'f4k_ui'    
    id_session  = models.AutoField(primary_key=True)
    key         = models.CharField( max_length = 32, unique = True, default = generate_hash )
    name        = models.CharField( max_length = 40, null = True )
    dataset     = models.ForeignKey( Dataset, null = True )
    id_source   = models.ForeignKey( Source )
    start_time  = models.DateTimeField( null = True, blank = True )
    end_time    = models.DateTimeField( null = True, blank = True )

class Person( models.Model ):
    id_person      = models.AutoField(primary_key=True)
    sdk_name       = models.CharField( max_length = 30 )
    id_source      = models.ForeignKey( Source )
    id_session     = models.ForeignKey( Session )
    start          = models.DateTimeField( null = True, blank = True )
    end            = models.DateTimeField( null = True, blank = True )
    gender_av      = models.SmallIntegerField( null = True )
    gender_sd      = models.SmallIntegerField( null = True )
    age_av         = models.PositiveSmallIntegerField( null = True )
    age_sd         = models.PositiveSmallIntegerField( null = True )
    mood_av        = models.SmallIntegerField( null = True )
    mood_sd        = models.SmallIntegerField( null = True )
    gaze_x_av      = models.SmallIntegerField( null = True )
    gaze_x_sd      = models.SmallIntegerField( null = True )
    gaze_y_av      = models.SmallIntegerField( null = True )
    gaze_y_sd      = models.SmallIntegerField( null = True )
    attention_span = models.IntegerField( null = True )
    neutral_av     = models.PositiveSmallIntegerField( null = True )
    neutral_sd     = models.PositiveSmallIntegerField( null = True )
    happy_av       = models.PositiveSmallIntegerField( null = True )
    happy_sd       = models.PositiveSmallIntegerField( null = True )
    surprised_av   = models.PositiveSmallIntegerField( null = True )
    surprised_sd   = models.PositiveSmallIntegerField( null = True )
    angry_av       = models.PositiveSmallIntegerField( null = True )
    angry_sd       = models.PositiveSmallIntegerField( null = True )
    disgusted_av   = models.PositiveSmallIntegerField( null = True )
    disgusted_sd   = models.PositiveSmallIntegerField( null = True )
    afraid_av      = models.PositiveSmallIntegerField( null = True )
    afraid_sd      = models.PositiveSmallIntegerField( null = True )
    sad_av         = models.PositiveSmallIntegerField( null = True )
    sad_sd         = models.PositiveSmallIntegerField( null = True )
    color_1        = models.CharField( max_length = 6, null = True )
    color_2        = models.CharField( max_length = 6, null = True )
    color_3        = models.CharField( max_length = 6, null = True )

    def compute_averages( self ):
        person_detections = self.person_img_set.all()
        count = len( person_detections )
        if count == 0:
            return

        average_fn = lambda arr, member, _count : sum( [ getattr( x, member ) for x in arr ] ) / ( float )( _count )
        std_dev_fn = lambda arr, member, _count, avg : ( sum( [ ( getattr( x, member ) - avg )  ** 2 for x in arr ] ) / ( float )( _count ) ) ** 0.5

        self.gender_av      = average_fn( person_detections, "gender", count )
        self.gender_sd      = std_dev_fn( person_detections, "gender", count, self.gender_av )
        self.age_av         = average_fn( person_detections, "age", count )
        self.age_sd         = std_dev_fn( person_detections, "age", count, self.age_av )

        self.mood_av        = average_fn( person_detections, "mood", count )
        self.mood_sd        = std_dev_fn( person_detections, "mood", count, self.mood_av )
        #self.gaze_x_av      = average_fn( person_detections, "bbb", count )
        #self.gaze_x_sd      = average_fn( person_detections, "bbb", count, self.gaze_x_av )
        #self.gaze_y_av      = average_fn( person_detections, "bbb", count )
        #self.gaze_y_sd      = average_fn( person_detections, "bbb", count, self.gaze_y_av )
        #self.attention_span = average_fn( person_detections, "bbb", count, ddd )

        self.neutral_av     = average_fn( person_detections, "neutral", count )
        self.neutral_sd     = std_dev_fn( person_detections, "neutral", count, self.neutral_av )
        self.happy_av       = average_fn( person_detections, "happy", count )
        self.happy_sd       = std_dev_fn( person_detections, "happy", count, self.happy_av )
        self.surprised_av   = average_fn( person_detections, "surprised", count )
        self.surprised_sd   = std_dev_fn( person_detections, "surprised", count, self.surprised_av )
        self.angry_av       = average_fn( person_detections, "angry", count )
        self.angry_sd       = std_dev_fn( person_detections, "angry", count, self.angry_av )
        self.disgusted_av   = average_fn( person_detections, "disgusted", count )
        self.disgusted_sd   = std_dev_fn( person_detections, "disgusted", count, self.disgusted_av )
        self.afraid_av      = average_fn( person_detections, "afraid", count )
        self.afraid_sd      = std_dev_fn( person_detections, "afraid", count, self.afraid_av )
        self.sad_av         = average_fn( person_detections, "sad", count )
        self.sad_sd         = std_dev_fn( person_detections, "sad", count, self.sad_av )

        self.save()
        #self.color_1        = average_fn( person_detections, "bbb", count, ddd )
        #self.color_2        = average_fn( person_detections, "bbb", count, ddd )
        #self.color_3        = average_fn( person_detections, "bbb", count, ddd )

#    objects = PersonManager()

#    class Meta:
#        app_label = 'f4k_ui'    

class Person_img( models.Model ):
#    class Meta:
#        app_label = 'f4k_ui'    
    id_img          = models.AutoField(primary_key=True)
    id_person       = models.ForeignKey( Person, null = True )
    #id_source       = models.ForeignKey( Source )
    timestamp       = models.DateTimeField( auto_now_add = True )
    frame           = models.PositiveIntegerField( default = 0 ) # Ordinal number. 0 means not part of a sequence (single frame)
    age             = models.PositiveSmallIntegerField()
    gender          = models.SmallIntegerField()
    mood            = models.SmallIntegerField()
    facePosition_x  = models.SmallIntegerField()
    facePosition_y  = models.SmallIntegerField()
    facePosition_w  = models.SmallIntegerField()
    facePosition_h  = models.SmallIntegerField()
    headYaw         = models.FloatField()
    headPitch       = models.FloatField()
    rightEye_x      = models.SmallIntegerField()
    rightEye_y      = models.SmallIntegerField()
    leftEye_x       = models.SmallIntegerField()
    leftEye_y       = models.SmallIntegerField()
    head_roll       = models.FloatField()
    attention_span  = models.IntegerField( null = True )
    neutral         = models.PositiveSmallIntegerField()
    happy           = models.PositiveSmallIntegerField()
    surprised       = models.PositiveSmallIntegerField()
    angry           = models.PositiveSmallIntegerField()
    disgusted       = models.PositiveSmallIntegerField()
    afraid          = models.PositiveSmallIntegerField()
    sad             = models.PositiveSmallIntegerField()
    ClothesColors_1 = models.CharField( max_length = 6, null = True, blank = True )
    ClothesColors_2 = models.CharField( max_length = 6, null = True, blank = True )
    ClothesColors_3 = models.CharField( max_length = 6, null = True, blank = True )

