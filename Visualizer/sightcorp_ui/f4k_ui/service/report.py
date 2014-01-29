from collections import namedtuple
import csv
import logging
import random
from django.http import HttpResponse, HttpResponseRedirect
from django_ui import settings
from f4k_ui.parameters import ReportParameters

Chart = namedtuple('Chart', ['id', 'parameters', 'name', 'description'])

class Report(namedtuple('Report', ['title', 'charts'])):

    def getChart(self, chartId):
        for c in self.charts:
            if c.id == chartId:
                return c
        return None

    def addChart(self, chart):
        toSave = True
        for c in self.charts:
            if c.parameters == chart.parameters:
                toSave = False
        if toSave:
            self.charts.append(chart)
        return toSave

    def removeChart(self, chartId):
        for c in self.charts:
            if c.id == chartId:
                self.charts.remove(c)
                return c
        return None

    def __str__(self):
        return 'Report: title=%s charts=%s' % (self.title, self.charts)

    def toJson(self):
        return {
            'title': self.title,
            'charts': [{
                'id': c.id,
                'parameters': c.parameters,
                'name': c.name,
                'description': c.description
            } for c in self.charts ]
        }

class ReportService:
    __reports = {}

    def __init__(self):
        pass

    def process_request(self, request):
        p = ReportParameters(request)
        logging.info("Requesting Report - data: %s" % p)

        response = {}
        user = request.user.username
        if p.cmd() == 'save':
            saved = self.save(user, p.parameters())
            response.update({'duplicate': not saved})
        elif p.cmd() == 'remove':
            r = self.remove(user, p.id())
            response.update({'removed': r is not None})
        elif p.cmd() == 'update-report':
            u = self.updateReport(user, p.title())
            response.update({'updated': u})
        elif p.cmd() == 'update-chart':
            u = self.updateChart(user, p.id(), p.name(), p.description())
            response.update({'updated': u})
        else:
            user_report = self.safeGetUserReport(user)
            response.update({'report': user_report.toJson()})

        return response

    def safeGetUserReport(self, user):
        if user not in self.__reports:
            ur = Report('', [])
            self.__reports[user] = ur
        else:
            ur = self.__reports[user]
        return ur

    def nextChartId(self):
        return random.randint(1, 1000000)

    def save(self, user, parameters):
        ur = self.safeGetUserReport(user)
        added = ur.addChart(Chart(self.nextChartId(), parameters, '', ''))
        logging.info("Added: %s, Current user reports: %s" % (added, str(ur)))
        return added

    def get(self, user):
        return self.safeGetUserReport(user)

    def remove(self, user, chartId):
        ur = self.safeGetUserReport(user)
        return ur.removeChart(chartId)

    def updateReport(self, user, title):
        ur = self.safeGetUserReport(user)
        self.__reports[user] = Report(title, ur.charts)
        return True

    def updateChart(self, user, chartId, name, description):
        ur = self.safeGetUserReport(user)
        c = ur.removeChart(chartId)
        return ur.addChart(Chart(c.id, c.parameters, name, description))

    def csv(self, request):
        user = request.user.username
        if request.method == 'POST':
            file = request.FILES['report']
            for row in csv.reader(file.read().splitlines()):
                ur = self.safeGetUserReport(user)
                ur.addChart(Chart(self.nextChartId(), row[0], row[1], row[2]))

            response = HttpResponseRedirect('%s%s' % (settings.HOME_ROOT, 'ui/report/'))
        else:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="report.csv"'

            writer = csv.writer(response)

            for chart in self.safeGetUserReport(user).charts:
                writer.writerow([chart.parameters, chart.name, chart.description])

        return response