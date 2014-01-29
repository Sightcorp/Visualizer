VideoController = function () {
    var video_site_old = 'http://140.110.134.241//history/KenTing/Video_';
    var video_site_new1 = 'http://140.110.134.240//history/KenTing/Video_';
    var video_site_new2 = 'http://140.110.134.242//history/KenTing/Video_';
    var video_data_map = {};

    refresh();

    this.refreshZoneB = function () {
        refresh();
    };

    function refresh() {
        $.ajax({type:"GET", url:video_data_url, data:parameters}).done(renderVideos);
    }

    function renderVideos(response) {
        $.each(response, function (key, value) {
            list_video(key, value);
        });
    }

    //data are lists with (camera_id, data)
    //when loading the list, the default video is the first one in the list
    function load_video(video_url, sp_counts) {
        embed = [];
        embed.push('<embed id="embed_vid" width="300" height="250"');
        embed.push('allowfullscreen="false" allowscriptaccess="always"');
        embed.push('scale="ShowAll" quality="High" wmode="Opaque" manu="true" loop="true" play="true"');
        embed.push('flashvars="f=' + video_url + '&amp;startPlayingOnload=yes"');
        embed.push('src="http://ecocam.nchc.org.tw/_MonitorGrid_/SWF/wasp.swf"');
        embed.push('movie="http://ecocam.nchc.org.tw/_MonitorGrid_/SWF/wasp.swf"');
        embed.push('http://ecocam.nchc.org.tw/_MonitorGrid_/SWF/wasp.swf');
        embed.push('pluginspage="http://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash');
        embed.push('type="application/x-shockwave-flash">');
        document.getElementById('video_clip').innerHTML = embed.join(' ');
        //species counts
        var sp = ['<h3>Species counts in current video</h3>'];
        sp.push(sp_counts);
        document.getElementById('video_fish_counts').innerHTML = sp.join(' ');

    }

    this.showVid = function(url) {
        var tmp = url.split('##');
        var vid_id = tmp[0];
        var sp_counts = tmp[1];
        load_video(vid_id, sp_counts);
        document.getElementById("video_play_title").innerHTML = get_video_title(vid_id);
    };

    //store the retrieved video list as global variable
    //get the urls
    //data {camera_id: [vid, tot_count, [(sp, sp_count)..]]}
    function process_video_list(data) {
        video_data_map = {};
        for (var i = 0; i < data.length; i++) {
            var camera_id = data[i][0];
            var videos = data[i][1];
            var video_urls = [];
            for (var j = 0; j < videos.length; j++) {
                var vid_url = get_video_url(videos[j][0]);
                video_urls.push([vid_url, videos[j][1], videos[j][2]]);
            }
            video_data_map[camera_id] = video_urls;
        }
    }

    function get_video_title(vid_url) {
        //console.log(vid_url);
        var tmp = vid_url.split('/');
        var video_name = tmp[tmp.length - 1];
        tmp = video_name.split('_')[1].replace('.flv', '').split('-');
        return tmp[0] + '-' + tmp[1] + '-' + tmp[2] + ' ' + tmp[3] + ':' + tmp[4];
    }

    function get_video_url(filename) {
        var tmp = filename.split('/');
        var video_name = tmp[tmp.length - 1];

        var video_title = 'Video: ' + filename.replace('/var/www/EcoData/', '');
        var path = video_name.split('_')[1].replace(/-/g, '/').replace('.flv', '/');
        var letter = filename.split('Site_')[1].split('/')[0];

        var video_url = '';
        //console.log(filename);
        //console.log('OLD'.indexOf(filename));
        if (filename.indexOf('OLD') != -1) {
            video_url = video_site_old + letter + '/' + path + video_name;
        }
        else if (filename.indexOf('NEW.1') != -1) {
            video_url = video_site_new1 + letter + '/' + path + video_name;
        }
        else if (filename.indexOf('NEW.2') != -1) {
            video_url = video_site_new2 + letter + '/' + path + video_name;
        }
        //console.log(video_url);
        return video_url;
    }

    //click on "more" to show more videos
    this.showMore = function(id) {
        var current_content = document.getElementById(id).innerHTML;
        var camera_id = id.split('_')[1];
        var videos = video_data_map[camera_id];
        var content = '';
        if (current_content == 'Show less') {
            content = 'Show more';
            extra_vids = []
        }
        else if (current_content == 'Show more') {
            content = 'Show less';
            var extra_vids = [];
            for (var i = 5; i < videos.length; i++) {
                var item = get_video_title(videos[i][0]);
                var sp_counts = videos[i][2];
                var tmp = [];
                for (var x = 0; x < sp_counts.length; x++)
                    tmp.push(sp_counts[x][0] + ' (' + sp_counts[x][1] + ')<br/>');
                sp_counts = tmp.join('');
                var vid_id = videos[i][0] + '##' + sp_counts;

                extra_vids.push('<div class="vid_item" id="' + vid_id + '" onclick="zoneBcontroller.showVid(id)" >' + item + '(' + videos[i][1] + ' fish)</div>');
                //	extra_vids.push(videos[i][0]);
                //	extra_vids.push('" onclick=showVid(id, sp_counts)>');
                //	extra_vids.push(item+' ('+videos[i][1]+' fish)');
                //	extra_vids.push('</div>');
            }
        }
        document.getElementById(id).innerHTML = content;
        document.getElementById('extra_' + camera_id).innerHTML = extra_vids.join('');
    };

    //when loading the page, list the videos
    function list_video(div_id, data) {
        process_video_list(data);
        var content = [];
        var default_video = '';
        var default_video_url = '';
        var default_sp_counts = [];
        $.each(video_data_map, function (camera_id, videos) {
            var header = '<h3> Camera' + camera_id + ' (' + videos.length + ' videos)' + '</h3>';
            content.push(header);
            for (var j = 0; j < videos.length; j++) {
                if (default_video == '') {
                    default_video_url = videos[j][0];
                    default_video = get_video_title(default_video_url);
                    var sp_counts = videos[j][2];
                    tmp = [];
                    for (var x = 0; x < sp_counts.length; x++)
                        tmp.push(sp_counts[x][0] + ' (' + sp_counts[x][1] + ')<br/>');
                    default_sp_counts = tmp.join('');
                }
                if (j < 5) {
                    item = get_video_title(videos[j][0]);
                    counts = videos[j][1];
                    var sp_counts = videos[j][2];
                    //console.log(sp_counts);
                    tmp = [];
                    for (var x = 0; x < sp_counts.length; x++)
                        tmp.push(sp_counts[x][0] + ' (' + sp_counts[x][1] + ')<br/>');
                    sp_counts = tmp.join('');

                    var vid_id = videos[j][0] + '##' + sp_counts;

                    content.push('<div class="vid_item" id="' + vid_id + '" onclick="zoneBcontroller.showVid(id)" >');
                    content.push(item + ' (' + counts + ' fish)');
                    content.push('</div>');
                }
            }
            if (videos.length > 5) {
                content.push('<br/><div class="vid_item" id="more_' + camera_id + '" onclick=zoneBcontroller.showMore(id)>Show more</div><br/>');
                content.push('<div id="extra_' + camera_id + '" ></div>');
            }
        });
        document.getElementById(div_id).innerHTML = content.join(' ');
        //set the video title by default the first one
        document.getElementById("video_play_title").innerHTML = default_video;
        //set the video
        load_video(default_video_url, default_sp_counts);
    }

};