from django.db import models

import uuid

# End utilities
def generate_hash():
    return uuid.uuid4().hex
# End utilities

class Source( models.Model ):
    label       = models.CharField( max_length = 80 )
    description = models.TextField( null = True, blank = True )

class Dataset( models.Model ):
    label       = models.CharField( max_length = 80 )
    description = models.TextField( null = True, blank = True )

class Session( models.Model ):
    key         = models.CharField( max_length = 32, unique = True, default = generate_hash )
    name        = models.CharField( max_length = 40, null = True )
    dataset     = models.ForeignKey( Dataset, null = True )
    start_time  = models.DateTimeField( null = True, blank = True )
    end_time    = models.DateTimeField( null = True, blank = True )

class Person( models.Model ):
    name           = models.CharField( max_length = 40, null = True )
    session        = models.ForeignKey( Session )
    start_time     = models.DateTimeField( null = True, blank = True )
    end_time       = models.DateTimeField( null = True, blank = True )
    gender_av      = models.SmallIntegerField( null = True )
    gender_sd      = models.SmallIntegerField( null = True )
    age_av         = models.PositiveSmallIntegerField( null = True )
    age_sd         = models.PositiveSmallIntegerField( null = True )
    gaze_x_av      = models.SmallIntegerField( null = True )
    gaze_x_sd      = models.SmallIntegerField( null = True )
    gaze_y_av      = models.SmallIntegerField( null = True )
    gaze_y_sd      = models.SmallIntegerField( null = True )
    attention_span = models.IntegerField( null = True )
    mood_av        = models.SmallIntegerField( null = True )
    mood_sd        = models.SmallIntegerField( null = True )
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

class Person_detection( models.Model ):
    person          = models.ForeignKey( Person, null = True )
    source          = models.ForeignKey( Source )
    time_stamp      = models.DateTimeField( auto_now_add = True )
    frame           = models.PositiveIntegerField( default = 0 ) # Ordinal number. 0 means not part of a sequence (single frame)
    age             = models.PositiveSmallIntegerField()
    face_position_x = models.SmallIntegerField()
    face_position_y = models.SmallIntegerField()
    face_position_w = models.SmallIntegerField()
    face_position_h = models.SmallIntegerField()
    right_eye_x     = models.SmallIntegerField()
    right_eye_y     = models.SmallIntegerField()
    left_eye_x      = models.SmallIntegerField()
    left_eye_y      = models.SmallIntegerField()
    head_yaw        = models.DecimalField( max_digits = 8, decimal_places = 6 )
    head_pitch      = models.DecimalField( max_digits = 8, decimal_places = 6 )
    head_roll       = models.DecimalField( max_digits = 8, decimal_places = 6 )
    attention_span  = models.IntegerField( null = True )
    mood            = models.SmallIntegerField()
    neutral         = models.PositiveSmallIntegerField()
    happy           = models.PositiveSmallIntegerField()
    surprised       = models.PositiveSmallIntegerField()
    angry           = models.PositiveSmallIntegerField()
    disgusted       = models.PositiveSmallIntegerField()
    afraid          = models.PositiveSmallIntegerField()
    sad             = models.PositiveSmallIntegerField()
    color_1         = models.CharField( max_length = 6, null = True )
    color_2         = models.CharField( max_length = 6, null = True )
    color_3         = models.CharField( max_length = 6, null = True )

