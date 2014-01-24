README file for the CrowdSight-SDK OSX
==========================================

Requirements:

    * An Intel CPU based system
    * OSX 10.6.8 or higher
    * Command Line Tools for Xcode https://developer.apple.com/downloads
      or 
      Xcode http://itunes.apple.com/us/app/xcode/id497799835
      (If using Xcode enable command line tools in Preferences->Downloads menu)
    * Homebrew http://mxcl.github.com/homebrew/
    * CrowdSight installer version 2.2 for OSX (CrowdSight-SDK-OSX-2.2.bin)


Installation:

* Install all dependencies listed above 
* Open the Terminal app and type 'brew doctor' followed by enter. Follow on 
  screen instructions to fix any errors that appear.
* Install dependencies by entering the following command in the terminal: 
    
    cd /usr/local
    git checkout 2797501 /usr/local
    brew install ffmpeg gfortran tbb
    brew tap homebrew/science
    cd Library/Taps/homebrew-science
    git checkout ae74fe9
    brew install opencv --with-tbb --env=std

* Verify that all dependencies installed successfully
* Locate your CrowdSight-SDK-OSX-2.2.bin file through the terminal.
  Afterwards enter the following commands in the terminal:

   chmod +x CrowdSight-SDK-OSX-2.2.bin
   sudo ./CrowdSight-SDK-OSX-2.2.bin

* Verify that CrowdSight SDK installed successfully by checking the terminal output


Test installation:

* Compile the example application by entering the following command in Terminal:

   cd /usr/local/crowdsight/example
   make
   ./example

* The last command prints the required parameters of the example program:

Usage: ./example --file <videofile> <data dir> <resources dir> <auth key>
       ./example --capture <frame-id> <data dir> <resources dir> <auth key>
       ./example --stream <stream-url> <data dir> <resources dir> <auth key>

Using a video as input:
  <videofile>     A full path to a video file
  <data dir>      Default location is /usr/local/crowdsight/data/
  <resources dir> Default location is /usr/local/crowdsight/resources/
  <auth key>      Your crowdsight license key

Using a webcam as input:
  <frame-id>      ID of the webcam to be used, most of the time should be 0
  <data dir>      Default location is /usr/local/crowdsight/data/
  <resources dir> Default location is /usr/local/crowdsight/resources/
  <auth key>      Your crowdsight license key

Using a stream as input:
  <stream-url>    An asf stream url
  <data dir>      Default location is /usr/local/insight/data/
  <resources dir> Default location is /usr/local/insight/resources/
  <auth key>      Your insight license key

Example usages: 

    ./example --file testmovie.avi /usr/local/crowdsight/data/ /usr/local/crowdsight/resources/ mycrowdsightlicensekey
    ./example --capture 0 /usr/local/crowdsight/data/ /usr/local/crowdsight/resources/ mycrowdsightlicensekey
    ./example --stream http://[ipaddress]/videostream.asf?user=[USER]&pwd=[PASSWORD]&resolution=64&rate=0 /usr/local/insight/data/ /usr/local/insight/resources/ myinsightlicensekey


Troubleshooting:
    
    Problem excuting the example program:
    
    OpenCV Error: Unspecified error (Could not open the file storage. Check the path and permissions) in CvStatModel::save, file /tmp/brew-opencv-2.4.2-mqMO/OpenCV-2.4.2/modules/ml/src/inner_functions.cpp, line 71
    terminate called after throwing an instance of 'cv::Exception'
      what():  /tmp/brew-opencv-2.4.2-mqMO/OpenCV-2.4.2/modules/ml/src/inner_functions.cpp:71: error: (-2) Could not open the file storage. Check the path and permissions in function CvStatModel::save

    Solution:

    sudo chmod -R a+w /usr/local/crowdsight/data

Example Project Overview:
  The example project is split up in several files:
  * main          : mainly initializing necessary objects and parsing the command line arguments.
  * main_loop     : CrowdSight processing main loop. This class initializes and handles CrowdSight
					core operations. After CrowdSight initialization, MainLoop::run() grabs input
					frames, processes those and present the result of each frame analysis to the
					Visualization class, in the form of a vector of Person objects.
  * visualization : all drawing related functions are collected here. The function Visualization::drawPerson
					demonstrates how to retrieve the demographics of a single person and how to draw them
					to the frame.
	
Contact:

If you have any questions, please contact us at

support@sightcorp.com
