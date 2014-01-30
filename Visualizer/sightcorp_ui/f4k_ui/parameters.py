# Camera mngt heritated from teh 1st demo. It's rather useless here, it's just a quick hack
#from f4k_ui.db.models import dict_all_camera_table

class Parameters:
    _p = None

    def _parseSingleValue(self, method, name, default):
        if name in method:
            value = method.get(name).strip()
            if value != '':
                return value
        return default

    def _parseArray(self, method, name, defaults):
        values = defaults
        if name in method:
            values = method.get(name).strip().split(',')
        elif name + '[]' in method:
            values = method.getlist(name + '[]')

        if 'all' in values:
            values = []

        # removes duplicates
        seen = set()
        seen_add = seen.add
        return [x for x in values if x not in seen and not seen_add(x)]

    def status(self):
        return {'parameters': self._p}

    def __repr__(self):
        return str(self._p)


class VisualizationParameters(Parameters):
    def __init__(self, request, species_names):
        method = request.GET
        if request.method == 'POST':
            method = request.POST

        self._species_names = species_names
        self._p = self._parseParameters(method)

    def _parseParameters(self, method):
        chart_type = self._parseSingleValue(method, 't', 'S')

        axis_x = self._parseSingleValue(method, 'x', 'D')
        axis_y = self._parseSingleValue(method, 'y', 'NP')
        axis_z = self._parseSingleValue(method, 'z', '')

        f = self._parseArray(method, 'f', ['f_c'])
        f_c = [int(i) for i in self._parseArray(method, 'f_c', [])]
        f_d = [int(i) for i in self._parseArray(method, 'f_d', [])]
        f_h = [int(i) for i in self._parseArray(method, 'f_h', [])]
        f_mood = [int(i) for i in self._parseArray(method, 'f_mood', [])]
        f_gender = [int(i) for i in self._parseArray(method, 'f_gen', [])]
        f_age = [int(i) for i in self._parseArray(method, 'f_age', [])]
        f_happy = [int(i) for i in self._parseArray(method, 'f_hap', [])]
        f_disgusted = [int(i) for i in self._parseArray(method, 'f_dis', [])]
        f_angry = [int(i) for i in self._parseArray(method, 'f_ang', [])]
        f_surprised = [int(i) for i in self._parseArray(method, 'f_sur', [])]
        f_afraid = [int(i) for i in self._parseArray(method, 'f_afr', [])]
        f_sad = [int(i) for i in self._parseArray(method, 'f_sad', [])]

        return {'x': axis_x, 'y': axis_y, 'z': axis_z, 't': chart_type, 'f': f, 'f_c': f_c, 'f_d': f_d, 'f_h': f_h, 'f_mood': f_mood, 'f_gen': f_gender, 'f_age': f_age, 'f_hap': f_happy, 'f_dis': f_disgusted, 'f_ang': f_angry, 'f_sur': f_surprised, 'f_afr': f_afraid, 'f_sad': f_sad}

    def x(self):
        return self._p['x']

    def y(self):
        return self._p['y']

    def z(self):
        return self._p['z']

    def t(self):
        return self._p['t']

    def opened_filters(self):
        return self._p['f']

    def filter_cameras(self):
        return self._p['f_c']
    def filter_days(self):
        return self._p['f_d']
    def filter_hours(self):
        return self._p['f_h']
    def filter_moods(self):
        return self._p['f_mood']
    def filter_genders(self):
        return self._p['f_gen']
    def filter_ages(self):
        return self._p['f_age']
    def filter_happys(self):
        return self._p['f_hap']
    def filter_disgusteds(self):
        return self._p['f_dis']
    def filter_angrys(self):
        return self._p['f_ang']
    def filter_surpriseds(self):
        return self._p['f_sur']
    def filter_afraids(self):
        return self._p['f_afr']
    def filter_sads(self):
        return self._p['f_sad']

############################
class WorkflowParameters(Parameters):
    def __init__(self, request):
        method = request.GET
        if request.method == 'POST':
            method = request.POST

        self._p = self._parseParameters(method)

    def _parseParameters(self, method):
        cmd = self._parseSingleValue(method, 'cmd', '')
        query = self._parseSingleValue(method, 'q', '')
        id = self._parseSingleValue(method, 'id', '')

        detection = self._parseSingleValue(method, 'detection', 0)
        recognition = self._parseSingleValue(method, 'recognition', 0)

        start = self._parseSingleValue(method, 'start', '')
        end = self._parseSingleValue(method, 'end', '')
        f_c = [int(i) for i in self._parseArray(method, 'f_c', [1])]

        return {'cmd': cmd, 'q': query, 'id': id, 'det': detection, 'rec': recognition, 'start': start, 'end': end, 'f_c': f_c}

    def cmd(self):
        return self._p['cmd']

    def query(self):
        return self._p['q']

    def id(self):
        return self._p['id']

    def detection(self):
        return self._p['det']

    def recognition(self):
        return self._p['rec']

    def start(self):
        return self._p['start']

    def end(self):
        return self._p['end']

    def filter_cameras(self):
        return self._p['f_c']

class ReportParameters(Parameters):
    def __init__(self, request):
        method = request.GET
        if request.method == 'POST':
            method = request.POST

        self._p = self._parseParameters(method)

    def _parseParameters(self, method):
        cmd = self._parseSingleValue(method, 'cmd', '')
        parameters = self._parseSingleValue(method, 'parameters', '')
        id = int(self._parseSingleValue(method, 'id', -1))
        title = self._parseSingleValue(method, 'title', '')
        name = self._parseSingleValue(method, 'name', '')
        description = self._parseSingleValue(method, 'description', '')

        return {'cmd': cmd, 'p': parameters, 'id': id, 'title': title, 'name': name, 'description': description}

    def cmd(self):
        return self._p['cmd']

    def parameters(self):
        return self._p['p']

    def id(self):
        return self._p['id']

    def title(self):
        return self._p['title']

    def description(self):
        return self._p['description']

    def name(self):
        return self._p['name']