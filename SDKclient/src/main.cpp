#include <iostream>
#include <string>

#include "main_loop.h"

#if defined( __APPLE__ ) && defined( PUBLIC_DEMO )
#include <mach-o/dyld.h>
#include <libgen.h>

//Find Resources folder inside an app bundle
std::string findResourcesPath()
{
  char pathbuf[PATH_MAX + 1];
  char *bundle_id;
  uint32_t  bufsize = sizeof( pathbuf );
  _NSGetExecutablePath( pathbuf, &bufsize);
  bundle_id = dirname(pathbuf);
  std::string bundle_id_str = bundle_id;
  return bundle_id_str + "/../Resources";
}
#endif


int main( int argc, char *argv[] )
{
  // Allocate argument structure
  MainLoopArguments args;

#ifndef PUBLIC_DEMO
  // Parse command line arguments
  switch( argc )
  {
    case 5:
      {
        args.captureInput      = argv[2];
        args.cameraName        = argv[3];
        args.authenticationKey = argv[4];

        if( strcmp( argv[1], "--file" ) == 0 )        // file input
        {
          args.source = VIDEO_FILE;
          break;
        }
        if( strcmp( argv[1], "--capture" ) == 0 )     // webcam input
        {
          args.captureDevice = atoi(argv[2]);
          args.source = WEBCAM;
          break;
        }
        else if( strcmp( argv[1], "--stream" ) == 0 ) // http stream input
        {
          // Example of an asf stream that can be opened by OpenCV
          // http://[ipaddress]/videostream.asf?user=[USER]&pwd=[PASSWORD]&resolution=64&rate=0
          args.source = VIDEO_STREAM;
          break;
        }
        else
        {
          std::cerr << "Invalid argument 2 :  " << argv[1] << std::endl << std::endl;
        }
      }
    default:
      {
        std::cout
            << "Usage: "
            << argv[0]
            << " --file <videofile> <camera name> <auth key>"
            << std::endl;
        std::cout
            << "       "
            << argv[0]
            << " --capture <camera-id> <camera name> <auth key>"
            << std::endl;
        std::cout
            << "       "
            << argv[0]
            << " --stream <stream-url> <camera name> <auth key>"
            << std::endl;
        return -1;
      }
  }
#elif defined( __APPLE__ )
  // For OSX app bundles set default paths to foo.app/Resources/data/
  // and foo.app/Resources/resources/
  std::string osxPathPrefix = findResourcesPath();
  args.dataDirPath = osxPathPrefix + "/data/";
  args.resourceDirPath = osxPathPrefix + "/resources/";
#endif

  // Setup capture resolution
  args.captureResolution = CaptureResolution( 640, 480 );

  // Allocate MainLoop
  MainLoop ml( args );

  return ml.run();
}

// Conversion to WinMain() entry point from main() for console free application in MSVC
#if MSVC
class Win32CommandLineConverter {
private:
  std::unique_ptr<char*[]> argv_;
  std::vector<std::unique_ptr<char[]> > storage_;
public:
  Win32CommandLineConverter()
  {
    LPWSTR cmd_line = GetCommandLineW();
    int argc;
    LPWSTR* w_argv = CommandLineToArgvW(cmd_line, &argc);
    argv_ = std::unique_ptr<char*[]>(new char*[argc]);
    storage_.reserve(argc);
    for(int i=0; i<argc; ++i) {
      storage_.push_back(ConvertWArg(w_argv[i]));
      argv_[i] = storage_.back().get();
    }
    LocalFree(w_argv);
  }
  int argc() const
  {
    return static_cast<int>(storage_.size());
  }
  char** argv() const
  {
    return argv_.get();
  }
  static std::unique_ptr<char[]> ConvertWArg(LPWSTR w_arg)
  {
    int size = WideCharToMultiByte(CP_UTF8, 0, w_arg, -1, nullptr, 0, nullptr, nullptr);
    std::unique_ptr<char[]> ret(new char[size]);
    WideCharToMultiByte(CP_UTF8, 0, w_arg, -1, ret.get(), size, nullptr, nullptr);
    return ret;
  }
};

int CALLBACK WinMain(HINSTANCE /* hInstance */, HINSTANCE /* hPrevInstance */, LPSTR /* lpCmdLine */, int /* nCmdShow */)
{
  Win32CommandLineConverter cmd_line;
  return main(cmd_line.argc(), cmd_line.argv());
}
#endif
