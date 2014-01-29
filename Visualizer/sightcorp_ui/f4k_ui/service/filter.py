import logging
from f4k_ui.db import util
from f4k_ui.db.models import Person, Source
from f4k_ui.parameters import VisualizationParameters

class FilterService:
    ### Maybe that's what's making l.18-38 in views.py useless..
    def __init__(self, species_names, cameras_names):
        self.species_names = species_names
        self.cameras_names = cameras_names
    ###
    def process_request(self, request):
        parameters = VisualizationParameters(request, self.species_names)
        
        logging.info("Requesting Filters - data: %s" % parameters)

        response = {}
        if 'f_c' in parameters.opened_filters():
            response['f_c'] = self.filter_cameras(parameters)
        if 'f_d' in parameters.opened_filters():
            response['f_d'] = self.filter_time('d', parameters.filter_days(), parameters)
        if 'f_h' in parameters.opened_filters():
            response['f_h'] = self.filter_time('h', parameters.filter_hours(), parameters)
        if 'f_mood' in parameters.opened_filters():
            response['f_mood'] = self.filter_moods(parameters)
        if 'f_gen' in parameters.opened_filters():
            response['f_gen'] = self.filter_genders(parameters)
        if 'f_age' in parameters.opened_filters():
            response['f_age'] = self.filter_ages(parameters)
        if 'f_hap' in parameters.opened_filters():
            response['f_hap'] = self.filter_happys(parameters)
        if 'f_dis' in parameters.opened_filters():
            response['f_dis'] = self.filter_disgusteds(parameters)
        if 'f_ang' in parameters.opened_filters():
            response['f_ang'] = self.filter_angrys(parameters)
        if 'f_sur' in parameters.opened_filters():
            response['f_sur'] = self.filter_surpriseds(parameters)
        if 'f_afr' in parameters.opened_filters():
            response['f_afr'] = self.filter_afraids(parameters)
        if 'f_sad' in parameters.opened_filters():
            response['f_sad'] = self.filter_sads(parameters)

        logging.debug("Response Filters - computed.")
        return response

    def filter_time(self, x_axis, x_selected_values, parameters):
        y_axis = parameters.y().lower()

        final_counts = []

        if x_axis == 'd':
            final_counts = [[i,0] for i in range(4,7)]
        elif x_axis == 'h':
            final_counts = [[i,0] for i in range(24)]

        if y_axis == 'np':
            count = Person.objects.person_count(x_axis, parameters)
            final_counts = util.add_counts_multicol(final_counts, count)

        return util.set_selected_value(final_counts, x_selected_values)
        
    def filter_cameras(self, parameters):
        y_axis = parameters.y().lower()
        x_selected_values = parameters.filter_cameras()

        final_counts = [[i,0] for i in range(1,4)]

        if y_axis == 'np':
            count = Person.objects.person_count('c', parameters)
            final_counts = util.add_counts_multicol(final_counts, count)

        return util.set_selected_value(final_counts, x_selected_values)

    def filter_moods(self, parameters):
        y_axis = parameters.y().lower()
        x_selected_values = parameters.filter_moods()

        final_counts = [[i,0] for i in [-100,-90,-80,-70,-60,-50,-40,-30,-20,-10,0,10,20,30,40,50,60,70,80,90,100]]

        if y_axis == 'np':
            count = Person.objects.person_count('mood_filter', parameters)
            final_counts = util.add_counts_multicol(final_counts, count)
            #final_counts = Person.objects.person_count('mood', parameters)

        return util.set_selected_value(final_counts, x_selected_values)

    def filter_genders(self, parameters):
        y_axis = parameters.y().lower()
        x_selected_values = parameters.filter_genders()

        final_counts = [[i,0] for i in [-100,-90,-80,-70,-60,-50,-40,-30,-20,-10,0,10,20,30,40,50,60,70,80,90,100]]

        if y_axis == 'np':
            count = Person.objects.person_count('gen_filter', parameters)
            final_counts = util.add_counts_multicol(final_counts, count)

        return util.set_selected_value(final_counts, x_selected_values)

    def filter_ages(self, parameters):
        y_axis = parameters.y().lower()
        x_selected_values = parameters.filter_ages()

        final_counts = [[i,0] for i in [0,10,20,30,40,50,60,70,80,90,100]]

        if y_axis == 'np':
            count = Person.objects.person_count('age_filter', parameters)
            final_counts = util.add_counts_multicol(final_counts, count)

        return util.set_selected_value(final_counts, x_selected_values)

    def filter_happys(self, parameters):
        y_axis = parameters.y().lower()
        x_selected_values = parameters.filter_happys()

        final_counts = [[i,0] for i in [0,10,20,30,40,50,60,70,80,90,100]]

        if y_axis == 'np':
            count = Person.objects.person_count('hap_filter', parameters)
            final_counts = util.add_counts_multicol(final_counts, count)

        return util.set_selected_value(final_counts, x_selected_values)

    def filter_disgusteds(self, parameters):
        y_axis = parameters.y().lower()
        x_selected_values = parameters.filter_disgusteds()

        final_counts = [[i,0] for i in [0,10,20,30,40,50,60,70,80,90,100]]

        if y_axis == 'np':
            count = Person.objects.person_count('dis_filter', parameters)
            final_counts = util.add_counts_multicol(final_counts, count)

        return util.set_selected_value(final_counts, x_selected_values)

    def filter_angrys(self, parameters):
        y_axis = parameters.y().lower()
        x_selected_values = parameters.filter_angrys()

        final_counts = [[i,0] for i in [0,10,20,30,40,50,60,70,80,90,100]]

        if y_axis == 'np':
            count = Person.objects.person_count('ang_filter', parameters)
            final_counts = util.add_counts_multicol(final_counts, count)

        return util.set_selected_value(final_counts, x_selected_values)

    def filter_surpriseds(self, parameters):
        y_axis = parameters.y().lower()
        x_selected_values = parameters.filter_surpriseds()

        final_counts = [[i,0] for i in [0,10,20,30,40,50,60,70,80,90,100]]

        if y_axis == 'np':
            count = Person.objects.person_count('sur_filter', parameters)
            final_counts = util.add_counts_multicol(final_counts, count)

        return util.set_selected_value(final_counts, x_selected_values)

    def filter_afraids(self, parameters):
        y_axis = parameters.y().lower()
        x_selected_values = parameters.filter_afraids()

        final_counts = [[i,0] for i in [0,10,20,30,40,50,60,70,80,90,100]]

        if y_axis == 'np':
            count = Person.objects.person_count('afr_filter', parameters)
            final_counts = util.add_counts_multicol(final_counts, count)

        return util.set_selected_value(final_counts, x_selected_values)

    def filter_sads(self, parameters):
        y_axis = parameters.y().lower()
        x_selected_values = parameters.filter_sads()

        final_counts = [[i,0] for i in [0,10,20,30,40,50,60,70,80,90,100]]

        if y_axis == 'np':
            count = Person.objects.person_count('sad_filter', parameters)
            final_counts = util.add_counts_multicol(final_counts, count)

        return util.set_selected_value(final_counts, x_selected_values)
