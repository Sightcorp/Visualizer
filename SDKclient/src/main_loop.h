//
//  main_loop.h
//
//  MainLoop of the SDK
//
//  Created on 11/12/13.
//  Copyright (c) 2013 Sightcorp. All rights reserved.
//

#ifndef _MAIN_LOOP_H_
#define _MAIN_LOOP_H_

#include <string>

#include <opencv2/opencv.hpp>

#include "visualization.h"
#include "client.h"

class CrowdSight;

enum InputSource
{
  WEBCAM,
  VIDEO_FILE,
  VIDEO_STREAM
};

struct CaptureResolution
{
  CaptureResolution( int w, int h ) : width( w ), height( h ) {}

  int width;
  int height;
};

struct MainLoopArguments
{
  // Default arguments
  MainLoopArguments()
    : authenticationKey( "enter_license_key" ),
      captureDevice( 0 ),
      captureInput( "" ),
      dataDirPath( "./data/" ),
      resourceDirPath( "./resources/" ),
      source( WEBCAM ),
      captureResolution( 640, 480 ),
      cameraName( "Cam001" ) {}

  std::string authenticationKey;
  int captureDevice;
  std::string captureInput;
  std::string dataDirPath;
  std::string resourceDirPath;
  InputSource source;
  CaptureResolution captureResolution;
  std::string cameraName;
};


class MainLoop
{
public:
  MainLoop();
  MainLoop( MainLoopArguments args );
  ~MainLoop();

  int run();

private:
  void init();
  bool grabFrame();
  void setFrame( cv::Mat & frame );

  MainLoopArguments mArgs;
  CrowdSight * mCrowdSight;
  Client     * mClient;
  cv::VideoCapture mCap;
  cv::Mat mFrame;
  Visualization * mVisualization;
};

#endif // _MAIN_LOOP_H_
