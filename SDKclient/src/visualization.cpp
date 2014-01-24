#include "visualization.h"

#include <iostream>

#include <crowdsight.h>

namespace VisualizationColor
{
  // Some color constants
  const cv::Scalar KCOLOR_BLUE_1  ( 0xe4, 0X5a, 0X5a );
  const cv::Scalar KCOLOR_GREEN_1 ( 0x10, 0xaa, 0x10 );
  const cv::Scalar KCOLOR_ORANGE_1( 0x00, 0x7f, 0xff );
  const cv::Scalar KCOLOR_WHITE_1 ( 0xff, 0xff, 0xff );
  const cv::Scalar KCOLOR_BLACK_1 ( 0x00, 0x00, 0x00 );

  const cv::Scalar KCOLOR_GREEN_2 ( 0x00, 0xff, 0x00 );
  const cv::Scalar KCOLOR_BLUE_2  ( 0xa1, 0x74, 0x00 );
  const cv::Scalar KCOLOR_RED_1   ( 0x00, 0x00, 0xff );
  const cv::Scalar KCOLOR_YELLOW_1( 0x00, 0xff, 0xff );
  const cv::Scalar KCOLOR_BROWN_1 ( 0x00, 0x40, 0xa0 );
  const cv::Scalar KCOLOR_PURPLE_1( 0xc8, 0x00, 0xc8 );
}

namespace VisualizationOffset
{

  const cv::Point KPOINT_OFFSET_INTERFACE ( 690, 75 );
  const cv::Point KPOINT_OFFSET_ID        ( 60, 14 );
  const cv::Point KPOINT_OFFSET_ATTENTION ( 60, 25 );
  const cv::Point KPOINT_OFFSET_AGE       ( 60, 36 );
  const cv::Point KPOINT_OFFSET_GENDER    ( 60, 47 );

  const cv::Point KPOINT_OFFSET_EMOTION_BAR_HAPPY     ( 60, 51 );
  const cv::Point KPOINT_OFFSET_EMOTION_BAR_SURPRISE  ( 60, 62 );
  const cv::Point KPOINT_OFFSET_EMOTION_BAR_ANGER     ( 60, 73 );
  const cv::Point KPOINT_OFFSET_EMOTION_BAR_DISGUSTED ( 60, 84 );
  const cv::Point KPOINT_OFFSET_EMOTION_BAR_FEAR      ( 60, 95 );
  const cv::Point KPOINT_OFFSET_EMOTION_BAR_SADNESS   ( 60, 106 );

}

namespace VisualizationFrame
{
  const cv::Rect KCAPTURE_ELEMENT_FRAME( 10, 10, 640, 480 );
}

namespace vcolor = VisualizationColor;
namespace voffset = VisualizationOffset;
namespace vframe = VisualizationFrame;


Visualization::Visualization()
{
  init();
}


Visualization::Visualization( VisualizationArguments a ) : mArgs( a )
{
  init();
}

/**
 * @brief init create windows and load resources
 *
 */
void Visualization::init()
{
  // Load visualization canvas
  std::string canvasImagePath = mArgs.resourceDirPath + "demo_dashboard.png";
  mCanvas = cv::imread( canvasImagePath );
  if( mCanvas.empty() )
  {
    std::cerr << "Failed to load canvas file : " << canvasImagePath << std::endl;
  }

  // Load stats panel background
  std::string statsImagePath = mArgs.resourceDirPath + "stats_background.png";
  mStatsElement = cv::imread( statsImagePath, CV_LOAD_IMAGE_UNCHANGED );
  if( mStatsElement.empty() )
  {
    std::cerr << "Failed to load stats file : " << statsImagePath << std::endl;
  }
}

/**
 * @brief draw draw and display the dashboard, camera feed and all information retrieved
 *
 * @param person the person information retrieved
 * @param frame the capture frame to draw retrieved information on
 */
