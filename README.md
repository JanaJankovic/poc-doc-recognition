# poc-doc-recognition
Dataset : https://www.kaggle.com/wanderdust/skin-lesion-analysis-toward-melanoma-detection<br/>
Nevus -> Birthmark<br/>
Melanoma -> Skin cancer<br/>
Seborrheic keratosis -> Common noncancerous skin growth<br/>

How to install model :
1. extract dataset and rename it to dataset_raw<br/>
2. install all modules<br/>
3. run preprocessing<br/>
4. run machine_learning.py<br/>

How to use local_operators.py :<br/>
locate_object(picture_path, photo_saved_location, model_path, size, predicted_save_location)<br/>
</br>
picture_path - string <br/>
* should be saved in folder predict_set<br/>
* example : 'predict_set\\img_123.jpg'<br/>
model_path - string<br/>
* should be just 'model'<br/>
size - int<br/>
* should be size of model we trained, 128<br/>
predicted_save_location - string<br/>
* folder name of place for saving picture, should be predicted_set, or anything from where you will read it and send back to android</br>

Example call

```python
locate_object('dataset_size128\\train\\nevus\\ISIC_0012680.jpg', "predict_set", "model", 128, "predicted_set")
```



