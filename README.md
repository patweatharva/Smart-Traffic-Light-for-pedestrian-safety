# Smart-Traffic-Light-for-pedestrian-safety
This repository contains the Python code for a smart traffic light project designed to enhance pedestrian safety. The system uses a camera to detect pedestrians at a zebra crossing and manipulates the traffic signals accordingly. The project can be integrated with existing traffic signal systems as an added functionality.


## Description
The project aims to provide warning signals to vehicles approaching a zebra crossing if a pedestrian is crossing the road. This system is especially useful during night conditions or when visibility is low, as it ensures that vehicle drivers are aware of pedestrians on the road.

### Conditions and regions
This system manipulates three signal, Vehicle red, Vehicle Green and Pedestrain Green for each lane.

Three regions are created on each lane of the road: Waiting_area_1, Main_Area, Waiting_Area_2. If a pedestrian is present in the Waiting_Area_1 or Waiting_Area_2, the pedestrian green signal and vehicle green signal blink with a certain frequency, indicating a state change and warning to both the pedestrian and the vehicle driver. 

If the pedestrian commits to crossing the road and enters the Main_Area, the pedestrian signal turns green, allowing them to cross the road, while the vehicle signal turns red, warning the driver to slow down and stop before the zebra crossing to let the pedestrian cross safely. After the pedestrian safely crosses the road, the vehicle signal turns green, allowing the vehicle to proceed, and the pedestrian signal stops being green.


following picture shows the schematic of the system.
![schematic](images/setup_schematic.png)

### Technical Implementation
The video obtained from the camera is used for person detection on the zebra crossing using [jetson-inference](https://github.com/dusty-nv/jetson-inference) and above mentioned conditions are checked.


## Installations
To install the system, you will need to install the latest version of [JetPack](https://developer.nvidia.com/embedded/jetpack) on your Jetson device. 


Then, follow the steps below to install the needed components on your Jetson.

### jetson-inference

This system uses the DNN objects from the [jetson-inference](https://github.com/dusty-nv/jetson-inference) project (also known as Hello AI World). 

To build and install jetson-inference, see [this page](https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md) or run the commands below:

```

$ cd ~
$ sudo apt-get install git cmake
$ git clone --recursive https://github.com/dusty-nv/jetson-inference
$ cd jetson-inference
$ mkdir build
$ cd build
$ cmake ../
$ make -j$(nproc)
$ sudo make install
$ sudo ldconfig

```
Before proceeding, it's worthwhile to test that [jetson-inference](https://github.com/dusty-nv/jetson-inference)  is working properly on your system by following this step of the Hello AI World tutorial:

* [Classifying Images with ImageNet](https://github.com/dusty-nv/jetson-inference/blob/master/docs/imagenet-console-2.md)


### Jetson.GPIO

Follow [this_page](https://pypi.org/project/Jetson.GPIO/#:~:text=In%20order%20to%20use%20the,to%20the%20newly%20created%20group.&text=Install%20custom%20udev%20rules%20by%20copying%20the%2099%2Dgpio.) for manual installation or run following command

```
sudo pip install Jetson.GPIO
```

Openup python shell to check correct installation by running following command

```
import Jetson.GPIO as GPIO
```

### numpy

Run following command

```
pip install --user numpy
```

### jetson-utils

Run following command

```
pip install --user jetson-utils
```

Openup python shell to check correct installation by running following command

```
import jetson-utils
```

### OpenCV

Run following command

```
pip install --user opencv-python
```

Openup python shell to check correct installation by running following command

```
import cv2
```

## Setting up regions

After setting up cameras on desired locations from where clear view of lane is visible capture a frame and save to local directory for setting up the regions.

### For saving a frame from live feed or video 

Run [capture_frame_from_video.py](https://github.com/patweatharva/Smart-Traffic-Light-for-pedestrian-safety/blob/main/capture_frame_from_video.py) after giving path to the video file or giving usb address of the camera connected.

press 'x' to capture a frame

The frame is then stored into the current working directory.

### For getting region coordinates

Run following python script to get the co-ordinates of the regions

[region_coordinates.py](https://github.com/patweatharva/Smart-Traffic-Light-for-pedestrian-safety/blob/main/region_coordinates.py)

Click on the window to get the coordinates of the region and note them and move onto the next step

### Putting coordinates in code

In [main.py](https://github.com/patweatharva/Smart-Traffic-Light-for-pedestrian-safety/blob/main/main.py) in the specified pts variable put the respective coordinates

![coordinates location in code](images/region_coordinates_copy.png) 


## Running the script

Connect following hardware to the jetson nano

1. One or two cameras
2. Relay modules connected to respective pins as mentioned in the script
3. Lamps connected to the relay module
4. 5V 3A power supply to jetson nano


There, you have it!!! 

You have successfully implemented the program 

You can autorun the script in jetson nano using following steps

1. Openup Terminal
2. Run

```
crontab -e
```
3. At the end, put following command

```
@reboot python3 path/to/script
```
at the place of python3 put path to your python3 interpreter


## Refrences 

*[jetson-inference](https://github.com/dusty-nv/jetson-inference)
*[jetson.GPIO](https://pypi.org/project/Jetson.GPIO/)
*[openCV](https://opencv.org/)


##Conclusion
This Smart Traffic Light project can help to improve pedestrian safety by providing warning signals to vehicle drivers when pedestrians are present at a zebra crossing. The system can be integrated with existing traffic signal systems and can be easily installed on Jetson devices. This project is an example of how computer vision and machine learning can be used in real-world applications to improve safety and quality of life.

##Note
Please note that the above code is tested on Jetson Xavier, It may not work on other platforms.

##Contribution
If you want to contribute to this project, you are most welcome. Just fork the repo and make a pull request.

##License
This project is licensed under the [MIT License](https://github.com/patweatharva/Smart-Traffic-Light-for-pedestrian-safety/blob/main/LICENSE) - see the LICENSE file for details.

##Contact
If you have any questions or feedback, please feel free to contact me at [patweatharva@gmail.com](patweatharva@gmail.com)

