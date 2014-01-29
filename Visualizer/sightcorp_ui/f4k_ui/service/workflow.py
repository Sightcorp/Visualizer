from datetime import datetime
import logging
import re
from django.core.exceptions import ObjectDoesNotExist
#from f4k_ui.db.models import UserQuery
#from f4k_ui.parameters import WorkflowParameters

class WorkflowService:
    def __init__(self, cameras_list):
        self.cameras_location_video_list = cameras_list
        self.abort_pattern = re.compile("abort_query\((\d+)\)")

    def process_request(self, request):
        p = WorkflowParameters(request)
        logging.info("Requesting Workflow - data: %s" % p)

        response = {}
        if p.cmd() == 'add':
            analysis_query_id = self.add_user_query(p)
            if analysis_query_id:
                response.update({'added': True})
                response.update({'id': analysis_query_id})
                response.update(self.list_user_queries())
            else:
                response.update({'duplicate': True})
        elif p.cmd() == 'abort':
            self.abort_user_query(p)
            response.update({'aborted': True})
            response.update(self.list_user_queries())
        elif p.cmd() == 'estimate':
            estimation_query_id = self.add_user_query(p)
            if estimation_query_id:
                response.update({'added': True})
                response.update({'id': estimation_query_id})
            else:
                response.update({'duplicate': True})
        elif p.cmd() == 'estimate_result':
            estimationQueryId = p.id()
            response.update({'result': self.estimation_result(estimationQueryId)})
        else:
            response.update(self.list_user_queries())

        return response

    def add_user_query(self, p):
        query = p.query()
        component_detection = p.detection()
        component_recognition = p.recognition()

        formatted_cameras = ''
        for i, camera in enumerate(p.filter_cameras()):
            for clv in self.cameras_location_video_list:
                if clv[0] == camera:
                    formatted_cameras += '%s/%s' % (clv[1], clv[2])
                    if not i == len(p.filter_cameras()) - 1:
                        formatted_cameras += ','

        start = datetime.strptime(p.start(), '%d-%m-%Y').date()
        end = datetime.strptime(p.end(), '%d-%m-%Y').date()

        query_id = None
        args = (query, formatted_cameras, component_detection,component_recognition, start, end)
        if not UserQuery.objects.exists(*args):
            obj = UserQuery.objects.create(
                query_content=query,
                video_location_videoNumber=formatted_cameras,
                component_id_detection=component_detection,
                component_id_recognition=component_recognition,
                data_start_date=start,
                data_end_date=end)
            query_id = obj.query_id_by_wf
        return query_id

    def abort_user_query(self, p):
        queryId = p.id()
        UserQuery.objects.create(
            query_content='abort_query(%s)' % queryId,
        )

    def list_user_queries(self):
        userQueries = UserQuery.objects.get_cwi_queries()
        currentQueries = []
        for q in self.filter_aborted_queries(self.filter_estimation_queries(userQueries)):
            currentQueries.append({
                'id': q.query_id_by_wf,
                'status': q.query_overall_status,
                'time_left': q.time_to_completion,
                'detection': q.component_id_detection,
                'recognition': q.component_id_recognition,
                'completed': q.query_percentage_successful
            })
        return {'queries': currentQueries}

    def filter_aborted_queries(self, queries):
        # it will contain the id of the aborting queries and the queries they refer to
        list_abort_queries = []
        for q in queries:
            m = self.abort_pattern.match(q.query_content)
            if m is not None:
                list_abort_queries.append(q.query_id_by_wf)
                list_abort_queries.append(int(m.group(1)))

        return [q for q in queries if q.query_id_by_wf not in list_abort_queries]

    def filter_estimation_queries(self, queries):
        return [q for q in queries if 'estimation' not in q.query_content]

    def estimation_result(self, queryId):
        res = -1
        try:
            #  The result will be stored in 'time_to_completion' (in seconds) and the 'query_overall_status' will be 'completed'.
            q = UserQuery.objects.get(query_id_by_wf=queryId)
            if q.query_overall_status == 'completed':
                res = q.time_to_completion
        except ObjectDoesNotExist:
            pass
        return res