int Visualization::draw(CrowdSight * crowdsight, Person * person, cv::Mat & frame )
{
  // Draw all retrieved information to capture frame
  if( person != NULL )
  {
    drawPerson( person, frame );
  }

  // Create a copy of the canvas
  cv::Mat canvasCopy;
  mCanvas.copyTo(canvasCopy);

  // Resize the capture frame and display it
  cv::Mat captureElement = canvasCopy( vframe::KCAPTURE_ELEMENT_FRAME );
  cv::Mat smallframe;
  cv::resize( frame, smallframe, captureElement.size() );
  smallframe.copyTo( captureElement );

  float fontsize= 1.0f;
  int spacing= 30;

  std::ostringstream age_string, gender_string, mood_string, headPose_string, fastDetect_string, maxNumPeople_string;
  age_string          << "1 Age Detection : "            << ( crowdsight->isAgeUsed()? "On":"Off" );
  gender_string       << "2 Gender Detection : "         << ( crowdsight->isGenderUsed()? "On":"Off" );
  mood_string         << "3 Mood Detection : "           << ( crowdsight->isMoodUsed()? "On":"Off" );
  headPose_string     << "4 HeadPose Detection : "       << ( crowdsight->isHeadPoseUsed()? "On":"Off" );
  fastDetect_string   << "5 Fast Face Detection : "      << ( crowdsight->isFastDetectionUsed()? "On":"Off" );
  maxNumPeople_string << "-/+ Max Number of People : "   << ( crowdsight->getMaxNumPeople());

  cv::putText( canvasCopy, age_string.str(),          cv::Point( voffset::KPOINT_OFFSET_INTERFACE.x, voffset::KPOINT_OFFSET_INTERFACE.y + 1 * spacing), cv::FONT_HERSHEY_PLAIN, fontsize, vcolor::KCOLOR_WHITE_1 );
  cv::putText( canvasCopy, gender_string.str(),       cv::Point( voffset::KPOINT_OFFSET_INTERFACE.x, voffset::KPOINT_OFFSET_INTERFACE.y + 2 * spacing), cv::FONT_HERSHEY_PLAIN, fontsize, vcolor::KCOLOR_WHITE_1 );
  cv::putText( canvasCopy, mood_string.str(),         cv::Point( voffset::KPOINT_OFFSET_INTERFACE.x, voffset::KPOINT_OFFSET_INTERFACE.y + 3 * spacing), cv::FONT_HERSHEY_PLAIN, fontsize, vcolor::KCOLOR_WHITE_1 );
  cv::putText( canvasCopy, headPose_string.str(),     cv::Point( voffset::KPOINT_OFFSET_INTERFACE.x, voffset::KPOINT_OFFSET_INTERFACE.y + 4 * spacing), cv::FONT_HERSHEY_PLAIN, fontsize, vcolor::KCOLOR_WHITE_1 );
  cv::putText( canvasCopy, fastDetect_string.str(),   cv::Point( voffset::KPOINT_OFFSET_INTERFACE.x, voffset::KPOINT_OFFSET_INTERFACE.y + 5 * spacing), cv::FONT_HERSHEY_PLAIN, fontsize, vcolor::KCOLOR_WHITE_1 );
  cv::putText( canvasCopy, maxNumPeople_string.str(), cv::Point( voffset::KPOINT_OFFSET_INTERFACE.x, voffset::KPOINT_OFFSET_INTERFACE.y + 6 * spacing), cv::FONT_HERSHEY_PLAIN, fontsize, vcolor::KCOLOR_WHITE_1 );

  cv::imshow( mArgs.mainWindowName, canvasCopy );

  // Check for keyboard input and return ASCII code of pressed key ( no input returns -1 )
  return parseInput(crowdsight);
}


