all: main.o main_loop.o visualization.o client.o
	g++ main.o main_loop.o visualization.o client.o -g -o example -L../lib -lcrowdsight -lopencv_calib3d -lopencv_contrib -lopencv_core -lopencv_features2d -lopencv_flann -lopencv_gpu -lopencv_highgui -lopencv_imgproc -lopencv_legacy -lopencv_ml -lopencv_objdetect -lopencv_photo -lopencv_stitching -lopencv_superres -lopencv_ts -lopencv_video -lopencv_videostab

main.o:
	g++ -c -I../include -I/home/diego/Work/SightCorp/CrowdSight/lib/Utilities/src src/main.cpp -g

main_loop.o:
	g++ -c -I../include -I/home/diego/Work/SightCorp/CrowdSight/lib/Utilities/src src/main_loop.cpp -g

visualization.o:
	g++ -c -I../include -I/home/diego/Work/SightCorp/CrowdSight/lib/Utilities/src src/visualization.cpp -g

client.o:
	g++ -c -I../include -I/home/diego/Work/SightCorp/CrowdSight/lib/Utilities/src src/client.cpp -g

clean:
	rm -f *.o example
