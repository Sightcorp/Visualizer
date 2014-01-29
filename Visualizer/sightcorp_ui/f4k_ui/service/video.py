import logging
import operator
from f4k_ui.parameters import VisualizationParameters

class VideoService:
    def __init__(self, species_names):
        self.species_names = species_names

    def process_request(self, request):
        parameters = VisualizationParameters(request, self.species_names)
        logging.info("Requesting Video - data: %s" % parameters)

        res = self.get_videos(parameters)
        v_counts = []
        for r in res:
            c_id = r[0]
            vids = r[1]
            tmp = [(v[0], v[1], [(self.species_names[s[0]], s[1]) for s in v[2]]) for v in vids]
            v_counts.append((c_id, tmp))

        logging.debug("Response Video - computed.")
        return {'video_list': v_counts}

    def get_videos(self, parameters):
        #get results for each camera
        videos = []
        for camera in parameters.computed_camera_tables():
            v, vid_fish = camera.objects.retrieve_videos(parameters, camera._meta.db_table)
            if not len(v):
                continue
                #count total fish and per species fish
            vid_fish_counts = []
            vid_fish.sort(key=operator.itemgetter(0))
            current_vid = vid_fish[0][0]
            sp_count = [(vid_fish[0][1], vid_fish[0][2])]
            total_count = vid_fish[0][2]
            if len(v) == 1:
                continue
            for vid in vid_fish[1:]:
                if not current_vid == vid[0]:
                    vid_fish_counts.append((v[current_vid], total_count, sp_count))
                    total_count = 0
                    sp_count = []
                    current_vid = vid[0]
                total_count += vid[2]
                sp_count.append((vid[1], vid[2]))
            vid_fish_counts.append((v[current_vid], total_count, sp_count))

            tmp = [(vv[0].split('/')[-1], vv) for vv in vid_fish_counts]
            tmp.sort(key=operator.itemgetter(0))
            v = [t[1] for t in tmp]

            key = camera._meta.db_table.split('_')[2]
            videos.append((key, v))
        return videos
