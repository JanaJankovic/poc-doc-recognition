# Pocket-Doctor Recognition
> This repository is intented for analysis of moles/skin cancer and seborrheic keratosis.</br> 
Nevus -> Birthmark<br/>
Melanoma -> Skin cancer<br/>
Seborrheic keratosis -> Common noncancerous skin growth

## Table of contents
* [General info](#general-info)
* [Screenshots](#screenshots)
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)
* [Status](#status)
* [Inspiration](#inspiration)
* [Contact](#contact)

## General info
Pocket Doctor is an app intented to simulate the usage of blockchain in a healthcare system. It was developed as a student project with a potential to grow. So far it consists out of 6 repositories :
* [Android](https://github.com/JanaJankovic/poc-doc-android)
* [Blockchain](https://github.com/PetrovicGoran/blchain-hopefully-working)
* [Backend](https://github.com/PetrovicGoran/poc-doc-backend)
* [Frontend](https://github.com/PetrovicGoran/poc-doc-frontend)
* [Arduino](https://github.com/JanaJankovic/poc-doc-arduino)
* Recognition (this once)

You can see whole presention [here](https://univerzamb-my.sharepoint.com/:p:/g/personal/jana_jankovic_student_um_si/ETQo1_cbyKlDnSKktxM6_YABnMsRZP8nEeGqBBbXq_wHtg?e=2ceRYw)

## Screenshots
### Input
![Input](https://github.com/JanaJankovic/poc-doc-recognition/blob/master/screenshots/Screenshot_1.jpg)
### Output
![Output](https://github.com/JanaJankovic/poc-doc-recognition/blob/master/screenshots/Screenshot_2.jpg)

## Technologies
* Python 
* TensorFlow 

## Setup
### Python http server
What to do to make it running
1. pull file <b>py_server.py</b> from git to recognition folder (put it along with other python scripts)<br/>
2. create folders: <b>images</b> and <b>images_res</b><br/>
3. in script <b>local_operators.py</b> <b>comment every pyplot show and every unnecessary print (like print(category) )</b>
3. in recognition folder, open <b>command prompt</b> and run command: <b>python py_server.py</b><br/>
4. Test if everything works in Postman: send <b>POST</b> request to URL: <b>http://<your_local_ip_address>:9090/poc-doc/recognise</b>  , in request <b>body</b> click on radio button value <b>form-data</b> and add new entry: key = <b>image</b> (change from type Text to <b>File</b> , Value = <b>select any .jpg image from your computer you want to upload</b><br/>
5. Is everything works, response should give you JSON with 3 key-value pairs: status (true), imageBytes and category

### Model installation 
Dataset : https://www.kaggle.com/wanderdust/skin-lesion-analysis-toward-melanoma-detection<br/>

How to install model :
1. extract dataset and rename it to dataset_raw<br/>
2. install all modules<br/>
3. run preprocessing<br/>
4. run machine_learning.py<br/>

## How to use local_operators.py
```python
def locate_object(picture_path, photo_saved_location, model_path, size, predicted_save_location)
```
**Return value** - path to where end result picture is saved and string category<br/>

**picture_path** - string <br/>
* example : 'server_side_pics\\img_123.jpg'<br/>

**photo_saved_location** - string<br/>
* should be saved in folder predict_set<br/>

**model_path** - string<br/>
* should be just 'model'<br/>

**size** - int<br/>
* should be size of model we trained, 128<br/>

**predicted_save_location** - string<br/>
* folder name of place for saving picture, should be predicted_set, or anything from where you will read it and send back to android</br>

Example call : 
```python
locate_object('dataset_size128\\train\\nevus\\ISIC_0012680.jpg', "predict_set", "model", 128, "predicted_set")
```

## Features
List of features ready and TODOs for future development
* Analysis of input picture
* Creating result picture
* Sending result picture from server to client

## Status
Project is: _finished_
Purpose of this project is to analyze input photo and give output.

## Inspiration
Project is supported by [The Faculty of Electrical Engineering and Computer Science](https://feri.um.si/) and [University of Maribor](https://www.um.si/Strani/default.aspx).

## Contact
Created by [Jana Jankovic](https://github.com/JanaJankovic) - feel free to contact me on one of the emails :
* jana.jankovic@student.um.si
* jana.j00@outlook.com
* jana.jankovic.feri@gmail.com

Supported by [Goran Petrovic](https://github.com/PetrovicGoran) - feel free to contact him :
* goran.petrovic1@student.um.si

Suppored by [Nikola Vilar Jordanovski](https://github.com/NikolaVilar) - feel free to contact him :
* nikola.vialr@student.um.si