int Visualization::drawPeople( CrowdSight * crowdsight, std::vector<Person> &people, cv::Mat &frame )
{

  for (unsigned int i = 0; i < people.size(); i++)
  {

  // Draw all retrieved information to capture frame
      drawPerson(&  people.at(i), frame );
  }

  // Create a copy of the canvas
  cv::Mat canvasCopy;
  mCanvas.copyTo(canvasCopy);

  // Resize the capture frame and display it
  cv::Mat captureElement = canvasCopy( vframe::KCAPTURE_ELEMENT_FRAME );
  cv::Mat smallframe;
  cv::resize( frame, smallframe, captureElement.size() );
  smallframe.copyTo( captureElement );

  float fontsize= 1.0f;
  int spacing= 30;

  std::ostringstream age_string, gender_string, mood_string, headPose_string, fastDetect_string, emotionDetect_string,clothDetect_string, maxNumPeople_string;
  age_string          << "1 Age Detection : "            << ( crowdsight->isAgeUsed()? "On":"Off" );
  gender_string       << "2 Gender Detection : "         << ( crowdsight->isGenderUsed()? "On":"Off" );
  mood_string         << "3 Mood Detection : "           << ( crowdsight->isMoodUsed()? "On":"Off" );
  headPose_string     << "4 HeadPose Detection : "       << ( crowdsight->isHeadPoseUsed()? "On":"Off" );
  fastDetect_string   << "5 Fast Face Detection : "      << ( crowdsight->isFastDetectionUsed()? "On":"Off" );
  clothDetect_string  << "6 Clothing Style : "           << ( crowdsight->isClothingColorsUsed()? "On":"Off" );
  emotionDetect_string<< "7 Emotion Detection : "        << ( crowdsight->isEmotionsUsed()? "On":"Off" );
  maxNumPeople_string << "-/+ Max Number of People : "   << ( crowdsight->getMaxNumPeople());

  cv::putText( canvasCopy, age_string.str(),          cv::Point( voffset::KPOINT_OFFSET_INTERFACE.x, voffset::KPOINT_OFFSET_INTERFACE.y + 1 * spacing), cv::FONT_HERSHEY_PLAIN, fontsize, vcolor::KCOLOR_WHITE_1 );
  cv::putText( canvasCopy, gender_string.str(),       cv::Point( voffset::KPOINT_OFFSET_INTERFACE.x, voffset::KPOINT_OFFSET_INTERFACE.y + 2 * spacing), cv::FONT_HERSHEY_PLAIN, fontsize, vcolor::KCOLOR_WHITE_1 );
  cv::putText( canvasCopy, mood_string.str(),         cv::Point( voffset::KPOINT_OFFSET_INTERFACE.x, voffset::KPOINT_OFFSET_INTERFACE.y + 3 * spacing), cv::FONT_HERSHEY_PLAIN, fontsize, vcolor::KCOLOR_WHITE_1 );
  cv::putText( canvasCopy, headPose_string.str(),     cv::Point( voffset::KPOINT_OFFSET_INTERFACE.x, voffset::KPOINT_OFFSET_INTERFACE.y + 4 * spacing), cv::FONT_HERSHEY_PLAIN, fontsize, vcolor::KCOLOR_WHITE_1 );
  cv::putText( canvasCopy, fastDetect_string.str(),   cv::Point( voffset::KPOINT_OFFSET_INTERFACE.x, voffset::KPOINT_OFFSET_INTERFACE.y + 5 * spacing), cv::FONT_HERSHEY_PLAIN, fontsize, vcolor::KCOLOR_WHITE_1 );
  cv::putText( canvasCopy, clothDetect_string.str(),  cv::Point( voffset::KPOINT_OFFSET_INTERFACE.x, voffset::KPOINT_OFFSET_INTERFACE.y + 6 * spacing), cv::FONT_HERSHEY_PLAIN, fontsize, vcolor::KCOLOR_WHITE_1 );
  cv::putText( canvasCopy, emotionDetect_string.str(),cv::Point( voffset::KPOINT_OFFSET_INTERFACE.x, voffset::KPOINT_OFFSET_INTERFACE.y + 7 * spacing), cv::FONT_HERSHEY_PLAIN, fontsize, vcolor::KCOLOR_WHITE_1 );
  cv::putText( canvasCopy, maxNumPeople_string.str(), cv::Point( voffset::KPOINT_OFFSET_INTERFACE.x, voffset::KPOINT_OFFSET_INTERFACE.y + 8 * spacing), cv::FONT_HERSHEY_PLAIN, fontsize, vcolor::KCOLOR_WHITE_1 );

  cv::imshow( mArgs.mainWindowName, canvasCopy );

  // Check for keyboard input and return ASCII code of pressed key ( no input returns -1 )
  return  parseInput(crowdsight);
}


/**
 * @brief drawPerson draws retrieved information on the supplied capture frame
 *
 * @param person the person information retrieved
 * @param frame the capture frame to be drawn upon
 */
