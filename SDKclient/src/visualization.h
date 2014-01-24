//
//  visualization.h
//
//  Visualization of a person processed by the SDK
//
//  Created on 11/12/13.
//  Copyright (c) 2013 Sightcorp. All rights reserved.
//

#ifndef _VISUALIZATION_H_
#define _VISUALIZATION_H_

#include <string>

#include <opencv2/opencv.hpp>

class CrowdSight;

class Person;

struct ScreenResolution
{
  ScreenResolution( int w, int h ) : width( w ), height( h ) {}

  int width;
  int height;
};

struct VisualizationArguments
{
  // Default arguments
  VisualizationArguments()
    : resourceDirPath( "./resources/demo_dashboard.png" ),
      mainWindowName( "DEMO" ),
      waitKeyDelay( 1 ),
      screenResolution( 1920, 1080 ) {}

  std::string resourceDirPath;
  std::string mainWindowName;
  int waitKeyDelay;
  ScreenResolution screenResolution;
};


class Visualization
{
public:
  Visualization();
  Visualization( VisualizationArguments args );
  ~Visualization() {}

  int draw( CrowdSight *  crowdsight, Person * person, cv::Mat & frame );
  int drawPeople(CrowdSight *  crowdsight, std::vector<Person> &people, cv::Mat &frame );
  int parseInput( CrowdSight * crowdsight );

private:
  void init();
  void drawPerson( Person * person, cv::Mat & frame );

  void overlayImage( const cv::Mat & background,
                     const cv::Mat & foreground,
                     const cv::Point location,
                     cv::Mat & output );

  VisualizationArguments mArgs;
  cv::Mat mCanvas;
  cv::Mat mStatsElement;
};

#endif // _VISUALIZATION_H_
