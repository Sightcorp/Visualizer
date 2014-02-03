from django.db import models, connection
import operator
import logging
from django_ui import settings

######################################################

class PersonManager(models.Manager):
    def get_person(self):
        rows = self.all()
        return rows

    def person_count(self, groupby, parameters, zname=None, templayer=None):
        groupby = groupby.lower()
        cameras = parameters.filter_cameras()
        if zname=='c':
            cameras = [templayer]
        days = parameters.filter_days()
        if zname=='d':
            days = [templayer]
        hours = parameters.filter_hours()
        if zname=='h':
            hours = [templayer]
        moods = parameters.filter_moods()
        if zname=='mood':
            moods = [templayer]
        genders = parameters.filter_genders()
        if zname=='gen':
            genders = [templayer]
        ages = parameters.filter_ages()
        if zname=='age':
            ages = [templayer]
        happys = parameters.filter_happys()
        if zname=='hap':
            happys = [templayer]
        disgusteds = parameters.filter_disgusteds()
        if zname=='dis':
            disgusteds = [templayer]
        angrys = parameters.filter_angrys()
        if zname=='ang':
            angrys = [templayer]
        surpriseds = parameters.filter_surpriseds()
        if zname=='sur':
            surpriseds = [templayer]
        afraids = parameters.filter_afraids()
        if zname=='afr':
            afraids = [templayer]
        sads = parameters.filter_sads()
        if zname=='sad':
            sads = [templayer]

        where = []

        if not (cameras == [] or groupby == 'c'):
            where.append('id_source in (%s)' % ','.join(["'%s'" % s for s in cameras]))
        if not (days == [] or groupby == 'd'):
            where.append('day(start) in (%s)' % ','.join(["'%s'" % d for d in days]))
        if not (hours == [] or groupby == 'h'):
            where.append('hour(start) in (%s)' % ','.join(["'%s'" % h for h in hours]))  

        if not (moods == [] or groupby == 'mood' or groupby == 'mood_filter'):
            testmood = '(mood_av between '
            for m in moods:
                if len(testmood) != 17:
                    testmood = testmood + ' or mood_av between '
                testmood = testmood + str(m)
                testmood = testmood + ' and '
                testmood = testmood + str(m+9.9999999999)
            testmood = testmood + ')'
            where.append(testmood) 

        if not (genders == [] or groupby == 'gen' or groupby == 'gen_filter'):
            testmood = '(gender_av between '
            for m in genders:
                if len(testmood) != 19:
                    testmood = testmood + ' or gender_av between '
                testmood = testmood + str(m)
                testmood = testmood + ' and '
                testmood = testmood + str(m+9.9999999999)
            testmood = testmood + ')'
            where.append(testmood) 

        if not (ages == [] or groupby == 'age' or groupby == 'age_filter'):
            testmood = '(age_av between '
            for m in ages:
                if len(testmood) != 16:
                    testmood = testmood + ' or age_av between '
                testmood = testmood + str(m)
                testmood = testmood + ' and '
                testmood = testmood + str(m+9.9999999999)
            testmood = testmood + ')'
            where.append(testmood)

        if not (happys == [] or groupby == 'hap' or groupby == 'hap_filter'):
            testmood = '(happy_av between '
            for m in happys:
                if len(testmood) != 18:
                    testmood = testmood + ' or happy_av between '
                testmood = testmood + str(m)
                testmood = testmood + ' and '
                testmood = testmood + str(m+9.9999999999)
            testmood = testmood + ')'
            where.append(testmood)

        if not (disgusteds == [] or groupby == 'dis' or groupby == 'dis_filter'):
            testmood = '(disgusted_av between '
            for m in disgusteds:
                if len(testmood) != 22:
                    testmood = testmood + ' or disgusted_av between '
                testmood = testmood + str(m)
                testmood = testmood + ' and '
                testmood = testmood + str(m+9.9999999999)
            testmood = testmood + ')'
            where.append(testmood)

        if not (angrys == [] or groupby == 'ang' or groupby == 'ang_filter'):
            testmood = '(angry_av between '
            for m in angrys:
                if len(testmood) != 18:
                    testmood = testmood + ' or angry_av between '
                testmood = testmood + str(m)
                testmood = testmood + ' and '
                testmood = testmood + str(m+9.9999999999)
            testmood = testmood + ')'
            where.append(testmood)

        if not (surpriseds == [] or groupby == 'sur' or groupby == 'sur_filter'):
            testmood = '(surprised_av between '
            for m in surpriseds:
                if len(testmood) != 22:
                    testmood = testmood + ' or surprised_av between '
                testmood = testmood + str(m)
                testmood = testmood + ' and '
                testmood = testmood + str(m+9.9999999999)
            testmood = testmood + ')'
            where.append(testmood)

        if not (afraids == [] or groupby == 'afr' or groupby == 'afr_filter'):
            testmood = '(afraid_av between '
            for m in afraids:
                if len(testmood) != 19:
                    testmood = testmood + ' or afraid_av between '
                testmood = testmood + str(m)
                testmood = testmood + ' and '
                testmood = testmood + str(m+9.9999999999)
            testmood = testmood + ')'
            where.append(testmood)

        if not (sads == [] or groupby == 'sad' or groupby == 'sad_filter'):
            testmood = '(sad_av between '
            for m in sads:
                if len(testmood) != 16:
                    testmood = testmood + ' or sad_av between '
                testmood = testmood + str(m)
                testmood = testmood + ' and '
                testmood = testmood + str(m+9.9999999999)
            testmood = testmood + ')'
            where.append(testmood)

        if not where:
            where = ''
        else:
            where = 'where %s' % (' AND '.join(where))

        outer_unit = ''
        inner_unit = ''
        
        if groupby == 'c':
            inner_unit = 'id_source as source'
            outer_unit = 'source'
        elif groupby == 'd':
            inner_unit = 'day(start) as day'
            outer_unit = 'day'
        elif groupby == 'h':
            inner_unit = 'hour(start) as hour'
            outer_unit = 'hour'

        elif groupby == 'mood':
            inner_unit = 'cast(round((mood_av), 0) as SIGNED) as mood'
            outer_unit = 'mood'
        elif groupby == 'mood_filter':
            inner_unit = 'cast(round(mood_av/10, 0)*10 as SIGNED) as mood'
            outer_unit = 'mood'

        elif groupby == 'gen':
            inner_unit = 'cast(round((gender_av), 0) as SIGNED) as gender'
            outer_unit = 'gender'
        elif groupby == 'gen_filter':
            inner_unit = 'cast(round(gender_av/10, 0)*10 as SIGNED) as gender'
            outer_unit = 'gender'

        elif groupby == 'age':
            inner_unit = 'cast(round((age_av), 0) as SIGNED) as age'
            outer_unit = 'age'
        elif groupby == 'age_filter':
            inner_unit = 'cast(round(age_av/10, 0)*10 as SIGNED) as age'
            outer_unit = 'age'

        elif groupby == 'hap':
            inner_unit = 'cast(round((happy_av), 0) as SIGNED) as happy'
            outer_unit = 'happy'
        elif groupby == 'hap_filter':
            inner_unit = 'cast(round((happy_av/10), 0)*10 as SIGNED) as happy'
            outer_unit = 'happy'

        elif groupby == 'dis':
            inner_unit = 'cast(round((disgusted_av), 0) as SIGNED) as disgusted'
            outer_unit = 'disgusted'
        elif groupby == 'dis_filter':
            inner_unit = 'cast(round((disgusted_av/10), 0)*10 as SIGNED) as disgusted'
            outer_unit = 'disgusted'

        elif groupby == 'ang':
            inner_unit = 'cast(round((angry_av), 0) as SIGNED) as angry'
            outer_unit = 'angry'
        elif groupby == 'ang_filter':
            inner_unit = 'cast(round((angry_av/10), 0)*10 as SIGNED) as angry'
            outer_unit = 'angry'

        elif groupby == 'sur':
            inner_unit = 'cast(round((surprised_av), 0) as SIGNED) as surprised'
            outer_unit = 'surprised'
        elif groupby == 'sur_filter':
            inner_unit = 'cast(round((surprised_av/10), 0)*10 as SIGNED) as surprised'
            outer_unit = 'surprised'

        elif groupby == 'afr':
            inner_unit = 'cast(round((afraid_av), 0) as SIGNED) as afraid'
            outer_unit = 'afraid'
        elif groupby == 'afr_filter':
            inner_unit = 'cast(round((afraid_av/10), 0)*10 as SIGNED) as afraid'
            outer_unit = 'afraid'

        elif groupby == 'sad':
            inner_unit = 'cast(round((sad_av), 0) as SIGNED) as sad'
            outer_unit = 'sad'
        elif groupby == 'sad_filter':
            inner_unit = 'cast(round((sad_av/10), 0)*10 as SIGNED) as sad'
            outer_unit = 'sad'


        if inner_unit and outer_unit:
            qry = 'SELECT {inner_unit}, COUNT(id_person) FROM CSVisualizer.database_person {where} GROUP BY {outer_unit} ORDER BY {outer_unit}'\
                  ''.format(
                inner_unit=inner_unit,
                #tblname=tblname,
                where=where,
                outer_unit=outer_unit
            )
            print(qry)
        else:
            qry = 'SELECT COUNT(id_person) FROM CSVisualizer.database_person {where}'.format(where=where)


        cursor = connection.cursor()
        cursor.execute(qry)
        res = cursor.fetchall()
        if groupby in ['d', 'h', 'c', 'mood', 'mood_filter', 'gen', 'gen_filter', 'age', 'age_filter', 'hap', 'hap_filter', 'dis', 'dis_filter', 'ang', 'ang_filter', 'sur', 'sur_filter', 'afr', 'afr_filter', 'sad', 'sad_filter']:
            res = [[r[0], r[1]] for r in res]
        else:
            res = [[str(r[0]), r[1]] for r in res]
            res.sort(key=operator.itemgetter(0))
        #else:
        #    res = res[0]

        if settings.QUERY_RESULT_ENABLED:
            logging.info('[PersonManager] person_count results: ' + str(res))

        return res

class SourceManager(models.Manager):
    def get_source(self):
        q = self.all() #.order_by('person_id')
        res = [[s.id_source, s.label] for s in source]
        return res