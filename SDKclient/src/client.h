#include <crowdsight.h>
#include <util/connection.h>

class Client
{
public:
  Client( const std::string & cameraName );
  virtual ~Client();

  bool sendPeople( std::vector<Person> &people, int frameNumber );

private:
  // Private Functions
  bool startSession( const std::string & cameraName );
  bool stopSession();

  bool parseStartSession( const std::string & response );
  bool parseSendPerson(   const std::string & response );
  bool parseStopSession(  const std::string & response );

  // Private Members
  Connection * mConnection;
  std::string  mSessionKey;
  bool         mSessionStarted;

  static const std::string KServerURL;
  static const std::string KStartSessionURL;
  static const std::string KSendPersonURL;
  static const std::string KStopSessionURL;
};
