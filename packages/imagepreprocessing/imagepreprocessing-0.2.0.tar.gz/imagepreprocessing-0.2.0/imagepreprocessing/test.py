from imagepreprocessing import create_training_data_keras,create_training_data_yolo, create_only_path_files_yolo, make_prediction


source_path = "C:\\Users\\can\\datasets\\deep_learning\\food-101\\only3"
save_path = "C:\\Users\\can\\Desktop\\food10class100sampleeach"

images_path = "C:\\Users\\can\\PythonProjects2\\deep_learning\\test_images\\food2"
model_path = "C:\\Users\\can\\PythonProjects2\\deep_learning\\saved_models\\a.h5"


# create_training_data_keras(source_path, save_path, validation_split=0.2, percent_to_use=0.1)

# create_training_data_yolo(source_path, rename_duplicates=True, validation_split = 0.2)

create_only_path_files_yolo(source_path, percent_to_use=0.1,validation_split = 0.3)

# make_prediction(images_path, model_path)

