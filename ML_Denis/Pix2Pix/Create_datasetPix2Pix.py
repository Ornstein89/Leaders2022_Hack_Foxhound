import tensorflow as tf

import os 
import pathlib
import time 
import datetime

from matplotlib import pyplot as plt
from IPython import display
import SimpleITK as sitk
import numpy as np
import cv2

train_covid_path = "E:\\GitHub\\Covid_GAN\\COVID_TrainData\\train"
valid_covid_path = "E:\\GitHub\\Covid_GAN\\COVID_TrainData\\validate"

# Lungs
train_lungs_path = "E:\\GitHub\\Covid_GAN\\LUNGS_TrainData\\train"
valid_lungs_path = "E:\\GitHub\\Covid_GAN\\LUNGS_TrainData\\validate"

# Список файлов в дерикториях 
# Covid
list_train_covid_items = os.listdir(train_covid_path)
list_valid_covid_items = os.listdir(valid_covid_path)

# Lungs
list_train_lungs_items = os.listdir(train_lungs_path)
list_valid_lungs_items = os.listdir(valid_lungs_path)

# Разделение изображений и масок 
# Тренировочный
list_train_image = [item for item in list_train_covid_items if item[-11:] == "_img.nii.gz" ]
list_train_mask = [item for item in list_train_covid_items if item[-12:] == "_mask.nii.gz" ]
# валидационный 
list_valid_image = [item for item in list_valid_covid_items if item[-11:] == "_img.nii.gz" ]
list_valid_mask = [item for item in list_valid_covid_items if item[-12:] == "_mask.nii.gz" ]


def normalize(x):
    min_in = np.min(x)
    max_in = np.max(x)
    return (x - min_in) / (max_in - min_in + 1e-8)

count_train = 0
count_valid = 0
save_train_path = "E:\\GitHub\\Covid_GAN\\DataSetInpainting\\train\\"
save_valid_path = "E:\\GitHub\\Covid_GAN\\DataSetInpainting\\valid\\"
# получение кадров исследования train 
for item_number in range(len(list_train_image)-1):

    print(os.path.join(train_covid_path, list_train_image[item_number]))
    print(os.path.join(train_covid_path, list_train_mask[item_number]))
    print(os.path.join(train_lungs_path, list_train_lungs_items[item_number]))

    # Чтение данных
    images_items = sitk.ReadImage(os.path.join(train_covid_path, list_train_image[item_number]))
    mask_items = sitk.ReadImage(os.path.join(train_covid_path, list_train_mask[item_number]))
    lungs_items = sitk.ReadImage(os.path.join(train_lungs_path, list_train_lungs_items[item_number]))
    
    #  перевод в массив
    images_array = sitk.GetArrayFromImage(images_items)
    mask_array = sitk.GetArrayFromImage(mask_items)
    lungs_array = sitk.GetArrayFromImage(lungs_items)


    
    # изменение типа
    images_array = normalize(images_array.astype(np.int64))
    mask_array = mask_array.astype(np.float64)
    lungs_array = lungs_array.astype(np.uint8)

    print("images_array", images_array.shape)
    print("mask_array", mask_array.shape)
    print("lungs_array", lungs_array.shape)
    
    
    
    for number in range(len(images_array)-1):

        # проверка на не пустую маску 
        if len(mask_array[number,:,:].nonzero()[0]) > 0 or len(mask_array[number,:,:].nonzero()[1])>1:

            # cv2.imshow("main", images_array[number])
            # cv2.waitKey(0)
        
            # вырезание болячки по маске 
            lungs_image = cv2.bitwise_and(images_array[number,:,:], images_array[number,:,:],mask = lungs_array[number,:,:])
            lungs_image = lungs_image.astype(np.float64)

            # cv2.imshow("main", lungs_image)
            # cv2.waitKey(0)
            
            # Добавление 3-го измерения 
            mask_array_rgb = np.expand_dims(mask_array[number,:,:], axis = 2)
            ones_array = np.zeros((512,512,1))
            mask_array_rgb = np.dstack((ones_array,mask_array_rgb*255,ones_array))
            
            lungs_image = np.expand_dims(lungs_image, axis = 2)
            lungs_image = np.dstack((lungs_image,lungs_image,lungs_image))
            
            result = cv2.add(lungs_image,mask_array_rgb)
            
            # cv2.imshow("main", result)
            # cv2.waitKey(0)
            
            # # изменение размеров 
            result = cv2.resize(result, (512, 512), cv2.INTER_CUBIC)
            lungs_image = cv2.resize(lungs_image, (512, 512), cv2.INTER_CUBIC)

            result = np.hstack((lungs_image,result))
            
            cv2.imwrite(save_train_path+f'{count_train}.jpg',result*255)
            count_train +=1
        
    # --------------<Отладка>-------------
    # print(result.dtype)
    # print(images_array[30,:,:].shape)
    # print(result.shape)
    # fig, axes = plt.subplots(1, 3)
    # axes[0].imshow(images_array[number,:,:],cmap='gray')
    # axes[1].imshow(mask_array[number,:,:],cmap='gray')
    # axes[2].imshow(result,cmap='gray')
    # fig.set_figwidth(12)    #  ширина и
    # fig.set_figheight(6)    #  высота "Figure"
    # plt.show()
    
