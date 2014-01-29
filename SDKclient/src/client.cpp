#include "client.h"

#include <util/parsers.h>
#include <util/util.h>
#include <iomanip>

const std::string Client::KServerURL       = "http://localhost:8000";
const std::string Client::KStartSessionURL = "/start_session/";
const std::string Client::KSendPersonURL   = "/person_detection/";
const std::string Client::KStopSessionURL  = "/stop_session/";


// Utilities //

std::string getColorString( const std::vector<int> & color )
{
  std::stringstream result;
  result << "#" << std::hex <<
      std::setw( 2 ) << std::setfill( '0' ) << color[0] <<
      std::setw( 2 ) << std::setfill( '0' ) << color[1] <<
      std::setw( 2 ) << std::setfill( '0' ) << color[2];
  return result.str();
}

template<class T>
bool getJsonParam( JsonParser::TMembers & jsonMembers,
                   const std::string & param,
                   T & result )
{
  if( !jsonMembers.containsKey( param ) )
    return false;

  if( !Util::getValueFromString( jsonMembers[ param ], result ) )
    return false;

  return true;
}

bool parseGenericResponse( const std::string &          jsonText,
                                 JsonParser::TMembers & jsonMembers )
{
  if( !JsonParser::parseJson( jsonText, jsonMembers ) )
  {
    std::cerr << "Bad server response format : " << jsonText << std::endl;
    return false;
  }

  int code;
  if( !getJsonParam( jsonMembers, "code", code ) )
  {
    std::cerr << "Bad server response format. Missing 'code'." << std::endl;
    return false;
  }

  if( code != 0 )
  {
    std::string tmpDescription;
    if( getJsonParam( jsonMembers, "code", tmpDescription ) )
      std::cerr << "Server error description : " << tmpDescriprion << std::endl;
  }
  return code == 0;
}

// End Utilities //


Client::Client( const std::string & cameraName ) :
    mConnection( new Connection() ),
    mSessionKey( "" ),
    mSessionStarted( false )
{
  mConnection->init( "", 0, "", "" ); // No proxy
  mSessionStarted = startSession( cameraName );
}

Client::~Client()
{
  stopSession();
  delete mConnection;
}

bool Client::startSession( const std::string & cameraName )
{
  Connection::Response serverResponse;
  Connection::TRequest startSessionRequest;
  startSessionRequest[ "source_name" ] = cameraName;

  bool isConnected = mConnection->request( KServerURL + KStartSessionURL,
                                           startSessionRequest,
                                           serverResponse );
  if( isConnected )
  {
    if( !serverResponse.isReady() || !serverResponse.isOk() )
    {
      std::cerr << "Could not start a session" << std::endl;
      return false;
    }

    return parseStartSession( serverResponse.rawResponse );
  }
  else
  {
    std::cerr << mConnection->getErrorDescription() << std::endl;
  }

  return false;
}

bool Client::stopSession()
{
  Connection::Response serverResponse;
  Connection::TRequest stopSessionRequest;
  stopSessionRequest[ "session_key" ] = mSessionKey;

  bool isConnected = mConnection->request( KServerURL + KStopSessionURL,
                                           stopSessionRequest,
                                           serverResponse );
  if( isConnected )
  {
    if( !serverResponse.isReady() || !serverResponse.isOk() )
    {
      std::cerr << "Could not stop a session" << std::endl;
      return false;
    }

    return parseStopSession( serverResponse.rawResponse );
  }
  else
  {
    std::cerr << mConnection->getErrorDescription() << std::endl;
  }

  return false;
}

