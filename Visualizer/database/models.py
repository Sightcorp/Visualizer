from django.db import models

import uuid

# End utilities
def generate_hash():
    return uuid.uuid4().hex
# End utilities

class Source( models.Model ):
    id_source   = models.IntegerField(primary_key=True)
    label       = models.CharField( max_length = 80 )
    description = models.TextField( null = True, blank = True )

class Dataset( models.Model ):
    id_dataset  = models.IntegerField(primary_key=True)
    label       = models.CharField( max_length = 80 )
    description = models.TextField( null = True, blank = True )

class Session( models.Model ): # WHY NOT MERGING DATASET AND SESSION TABLES TOGETHER?
    id_session  = models.IntegerField(primary_key=True)
    key         = models.CharField( max_length = 32, unique = True, default = generate_hash )
    name        = models.CharField( max_length = 40, null = True )
    dataset     = models.ForeignKey( Dataset, null = True )
    start_time  = models.DateTimeField( null = True, blank = True )
    end_time    = models.DateTimeField( null = True, blank = True )

class Person( models.Model ):
    id_person      = models.IntegerField(primary_key=True)
   # name          = models.CharField( max_length = 40, null = True )
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

class Person_img( models.Model ):
    id_img          = models.IntegerField(primary_key=True)
    id_person       = models.ForeignKey( Person, null = True )
    #source          = models.ForeignKey( Source )
    timestamp       = models.DateTimeField( auto_now_add = True )
    frame           = models.PositiveIntegerField( default = 0 ) # Ordinal number. 0 means not part of a sequence (single frame)
    age             = models.PositiveSmallIntegerField()
    mood            = models.SmallIntegerField()
    facePosition_x  = models.SmallIntegerField()
    facePosition_y  = models.SmallIntegerField()
    facePosition_w  = models.SmallIntegerField()
    facePosition_h  = models.SmallIntegerField()
    headYaw         = models.DecimalField( max_digits = 8, decimal_places = 6 )
    headPitch       = models.DecimalField( max_digits = 8, decimal_places = 6 )
    rightEye_x      = models.SmallIntegerField()
    rightEye_y      = models.SmallIntegerField()
    leftEye_x       = models.SmallIntegerField()
    leftEye_y       = models.SmallIntegerField()
    head_roll       = models.DecimalField( max_digits = 8, decimal_places = 6 )
    attention_span  = models.IntegerField( null = True )
    neutral         = models.PositiveSmallIntegerField()
    happy           = models.PositiveSmallIntegerField()
    surprised       = models.PositiveSmallIntegerField()
    angry           = models.PositiveSmallIntegerField()
    disgusted       = models.PositiveSmallIntegerField()
    afraid          = models.PositiveSmallIntegerField()
    sad             = models.PositiveSmallIntegerField()
    ClothesColors_1         = models.CharField( max_length = 6, null = True )
    ClothesColors_2         = models.CharField( max_length = 6, null = True )
    ClothesColors_3         = models.CharField( max_length = 6, null = True )

