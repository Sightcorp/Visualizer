import logging
from f4k_ui.db import util
from f4k_ui.db.models import Person, Source
from f4k_ui.parameters import VisualizationParameters

class VizService:
    def __init__(self, species_names):
        self.species_names = species_names

    def process_request(self, request):
        parameters = VisualizationParameters(request, self.species_names)
        #? Change into: parameters = VisualizationParameters(request)
        logging.info("Requesting Chart - data: %s" % parameters)

        data = None
        t = parameters.t().lower()
        z = parameters.z().lower()
        if t == 's':
            data = self.simple(parameters)
        elif t == 't':

            if z == "c":
                data = self.stacked_cameras(parameters)
            if z == "d":
                data = self.stacked_days(parameters)
            if z == "h":
                data = self.stacked_hours(parameters)
            if z == "mood":
                data = self.stacked_moods(parameters)
            if z == "gen":
                data = self.stacked_genders(parameters)
            if z == "age":
                data = self.stacked_ages(parameters)
            if z == "hap":
                data = self.stacked_happys(parameters)
            if z == "dis":
                data = self.stacked_disgusteds(parameters)
            if z == "ang":
                data = self.stacked_angrys(parameters)
            if z == "sur":
                data = self.stacked_surpriseds(parameters)
            if z == "afr":
                data = self.stacked_afraids(parameters)
            if z == "sad":
                data = self.stacked_sads(parameters)

        if data is None:
            logging.warning('Dimensions t: %s, z: %s is NOT implemented.' % (t, z))

        logging.debug("Response Chart - computed.")
        return {'viz': data}

    def simple(self, parameters):
        x_axis = parameters.x().lower()

        if x_axis == 'd':
            counts = [[i,0] for i in range(4,7)]
        elif x_axis == 'h':
            counts = [[i,0] for i in range(24)]
        elif x_axis == 'c':
            counts = [[i,0] for i in range(1,4)]
        elif x_axis == 'mood':
            counts = [[i,0] for i in range(-100,100)]
        elif x_axis == 'gen':
            counts = [[i,0] for i in range(-100,100)]
        elif x_axis == 'age':
            counts = [[i,0] for i in range(0,100)]
        elif x_axis == 'hap':
            counts = [[i,0] for i in range(0,100)]
        elif x_axis == 'dis':
            counts = [[i,0] for i in range(0,100)]
        elif x_axis == 'ang':
            counts = [[i,0] for i in range(0,100)]
        elif x_axis == 'sur':
            counts = [[i,0] for i in range(0,100)]
        elif x_axis == 'afr':
            counts = [[i,0] for i in range(0,100)]
        elif x_axis == 'sad':
            counts = [[i,0] for i in range(0,100)]
        else:
            counts = []

        count = Person.objects.person_count(x_axis, parameters)
        counts = util.add_counts_multicol(counts, count)

        return counts

    def stacked_cameras(self, parameters):
        res = None
        y = parameters.y().lower()
        if y == 'np':
            res = self.cameras_decomposition_raw(parameters)
        return self.fix_missing_x_groupings(res)
    def stacked_days(self, parameters):
        res = None
        y = parameters.y().lower()
        if y == 'np':
            res = self.days_decomposition_raw(parameters)
        return self.fix_missing_x_groupings(res)
    def stacked_hours(self, parameters):
        res = None
        y = parameters.y().lower()
        if y == 'np':
            res = self.hours_decomposition_raw(parameters)
        return self.fix_missing_x_groupings(res)
    def stacked_moods(self, parameters):
        res = None
        y = parameters.y().lower()
        if y == 'np':
            res = self.moods_decomposition_raw(parameters)
        return self.fix_missing_x_groupings(res)
    def stacked_genders(self, parameters):
        res = None
        y = parameters.y().lower()
        if y == 'np':
            res = self.genders_decomposition_raw(parameters)
        return self.fix_missing_x_groupings(res)
    def stacked_ages(self, parameters):
        res = None
        y = parameters.y().lower()
        if y == 'np':
            res = self.ages_decomposition_raw(parameters)
        return self.fix_missing_x_groupings(res)
    def stacked_happys(self, parameters):
        res = None
        y = parameters.y().lower()
        if y == 'np':
            res = self.happys_decomposition_raw(parameters)
        return self.fix_missing_x_groupings(res)
    def stacked_surpriseds(self, parameters):
        res = None
        y = parameters.y().lower()
        if y == 'np':
            res = self.surpriseds_decomposition_raw(parameters)
        return self.fix_missing_x_groupings(res)
    def stacked_angrys(self, parameters):
        res = None
        y = parameters.y().lower()
        if y == 'np':
            res = self.angrys_decomposition_raw(parameters)
        return self.fix_missing_x_groupings(res)
    def stacked_afraids(self, parameters):
        res = None
        y = parameters.y().lower()
        if y == 'np':
            res = self.afraids_decomposition_raw(parameters)
        return self.fix_missing_x_groupings(res)
    def stacked_sads(self, parameters):
        res = None
        y = parameters.y().lower()
        if y == 'np':
            res = self.sads_decomposition_raw(parameters)
        return self.fix_missing_x_groupings(res)

    ###
    def cameras_decomposition_raw(self, parameters):
        grouping = self.define_grouping_for_x_axis(parameters)
        res = []
        for item in parameters.filter_cameras():
            counts = [[i, 0] for i in sorted(grouping)]
            count = Person.objects.person_count(parameters.x(), parameters)
            counts = util.add_stacked_counts(count, counts)
            layerRes = {'values': counts}
            key = item
            layerRes.update({'key': key})
            res.append(layerRes)
        return res
    def days_decomposition_raw(self, parameters):
        grouping = self.define_grouping_for_x_axis(parameters)
        res = []
        for item in parameters.filter_days():
            counts = [[i, 0] for i in sorted(grouping)]
            count = Person.objects.person_count(parameters.x(), parameters)
            counts = util.add_stacked_counts(count, counts)
            layerRes = {'values': counts}
            key = item
            layerRes.update({'key': key})
            res.append(layerRes)
        return res
    def hours_decomposition_raw(self, parameters):
        grouping = self.define_grouping_for_x_axis(parameters)
        res = []
        for item in parameters.filter_hours():
            counts = [[i, 0] for i in sorted(grouping)]
            count = Person.objects.person_count(parameters.x(), parameters)
            counts = util.add_stacked_counts(count, counts)
            layerRes = {'values': counts}
            key = item
            layerRes.update({'key': key})
            res.append(layerRes)
        return res
    def moods_decomposition_raw(self, parameters):
        grouping = self.define_grouping_for_x_axis(parameters)
        res = []
        for item in parameters.filter_moods():
            counts = [[i, 0] for i in sorted(grouping)]
            count = Person.objects.person_count(parameters.x(), parameters)
            counts = util.add_stacked_counts(count, counts)
            layerRes = {'values': counts}
            key = item
            layerRes.update({'key': key})
            res.append(layerRes)
        return res
    def genders_decomposition_raw(self, parameters):
        grouping = self.define_grouping_for_x_axis(parameters)
        res = []
        for item in parameters.filter_genders():
            counts = [[i, 0] for i in sorted(grouping)]
            count = Person.objects.person_count(parameters.x(), parameters)
            counts = util.add_stacked_counts(count, counts)
            layerRes = {'values': counts}
            key = item
            layerRes.update({'key': key})
            res.append(layerRes)
        return res
    def ages_decomposition_raw(self, parameters):
        grouping = self.define_grouping_for_x_axis(parameters)
        res = []
        for item in parameters.filter_ages():
            counts = [[i, 0] for i in sorted(grouping)]
            count = Person.objects.person_count(parameters.x(), parameters)
            counts = util.add_stacked_counts(count, counts)
            layerRes = {'values': counts}
            key = item
            layerRes.update({'key': key})
            res.append(layerRes)
        return res
    def happys_decomposition_raw(self, parameters):
        grouping = self.define_grouping_for_x_axis(parameters)
        res = []
        for item in parameters.filter_happys():
            counts = [[i, 0] for i in sorted(grouping)]
            count = Person.objects.person_count(parameters.x(), parameters)
            counts = util.add_stacked_counts(count, counts)
            layerRes = {'values': counts}
            key = item
            layerRes.update({'key': key})
            res.append(layerRes)
        return res
    def disgusteds_decomposition_raw(self, parameters):
        grouping = self.define_grouping_for_x_axis(parameters)
        res = []
        for item in parameters.filter_disgusteds():
            counts = [[i, 0] for i in sorted(grouping)]
            count = Person.objects.person_count(parameters.x(), parameters)
            counts = util.add_stacked_counts(count, counts)
            layerRes = {'values': counts}
            key = item
            layerRes.update({'key': key})
            res.append(layerRes)
        return res
    def angrys_decomposition_raw(self, parameters):
        grouping = self.define_grouping_for_x_axis(parameters)
        res = []
        for item in parameters.filter_angrys():
            counts = [[i, 0] for i in sorted(grouping)]
            count = Person.objects.person_count(parameters.x(), parameters)
            counts = util.add_stacked_counts(count, counts)
            layerRes = {'values': counts}
            key = item
            layerRes.update({'key': key})
            res.append(layerRes)
        return res
    def surpriseds_decomposition_raw(self, parameters):
        grouping = self.define_grouping_for_x_axis(parameters)
        res = []
        for item in parameters.filter_surpriseds():
            counts = [[i, 0] for i in sorted(grouping)]
            count = Person.objects.person_count(parameters.x(), parameters)
            counts = util.add_stacked_counts(count, counts)
            layerRes = {'values': counts}
            key = item
            layerRes.update({'key': key})
            rres.append(layerRes)
        return res
    def afraids_decomposition_raw(self, parameters):
        grouping = self.define_grouping_for_x_axis(parameters)
        res = []
        for item in parameters.filter_afraids():
            counts = [[i, 0] for i in sorted(grouping)]
            count = Person.objects.person_count(parameters.x(), parameters)
            counts = util.add_stacked_counts(count, counts)
            layerRes = {'values': counts}
            key = item
            layerRes.update({'key': key})
            rres.append(layerRes)
        return res
    def sads_decomposition_raw(self, parameters):
        grouping = self.define_grouping_for_x_axis(parameters)
        res = []
        for item in parameters.filter_sads():
            counts = [[i, 0] for i in sorted(grouping)]
            count = Person.objects.person_count(parameters.x(), parameters)
            counts = util.add_stacked_counts(count, counts)
            layerRes = {'values': counts}
            key = item
            layerRes.update({'key': key})
            rres.append(layerRes)
        return res

    def define_grouping_for_x_axis(self, parameters):
        grouping = None
        x = parameters.x().lower()
        if x == 'c':
            grouping = parameters.filter_cameras() or []
        elif x == 'd':
            grouping = parameters.filter_days() or range(4,7)
        elif x == 'h':
            grouping = parameters.filter_hours() or range(24)
        elif x == 'mood':
            grouping = parameters.filter_moods() or range(-100,100)
        elif x == 'gen':
            grouping = parameters.filter_genders() or range(-100,100)
        elif x == 'age':
            grouping = parameters.filter_ages() or range(0,100)
        elif x == 'hap':
            grouping = parameters.filter_happys() or range(0,100)
        elif x == 'dis':
            grouping = parameters.filter_disgusteds() or range(0,100)
        elif x == 'ang':
            grouping = parameters.filter_angrys() or range(0,100)
        elif x == 'sur':
            grouping = parameters.filter_surpriseds() or range(0,100)
        elif x == 'afr':
            grouping = parameters.filter_afraids() or range(0,100)
        elif x == 'sad':
            grouping = parameters.filter_sads() or range(0,100)
        return grouping

# !! EMMA: to check
    def fix_missing_x_groupings(self, res):
        # Find all x_groupings without duplicates
        x_grouping = []
        for r in res:
            x_grouping.extend(x[0] for x in r['values'])
        x_grouping = set(x_grouping)
        x_grouping_len = len(x_grouping)

        for dct in res:
            if len(dct['values']) != x_grouping_len:
                # Not all x_groupings are here.
                values = dict(dct['values'])
                values = [ (x_group, values.get(x_group, 0)) for x_group in x_grouping]
                dct['values'] = values
        return res