bool Client::sendPeople( std::vector<Person> &people, int frameNumber )
{
  Connection::Response serverResponse;
  Connection::TRequest sendPersonRequest;
  sendPersonRequest[ "session_key" ] = mSessionKey;
  sendPersonRequest[ "frame" ]       = Util::getStringFromValue( frameNumber );

  bool allSent = true;

  std::string                     tmpID;
  cv::Rect                        tmpFacePosition;
  cv::Point                       tmpEyeLocation;
  std::vector<float>              tmpEmotions;
  std::vector< std::vector<int> > tmpClothColors;

  for( std::vector<Person>::iterator person_it = people.begin();
       person_it != people.end();
       ++person_it )
  {
    tmpID = person_it->getID();
    if( tmpID.empty() )
    {
      std::cerr << "No ID on this person... Skip (tmp)" << std::endl;
      continue;
    }
    sendPersonRequest[ "sdk_name" ]       = tmpID;
    sendPersonRequest[ "age" ]            = Util::getStringFromValue( person_it->getAge() );
    sendPersonRequest[ "gender" ]         = Util::getStringFromValue( person_it->getGender() );
    sendPersonRequest[ "mood" ]           = Util::getStringFromValue( person_it->getMood() );
    tmpFacePosition = person_it->getFaceRect();
    sendPersonRequest[ "facePosition_x" ] = Util::getStringFromValue( tmpFacePosition.x );
    sendPersonRequest[ "facePosition_y" ] = Util::getStringFromValue( tmpFacePosition.y );
    sendPersonRequest[ "facePosition_w" ] = Util::getStringFromValue( tmpFacePosition.width );
    sendPersonRequest[ "facePosition_h" ] = Util::getStringFromValue( tmpFacePosition.height );
    sendPersonRequest[ "headYaw" ]        = Util::getStringFromValue( person_it->getHeadYaw() );
    sendPersonRequest[ "headPitch" ]      = Util::getStringFromValue( person_it->getHeadPitch() );
    tmpEyeLocation = person_it->getRightEye();
    sendPersonRequest[ "rightEye_x" ]     = Util::getStringFromValue( tmpEyeLocation.x );
    sendPersonRequest[ "rightEye_y" ]     = Util::getStringFromValue( tmpEyeLocation.y );
    tmpEyeLocation = person_it->getLeftEye();
    sendPersonRequest[ "leftEye_x" ]      = Util::getStringFromValue( tmpEyeLocation.x );
    sendPersonRequest[ "leftEye_y" ]      = Util::getStringFromValue( tmpEyeLocation.y );
    sendPersonRequest[ "head_roll" ]      = Util::getStringFromValue( person_it->getHeadRoll() );
    sendPersonRequest[ "attention_span" ] = Util::getStringFromValue( person_it->getAttentionSpan() );
    tmpEmotions = person_it->getEmotions();
    sendPersonRequest[ "neutral" ]        = "0";
    sendPersonRequest[ "happy" ]          = Util::getStringFromValue( tmpEmotions[0] );
    sendPersonRequest[ "surprised" ]      = Util::getStringFromValue( tmpEmotions[1] );
    sendPersonRequest[ "angry" ]          = Util::getStringFromValue( tmpEmotions[2] );
    sendPersonRequest[ "disgusted" ]      = Util::getStringFromValue( tmpEmotions[3] );
    sendPersonRequest[ "afraid" ]         = Util::getStringFromValue( tmpEmotions[4] );
    sendPersonRequest[ "sad" ]            = Util::getStringFromValue( tmpEmotions[5] );
    tmpClothColors = person_it->getClothingColors();
    if( !tmpClothColors.empty() )
    {
      sendPersonRequest[ "ClothesColors_1" ] = getColorString( tmpClothColors[0] );
      sendPersonRequest[ "ClothesColors_1" ] = getColorString( tmpClothColors[1] );
      sendPersonRequest[ "ClothesColors_1" ] = getColorString( tmpClothColors[2] );
    }

    bool isConnected = mConnection->request( KServerURL + KSendPersonURL,
                                             sendPersonRequest,
                                             serverResponse );
    if( isConnected )
    {
      if( !serverResponse.isReady() || !serverResponse.isOk() )
      {
        std::cerr << "Could not send person analysis" << std::endl;
        allSent = false;
      }
  
      allSent &= parseSendPerson( serverResponse.rawResponse );
    }
    else
    {
      std::cerr << mConnection->getErrorDescription() << std::endl;
      allSent = false;
    }
  }
  return allSent;
}

bool Client::parseStartSession( const std::string & response )
{
  JsonParser::TMembers jsonMembers;
  // Parse the response into a json structure and check for error codes.
  if( !parseGenericResponse( response, jsonMembers ) )
    return false;

  if( !getJsonParam( jsonMembers, "session_key", mSessionKey ) )
  {
    std::cerr << "Bad response formatting. Expecting session key." << std::endl;
    return false;
  }
  return true;
}

bool Client::parseSendPerson( const std::string & response )
{
  JsonParser::TMembers jsonMembers;
  // Parse the response into a json structure and check for error codes.
  if( !parseGenericResponse( response, jsonMembers ) )
    return false;

  return true;
}

bool Client::parseStopSession( const std::string & response )
{
  JsonParser::TMembers jsonMembers;
  // Parse the response into a json structure and check for error codes.
  if( !parseGenericResponse( response, jsonMembers ) )
    return false;

  return true;
}

