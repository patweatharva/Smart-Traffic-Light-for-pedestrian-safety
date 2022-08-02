# Smart-Traffic-Light-for-pedestrian-safety
This repo contains the python code for Smart traffic light project.

## Description
This project was initiated to make sure vehicles coming towards the zebra crossing get warning signal if a person is crossing the road from zebra crossing.This will enhance the safety of pedestrians especially in the night conditions or if the visibility is very low and vehicle driver is unable to see if the road is clear or not. This system can be integrated with existing traffic signal for added functionality.


### Conditions and regions
This system manipulates three signal, Vehicle red, Vehicle Green and Pedestrain Green for each lane.

Three regions are created on each lane of the road, Waiting_area_1, Main_Area, Waiting_Area_2.If a person is present in Waiting_Area_1 or Waiting_Area_2 the Pedestrain green and vehicle green signal blinks with some frequency indicating the state change and warning to the pedestrain and to the vehicle driver that person is about to enter into the the zebra crossing so, GO SLOW!!

If the person commits to the zebra cross and enter into the Main_Area, the pedestrain signal turns green allowing pedestrian to walk across the road but the vehicle signal turns red and warns the driver to slow down and stop the vechicle before zebracross and let that person cross the road. After the person safely crosses the road, vehicle signal turns green allowing vehicel to go and pedestrian signal stops being green.

following picture shows the schematic of the system.
![schematic](setup.jpg)

### How it's done
The video obtained from the camera is used for person detection on the zebra crossing using [jetson-inference](https://github.com/dusty-nv/jetson-inference) and above mentioned conditions are checked.


## Installations
First, install the latest version of [JetPack](https://developer.nvidia.com/embedded/jetpack) on your Jetson.

Then, follow the steps below to install the needed components on your Jetson.

### jetson-inference

This system uses the DNN objects from the [jetson-inference](https://github.com/dusty-nv/jetson-inference) project (aka Hello AI World). To build and install jetson-inference, see [this_page](https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md) or run the commands below:

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