void Visualization::drawPerson( Person * person, cv::Mat & frame )
{
  std::string ID   = person->getID();
  cv::Rect face              = person->getFaceRect();
  cv::Point leftEyePosition  = person->getLeftEye();
  cv::Point rightEyePosition = person->getRightEye();
  float yaw        = person->getHeadYaw();
  float pitch      = person->getHeadPitch();
  float roll       = person->getHeadRoll();

  std::vector<cv::Point> maskPoints = person->getTrackingPoints();

  // Draw mask points
  for(unsigned int i = 0; i < maskPoints.size(); ++i)
  {
    cv::circle( frame, maskPoints.at(i), 1, vcolor::KCOLOR_GREEN_1 );
  }

  cv::Point faceCenter;
  float halfWidth  = static_cast<float>( face.width  / 2 );
  faceCenter.x     = face.x + static_cast<int>( halfWidth );
  faceCenter.y     = face.y + static_cast<int>( halfWidth );

  // Draw face detection
  cv::Rect faceDetection( face.x      - static_cast<int>( face.width * 0.2f ),
                          face.y      - static_cast<int>( face.width * 0.2f ),
                          face.width  + static_cast<int>( face.width * 0.4f ),
                          face.height + static_cast<int>( face.width * 0.4f ) );

  cv::ellipse( frame, faceCenter, cv::Size( faceDetection.width / 3, faceDetection.height / 3 ), 61, 0.0, 328.0, vcolor::KCOLOR_BLUE_2, 1, CV_AA );

  // Draw eyes
  cv::circle( frame, rightEyePosition, 3, vcolor::KCOLOR_GREEN_1 );
  cv::circle( frame, leftEyePosition,  3, vcolor::KCOLOR_GREEN_1 );

  // Draw Stats panel
  cv::Point stats_pos = cv::Point( faceDetection.x + (int)( faceDetection.width / 1.51), faceDetection.y + (int) (faceDetection.height / 1.51 ));
  overlayImage( frame, mStatsElement, stats_pos, frame );

  std::vector<float> emotionPredictions = person->getEmotions();

  if (emotionPredictions.size() >0){
    float happy      = emotionPredictions[0];
    float surprise   = emotionPredictions[1];
    float anger      = emotionPredictions[2];
    float disgusted  = emotionPredictions[3];
    float fear       = emotionPredictions[4];
    float sadness    = emotionPredictions[5];

    // Draw emotions
    cv::rectangle( frame, stats_pos + voffset::KPOINT_OFFSET_EMOTION_BAR_HAPPY,     stats_pos + voffset::KPOINT_OFFSET_EMOTION_BAR_HAPPY +     cv::Point( static_cast<int>( 45.0f * happy ),     6 ), vcolor::KCOLOR_BLUE_2, CV_FILLED );
    cv::rectangle( frame, stats_pos + voffset::KPOINT_OFFSET_EMOTION_BAR_SURPRISE,  stats_pos + voffset::KPOINT_OFFSET_EMOTION_BAR_SURPRISE +  cv::Point( static_cast<int>( 45.0f * surprise ),  6 ), vcolor::KCOLOR_BLUE_2, CV_FILLED );
    cv::rectangle( frame, stats_pos + voffset::KPOINT_OFFSET_EMOTION_BAR_ANGER,     stats_pos + voffset::KPOINT_OFFSET_EMOTION_BAR_ANGER +     cv::Point( static_cast<int>( 45.0f * anger ),     6 ), vcolor::KCOLOR_BLUE_2, CV_FILLED );
    cv::rectangle( frame, stats_pos + voffset::KPOINT_OFFSET_EMOTION_BAR_DISGUSTED, stats_pos + voffset::KPOINT_OFFSET_EMOTION_BAR_DISGUSTED + cv::Point( static_cast<int>( 45.0f * disgusted ), 6 ), vcolor::KCOLOR_BLUE_2, CV_FILLED );
    cv::rectangle( frame, stats_pos + voffset::KPOINT_OFFSET_EMOTION_BAR_FEAR,      stats_pos + voffset::KPOINT_OFFSET_EMOTION_BAR_FEAR +      cv::Point( static_cast<int>( 45.0f * fear ),      6 ), vcolor::KCOLOR_BLUE_2, CV_FILLED );
    cv::rectangle( frame, stats_pos + voffset::KPOINT_OFFSET_EMOTION_BAR_SADNESS,   stats_pos + voffset::KPOINT_OFFSET_EMOTION_BAR_SADNESS +   cv::Point( static_cast<int>( 45.0f * sadness ),   6 ), vcolor::KCOLOR_BLUE_2, CV_FILLED );
  }

  // Draw ID
  putText( frame, ID, stats_pos +  voffset::KPOINT_OFFSET_ID, cv::FONT_HERSHEY_SIMPLEX, 0.30, vcolor::KCOLOR_BLACK_1 );


  // Draw head gaze
  float yawValue   = ( yaw + 1.0f ) / 2.0f;
  float pitchValue = ( pitch + 1.0f ) / 2.0f;
  cv::line( frame, cv::Point( faceCenter.x, faceCenter.y ),
            cv::Point( face.x + static_cast<int>( yawValue * face.width ), face.y + static_cast<int>( pitchValue * face.height ) ),
            vcolor::KCOLOR_WHITE_1, 2 );

  // Draw attention span in minutes:seconds
  int attentionSpan = static_cast<int>( person->getAttentionSpan() );
  std::stringstream to_string;


  bool rc = person->isReturningCustomer();

  int minutes = ( attentionSpan / 60000 );
  int seconds = ( attentionSpan / 1000 ) % 60;
  to_string << minutes;
  if (seconds < 10) { to_string << ":0" << seconds << " " << rc; }
  else              { to_string << ":"  << seconds << " " << rc; }
  putText( frame, to_string.str(), stats_pos + voffset::KPOINT_OFFSET_ATTENTION, cv::FONT_HERSHEY_SIMPLEX, 0.30, vcolor::KCOLOR_BLACK_1 );

  // Draw Age
  int age = person->getAge();
  age = ( age / 10 ) * 10;
  to_string.str( "" );
  to_string << age << "-" << age + 10;
  putText( frame, to_string.str(), stats_pos + voffset::KPOINT_OFFSET_AGE, cv::FONT_HERSHEY_SIMPLEX, 0.30, vcolor::KCOLOR_BLACK_1 );

  // Draw Gender
  float gender = person->getGender();
  std::string genderStr = "";
  if( gender > 0.2f ) genderStr = "Female";
  else if( gender < -0.2f ) genderStr = "Male";
  putText( frame, genderStr, stats_pos + voffset::KPOINT_OFFSET_GENDER, cv::FONT_HERSHEY_SIMPLEX, 0.30, vcolor::KCOLOR_BLACK_1 );

  // Draw mood
  float mood = person->getMood();
  float moodValue = ( mood + 1.0f ) / 2.0f;
  cv::ellipse( frame, faceCenter,
               cv::Size( faceDetection.width / 3, faceDetection.height / 3 )+ cv::Size( 5, 5 ),
               150, 0.0, 60.0, vcolor::KCOLOR_WHITE_1, 2, CV_AA );
  cv::ellipse( frame, faceCenter,
               cv::Size( faceDetection.width / 3, faceDetection.height / 3 )+ cv::Size( 5, 5 ),
               150, 0.0, 60.0 * moodValue, vcolor::KCOLOR_BLUE_2, 3, CV_AA );

  // Draw binned clothing colors
  std::vector< std::vector<int> > clothingColors = person->getClothingColors();
  if(clothingColors.size() )
  {
    int numColors = clothingColors.size();
    for( int i = 0; i < numColors; ++i )
    {
      cv::ellipse( frame, faceCenter,
                   cv::Size( faceDetection.width / 3, faceDetection.height / 3 ) + cv::Size( 10, 10 ),
                   150,
                   ( 60.0 / numColors ) * i,
                   ( 60.0 / numColors ) * ( i + 1 ),
                   cv::Scalar( clothingColors[i][2], clothingColors[i][1], clothingColors[i][0] ),
          3, CV_AA );
    }
  }
}



