README file for the CrowdSight-SDK example for Visual Studio
============================================================

These instructions are for vs2010 build of CrowdSight:

Installation:

* Install the CrowdSight SDK
* Download and install Visual Studio 2010 C++ Express edition
* Run Visual Studio C++ Express as administrator
* Open the example.sln file in Visual Studio
* Right click the project and select 'Properties'
* In the 'General->Debugging' settings, fill in command line 
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
  <auth key>      Your crowdsight license key

  Using a webcam as input:
  <frame-id>      ID of the webcam to be used, most of the time this is 0 
  <data dir>      Default location is ../data/
  <resources dir> Default location is ../resources/
  <auth key>      Your crowdsight license key

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