# получение кадров исследования valid 

for item_number in range(len(list_valid_image)-1):

    print(os.path.join(valid_covid_path, list_valid_image[item_number]))
    print(os.path.join(valid_covid_path, list_valid_mask[item_number]))
    print(os.path.join(valid_lungs_path, list_valid_lungs_items[item_number]))

    # Чтение данных
    images_items = sitk.ReadImage(os.path.join(valid_covid_path, list_valid_image[item_number]))
    mask_items = sitk.ReadImage(os.path.join(valid_covid_path, list_valid_mask[item_number]))
    lungs_items = sitk.ReadImage(os.path.join(valid_lungs_path, list_valid_lungs_items[item_number]))
    
    #  перевод в массив
    images_array = sitk.GetArrayFromImage(images_items)
    mask_array = sitk.GetArrayFromImage(mask_items)
    lungs_array = sitk.GetArrayFromImage(lungs_items)


    
    # изменение типа
    images_array = normalize(images_array.astype(np.int64))
    mask_array = mask_array.astype(np.float64)
    lungs_array = lungs_array.astype(np.uint8)

    print("images_array", images_array.shape)
    print("mask_array", mask_array.shape)
    print("lungs_array", lungs_array.shape)
    
    
    
    for number in range(len(images_array)-1):

        # проверка на не пустую маску 
        if len(mask_array[number,:,:].nonzero()[0]) > 0 or len(mask_array[number,:,:].nonzero()[1])>1:

            # cv2.imshow("main", images_array[number])
            # cv2.waitKey(0)
        
            # вырезание болячки по маске 
            lungs_image = cv2.bitwise_and(images_array[number,:,:], images_array[number,:,:],mask = lungs_array[number,:,:])
            lungs_image = lungs_image.astype(np.float64)

            # cv2.imshow("main", lungs_image)
            # cv2.waitKey(0)
            
            # Добавление 3-го измерения 
            mask_array_rgb = np.expand_dims(mask_array[number,:,:], axis = 2)
            ones_array = np.zeros((512,512,1))
            mask_array_rgb = np.dstack((ones_array,mask_array_rgb*255,ones_array))
            
            lungs_image = np.expand_dims(lungs_image, axis = 2)
            lungs_image = np.dstack((lungs_image,lungs_image,lungs_image))
            
            result = cv2.add(lungs_image,mask_array_rgb)
            
            # cv2.imshow("main", result)
            # cv2.waitKey(0)
            
            # # изменение размеров 
            result = cv2.resize(result, (512, 512), cv2.INTER_CUBIC)
            lungs_image = cv2.resize(lungs_image, (512, 512), cv2.INTER_CUBIC)

            result = np.hstack((lungs_image,result))
            
            cv2.imwrite(save_valid_path+f'{count_valid}.jpg',result*255)
            count_valid +=1