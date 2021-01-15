# PYTHON HTTP SERVER
What to do to make it running
1. pull file <b>py_server.py</b> from git to recognition folder (put it along with other python scripts)<br/>
2. create folders: <b>images</b> and <b>images_res</b><br/>
3. in recognition folder, open <b>command prompt</b> and run command: <b>python py_server.py</b><br/>
4. Test if everything works in Postman: send <b>POST</b> request to URL: <b>http://<your_local_ip_address>:9090/poc-doc/recognise  , in request <b>body</b> click on radio button value <b>form-data</b> and add new entry: key = <b>image</b> (change from type Text to <b>File</b> , Value = <b>select any .jpg image from your computer you want to upload</b><br/>
5. Is everything works, response should give you JSON with 3 key-value pairs: status (true), imageBytes and category

# poc-doc-recognition

Dataset : https://www.kaggle.com/wanderdust/skin-lesion-analysis-toward-melanoma-detection<br/>
Nevus -> Birthmark<br/>
Melanoma -> Skin cancer<br/>
Seborrheic keratosis -> Common noncancerous skin growth<br/>

## Model installation 

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
## Result
### Input
![Input](https://github.com/JanaJankovic/poc-doc-recognition/blob/master/screenshots/Screenshot_1.jpg)
### Output
![Output](https://github.com/JanaJankovic/poc-doc-recognition/blob/master/screenshots/Screenshot_2.jpg)

