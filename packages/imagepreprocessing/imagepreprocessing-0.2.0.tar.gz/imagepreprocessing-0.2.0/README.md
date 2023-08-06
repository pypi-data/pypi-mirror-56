## imagepreprocessing

- **Creates train ready data for keras or yolo in a single line**
- **Makes prediction with using keras model in a single line**

## Install

```sh
pip install imagepreprocessing
```

## Usage

```python
from imagepreprocessing import create_training_data_keras, create_training_data_yolo, create_only_path_files_yolo, make_prediction
```

## Create training data for keras

```python
source_path = "datasets/deep_learning/food-101/only3"
save_path = "food10class1000sampleeach"
create_training_data(source_path, save_path, img_size = 299, validation_split=0.1, percent_to_use=0.1, grayscale = True, files_to_exclude=["excludemoe","hi.txt"])
```
```
File name: apple_pie - 1/3  Image:100/100
File name: baby_back_ribs - 2/3  Image:100/100
File name: baklava - 3/3  Image:100/100

validation x: 30 validation y: 30
train x: 270 train y: 270

shape of train x: (270, 299, 299, 1)
shape of train y: (270, 3)
shape of validate x: (30, 299, 299, 1)
shape of validate y: (30, 3)

file saved -> C:\Users\can\Desktop\food3class100sampleeach_x_train.pkl
file saved -> C:\Users\can\Desktop\food3class100sampleeach_y_train.pkl
file saved -> C:\Users\can\Desktop\food3class100sampleeach_x_validation.pkl
file saved -> C:\Users\can\Desktop\food3class100sampleeach_y_validation.pkl
```

## Make prediction with a keras model

```python
images_path = "deep_learning/test_images/food2"
model_path = "deep_learning/saved_models/alexnet.h5"

make_prediction(images_path, model_path)
```
```
1.jpg : 0
2.jpg : 0
3.jpg : 0
4.jpg : 1
5.jpg : 1
6.jpg : 2
7.jpg : 2
8.jpg : 2
9.jpg : 1
```