int Visualization::parseInput( CrowdSight *crowdsight )
{
  //Press Esc, q to quit the program
  int key = cv::waitKey( mArgs.waitKeyDelay );


  if (key == '1')
  {
    if ( crowdsight->isAgeUsed() ) { crowdsight->useAge( false ); }
    else                          { crowdsight->useAge( true ); }
  }

  if (key == '2')
  {
    if ( crowdsight->isGenderUsed() ) { crowdsight->useGender( false ); }
    else                             { crowdsight->useGender( true ); }
  }

  if (key == '3')
  {
    if ( crowdsight->isMoodUsed() ) { crowdsight->useMood( false ); }
    else                           { crowdsight->useMood( true ); }
  }

  if (key == '4')
  {
    if ( crowdsight->isHeadPoseUsed() ) { crowdsight->useHeadPose( false ); }
    else                               { crowdsight->useHeadPose( true ); }
  }

  if (key == '5')
  {
    if ( crowdsight->isFastDetectionUsed() ) { crowdsight->useFastDetection( false ); }
    else                                    { crowdsight->useFastDetection( true ); }
  }

  if (key == '6')
  {
    if ( crowdsight->isClothingColorsUsed() ) { crowdsight->useClothColors(false ); }
    else                                    { crowdsight->useClothColors( true ); }
  }

  if (key == '7')
  {
    if ( crowdsight->isEmotionsUsed() ) { crowdsight->useEmotions( false ); }
    else                                    { crowdsight->useEmotions( true ); }
  }

  if (key == '-')
  {
    crowdsight->setMaxNumPeople( crowdsight->getMaxNumPeople() - 1 );
  }

  if (key == '=')
  {
    crowdsight->setMaxNumPeople( crowdsight->getMaxNumPeople() + 1 );
  }

  // Example for storing/loading models
  std::string saveId        = "1";
  std::string saveName      = "Subject 1";
  std::string saveModelName = "Model.bin";

  if (key == 'r')
  {
    crowdsight->saveModel( saveId, saveName, saveModelName );
  }

  if (key == 'l')
  {
    crowdsight->loadModel( saveModelName );
  }

  if (key == 'd')
  {
    crowdsight->unloadModel( saveName );
  }
  
  if( !cvGetWindowHandle( mArgs.mainWindowName.c_str() ) )
  {
    key = 'q';
  }

  return key;
}


