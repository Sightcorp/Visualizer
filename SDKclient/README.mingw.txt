README file for the CrowdSight-SDK example for QT Creator
=========================================================

These instructions are for mingw32 build of CrowdSight:

QuickStart:

* Download and install the latest version of QTSDK (mingw32).
* Download and install http://sourceforge.net/projects/mingw/files/Installer/mingw-get-inst/mingw-get-inst-20120426/mingw-get-inst-20120426.exe 
  Do NOT select 'download latest repository catalogues' option when installing.
* Copy the contents of your mingw installation (default C:\MinGW) into your Qt mingw folder (default C:\QtSDK\mingw)
* Run Qt Creator as administrator
* Open the example.pro file in Qt Creator.
* In the 'Target Setup' dialogue, select 'For One Qt Version One Debug And One Release'
* In the 'Qt Version' menu make sure to select MinGW Qt SDK and press Finish
* In 'Project -> Run settings' specify the command line        
  arguments according to following syntax:

    <videofile> <data dir> <resources dir> <auth key>
  
  or for webcam input:

    --capture <frame-id> <data dir> <resources dir> <auth key>

* Compile and run the example using the play button

Command line arguments specification:

  Using a video as input:
  <videofile>     A video file
  <data dir>      Default location is ../data/
  <resources dir> Default location is ../resources/
  <auth key>      Your crowdsight license key, create one at http://licensing.sightcorp.com

  Using a webcam as input:
  <frame-id>      ID of the webcam to be used, most of the time this is zero
  <data dir>      Default location is ../data/
  <resources dir> Default location is ../resources/
  <auth key>      Your crowdsight license key, create one at http://licensing.sightcorp.com

   Example arguments: 

   testmovie.avi ../data/ ../resources/ mycrowdsightlicensekey
   --capture 0 ../data/ ../resources/ mycrowdsightlicensekey

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

Support email:

If you have any questions, please contact us at

support@sightcorp.com
