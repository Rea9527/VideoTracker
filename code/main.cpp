//
//  main.cpp
//  VideoTracker
//
//  Created by 陈主润 on 26/06/2017.
//  Copyright © 2017 陈主润. All rights reserved.
//

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <algorithm>
#include <cstdio>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#include "KCF/kcftracker.hpp"

#include <dirent.h>

using namespace std;
using namespace cv;

int main(int argc, char* argv[]){
    
    if (argc > 5) return -1;
    
    bool HOG = true;
    bool FIXEDWINDOW = false;
    bool MULTISCALE = true;
    bool SILENT = false;
    bool LAB = false;
    
    for(int i = 0; i < argc; i++){
        if ( strcmp (argv[i], "hog") == 0 )
            HOG = true;
        if ( strcmp (argv[i], "fixed_window") == 0 )
            FIXEDWINDOW = true;
        if ( strcmp (argv[i], "singlescale") == 0 )
            MULTISCALE = false;
        if ( strcmp (argv[i], "show") == 0 )
            SILENT = false;
        if ( strcmp (argv[i], "lab") == 0 ){
            LAB = true;
            HOG = true;
        }
        if ( strcmp (argv[i], "gray") == 0 )
            HOG = false;
    }
    
    // Create KCFTracker object
    KCFTracker tracker(HOG, FIXEDWINDOW, MULTISCALE, LAB);
    
    // Frame readed
    Mat frame;
    
    // Tracker results
    Rect result;
    
    int folderSize;
    cin >> folderSize;
    
//    char cstr[10];
    // Write Results
    ofstream resultsFile;
    string resultsPath = "./output.txt";
    resultsFile.open(resultsPath.c_str());
    resultsFile << "filename";
    for (int i = 1; i < folderSize / 2 + 1; i++) {
        
        resultsFile << ",";
        string d = "d" + to_string(i);
//        sprintf(cstr,"%d",i);
        resultsFile << d;
    }
    resultsFile << endl;
    
    
    
    string rootFolder = "./frames2/";
    for (int curVideo = 0; curVideo < folderSize; curVideo++) {
        
        if (curVideo == 36 || curVideo == 37 || curVideo == 78 || curVideo == 79 || curVideo == 84 ||
            curVideo == 85 || curVideo == 116 || curVideo == 117) continue;
        
        string folder = to_string(curVideo);

        // Read groundtruth for the 1st frame
        ifstream groundtruthFile;
        string groundtruth = rootFolder + folder + "/region.txt";
//        cout << groundtruth << endl;
//        string groundtruth = "./rotate/" + to_string(curVideo) + "/region.txt";
        groundtruthFile.open(groundtruth.c_str());
        string firstLine;
        getline(groundtruthFile, firstLine);
        groundtruthFile.close();
        
        istringstream ss(firstLine);
        
        // Read groundtruth like a dumb
        string word;
        float x1, y1, x2, y2, x3, y3, x4, y4;
        vector<float> rect;
        while (getline(ss, word, ' ')) {
            cout << word << " ";
            rect.push_back(atof(word.c_str()));
        }
        cout << endl;
        x1 = rect[0];
        y1 = rect[1];
        x2 = rect[2];
        y2 = rect[3];
        x3 = rect[4];
        y3 = rect[5];
        x4 = rect[6];
        y4 = rect[7];
        
        // Using min and max of X and Y for groundtruth rectangle
        float xMin =  min(x1, min(x2, min(x3, x4)));
        float yMin =  min(y1, min(y2, min(y3, y4)));
        float width = max(x1, max(x2, max(x3, x4))) - xMin;
        float height = max(y1, max(y2, max(y3, y4))) - yMin;
        cout << curVideo << " " << xMin << " " << yMin << " " << width << " " << height << endl;
        
        // Read Images
        ifstream listFramesFile;
        string listFrames = rootFolder + folder + "/images.txt";
//        string listFrames = "./rotate/" + to_string(curVideo) + "/images.txt";
        listFramesFile.open(listFrames.c_str());
        string frameName;
    
        
        // Frame counter
        int nFrames = 0;
        
        float scaleWidth, scaleHeight;
        if (curVideo <= 129) {
            scaleWidth = 228.0 / 960.0;
            scaleHeight = 128.0 / 540.0;
            
        } else {
            scaleWidth = 228.0 / 1794.0;
            scaleHeight = 128.0 / 1080.0;
        }
        
        
        
        while ( getline(listFramesFile, frameName) ){
//            string framepath = "./allframes/" + frameName;
            string framepath = "./allframes/" + frameName;
            
            // Read each frame from the list
            cout << framepath << endl;
            frame = imread(framepath, CV_LOAD_IMAGE_COLOR);
            resultsFile << frameName << ",";
            
            //add ,
            for (int i = 0; i < curVideo / 2; i++)
                resultsFile << ",";
            
            // First frame, give the groundtruth to the tracker
            if (nFrames == 0) {
                tracker.init( Rect(xMin, yMin, width, height), frame );
                rectangle( frame, Point( xMin, yMin ), Point( xMin+width, yMin+height), Scalar( 0, 255, 255 ), 1, 8 );
                
                resultsFile << (int)(xMin * scaleWidth) << "&" << (int)(yMin * scaleWidth) << "&" << (int)(width * scaleWidth) << "&" << (int)(height * scaleWidth);
//                resultsFile << xMin << "&" << yMin << "&" << width << "&" << height;
            }
            // Update
            else{
                result = tracker.update(frame);
                rectangle( frame, Point( result.x, result.y ), Point( result.x+result.width, result.y+result.height), Scalar( 0, 255, 255 ), 1, 8 );
                resultsFile << (int)(result.x * scaleWidth) << "&" << (int)(result.y * scaleWidth) << "&" << (int)(result.width * scaleWidth) << "&" << (int)(result.height * scaleWidth);
//                resultsFile << result.x << "&" << result.y << "&" << result.width << "&" << result.height;
            }
            
            for (int i = curVideo / 2 + 1; i < folderSize / 2 + 1; i++) {
                resultsFile << ",";
            }
            resultsFile << endl;
            
            nFrames++;
            
            if (!SILENT){
                imshow("Image", frame);
                waitKey(1);
            }
        }
        
    }
    
    resultsFile.close();
    
}