/**
 * @brief overlayImage draws an image on top of a given image taking into account
 * the alpha channel
 *
 * @param[in] background the image to draw on
 * @param[in] foreground the image to be drawn
 * @param[in] origin origin of foreground image inside background image
 * @param[out] output resulting image
 */
void Visualization::overlayImage( const cv::Mat & background,
                                  const cv::Mat & foreground,
                                  const cv::Point origin,
                                  cv::Mat & output )
{
  background.copyTo( output );

  // start at the row indicated by origin, or at row 0 if origin.y is negative.
  for( int y = std::max( origin.y , 0 ); y < background.rows; ++y )
  {
    int fY = y - origin.y; // because of the translation

    // we are done of we have processed all rows of the foreground image.
    if( fY >= foreground.rows )
      break;

    // start at the column indicated by origin,

    // or at column 0 if origin.x is negative.
    for( int x = std::max( origin.x, 0 ); x < background.cols; ++x )
    {
      int fX = x - origin.x; // because of the translation.

      // we are done with this row if the column is outside of the foreground image.
      if( fX >= foreground.cols )
        break;

      // determine the opacity of the foregrond pixel, using its fourth (alpha) channel.
      double opacity =
          ( ( double )foreground.data[fY * foreground.step + fX * foreground.channels() + 3] )
          / 255.;

      // and now combine the background and foreground pixel, using the opacity,
      // but only if opacity > 0.
      for( int c = 0; opacity > 0 && c < output.channels(); ++c )
      {
        unsigned char foregroundPx =
            foreground.data[fY * foreground.step + fX * foreground.channels() + c];
        unsigned char backgroundPx =
            background.data[y * background.step + x * background.channels() + c];
        output.data[y * output.step + output.channels() * x + c] =
            backgroundPx * ( 1.- opacity ) + foregroundPx * opacity;
      }
    }
  }
}

