#include "main_loop.h"

#include <iostream>

#include <crowdsight.h>

MainLoop::MainLoop() : mCrowdSight( NULL ), mVisualization( NULL )
{
  init();
}


MainLoop::MainLoop( MainLoopArguments a ) : mArgs( a ), mCrowdSight( NULL ), mVisualization( NULL )
{
  init();
}


MainLoop::~MainLoop()
{
  delete mVisualization;
  mVisualization = NULL;
  delete mCrowdSight;
  mCrowdSight = NULL;
}


void MainLoop::init()
{
  // Open video capture source
  if( mArgs.source == WEBCAM )
  {
    mCap.open( mArgs.captureDevice );
  }
  else
  {
    mCap.open( mArgs.captureInput );
  }

  // Set capture resolution (default 640x480)
  mCap.set( CV_CAP_PROP_FRAME_WIDTH, mArgs.captureResolution.width );
  mCap.set( CV_CAP_PROP_FRAME_HEIGHT, mArgs.captureResolution.height );

  // Set up visualization arguments
  VisualizationArguments args;
  args.mainWindowName = "CrowdSight Tech Demo \t"+CrowdSight::getVersion();
  args.resourceDirPath = mArgs.resourceDirPath;
  args.waitKeyDelay = 1;

  // Allocate Visualization
  mVisualization = new Visualization( args );
}


int MainLoop::run()
{
  char key = -1;
  
  while(true)
  {
    // Allocate CrowdSight
    if( mCrowdSight == NULL )
    {
      mCrowdSight = new CrowdSight( mArgs.dataDirPath );
      mCrowdSight->useFastDetection( true );
    }

    // Authenticate CrowdSight
    if( !mCrowdSight->isAuthenticated() && !mCrowdSight->authenticate( mArgs.authenticationKey ) )
    {
      std::cerr << "Authentication Failed : " << mCrowdSight->getErrorDescription() << std::endl;
      return -1;
    }

    // Grab frame
    if( !grabFrame() )
    {
      std::cerr << "Failed to capture video frame"<< std::endl;
      continue;
    }

    // Process frame
    if( !mCrowdSight->process( mFrame ) )
    {
      std::cerr << "Failed to process frame : " << mCrowdSight->getErrorDescription() << std::endl;
      continue;
    }

    // Get the list of people in the last processed frame
    std::vector<Person> people;

    if ( !mCrowdSight->getCurrentPeople(people) )
    {
      std::cerr << mCrowdSight->getErrorDescription() << std::endl;
    }


    // Visualize retrieved information (and check for keyboard input)
    key = mVisualization->drawPeople(mCrowdSight, people, mFrame );

    // Quit if ESC or q was pressed
    if( key == 27 || key == 'q' || key == 'Q' )
    {
      break;
    }
  }

  return 0;
}

bool MainLoop::grabFrame()
{
  // Check if cap is open
  if ( !mCap.isOpened() )
  {
    std::cerr
        << "Couldn't capture video from input "
        << mArgs.captureInput
        << std::endl;
    return false;
  }

  // Capture frame
  mCap >> mFrame;

  // Flip frame horizontally if input source is a webcam or stream
  if( mArgs.source == WEBCAM || mArgs.source == VIDEO_STREAM )
  {
    cv::flip( mFrame, mFrame, 1 );
  }

  return true;
}

void MainLoop::setFrame( cv::Mat & frame )
{
  mFrame = frame;
}


