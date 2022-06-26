import pandas as pd
import os, shutil
import random
from PIL import Image
import cv2
import glob
import csv
import splitfolders
"""
#read the metadata csv file
metadata = pd.read_csv("C:/Users/ΣΠΥΡΟΣ ΒΟΛΛΑΣ/Documents/HAM10000_metadata")
#view the data format inside the csv file
print(metadata.head())  
#print all label names of dataset
print(metadata["dx"].value_counts()) 


#path of original data
dataset = "C:/HAM10000_all_images"
#path where the subfolders containing the data according their label will be created
target = "C:/HAM10000_categories"

#create a list containing the names of data labels
class_names = metadata["dx"].unique().tolist()
label_images = []

#divide images into seven subfolders according their label
for i in class_names:
    destination = "C:/HAM10000_categories/" + i
    os.makedirs(destination)
    sample = metadata[metadata["dx"]==i]["image_id"]
    label_images.extend(sample)
    for c in label_images : 
        get_image = "C:/HAM10000_all_images/" + c + ".jpg" 
        move_image_to_category = shutil.move(get_image, destination)
    label_images = []

#paths of the subfolders previously created 
path1 = "C:/HAM10000_categories/akiec/"
path2 = "C:/HAM10000_categories/bcc/"
path3 = "C:/HAM10000_categories/bkl/"
path4 = "C:/HAM10000_categories/df/"
path5 = "C:/HAM10000_categories/mel/"
path6 = "C:/HAM10000_categories/nv/"
path7 = "C:/HAM10000_categories/vasc/"

#change the size of the images
dirs = os.listdir(path7)

def resize():
    for item in dirs:
        if os.path.isfile(path7+item):
            im = Image.open(path7+item)
            f, e = os.path.splitext(path7+item)
            imResize = im.resize((100,75), Image.ANTIALIAS)
            imResize.save(f + ' resized.jpg', 'JPEG', quality=90)
            os.remove(path7+item)

resize()

#downsample class nv
files1 = os.listdir(path6)  # Get filenames in current folder
files1 = random.sample(files1, 3352)  # Pick random images equal to 50% of class data
for file in files1:  # Go over each file name to be deleted
    f = os.path.join(path6, file)  # Create valid path to file
    os.remove(f)  # Remove the file

#upsample class mel
os.chdir(path5)
for file in glob.glob("*.jpg"):
    for angle in (120 , 240):
        image = Image.open(file)
        image_rot = image.rotate(angle)
        image_rot.save(file.replace(".jpg", "_r{0}.jpg".format(angle))) 

#upsample class bkl    
os.chdir(path3)
for file in glob.glob("*.jpg"):
    for angle in (120 , 240):
        image = Image.open(file)
        image_rot = image.rotate(angle)
        image_rot.save(file.replace(".jpg", "_r{0}.jpg".format(angle))) 

#upsample class bcc
#os.chdir(path2)
#for file in glob.glob("*.jpg"):
#    for angle in (90 , 180):
#        image = Image.open(file)
#        image_rot = image.rotate(angle)
#        image_rot.save(file.replace(".jpg", "_r{0}.jpg".format(angle))) 

for image in os.listdir("C:/bcc/"):
    im = cv2.imread("C:/bcc/"+image)
    vertical_flip = cv2.flip(im,0)  
    cv2.imwrite("C:/bcc/" + image + "_VerticalFlip" + ".jpg",vertical_flip) 

#upsample class akiec
#os.chdir(path1)
#for file in glob.glob("*.jpg"):
#    for angle in (90, 180, 270):
#        image = Image.open(file)
#        image_rot = image.rotate(angle)
#        image_rot.save(file.replace(".jpg", "_r{0}.jpg".format(angle)))

for image in os.listdir("C:/akiec/"):
    im = cv2.imread("C:/akiec/"+image)
    vertical_flip = cv2.flip(im,0)  
    cv2.imwrite("C:/akiec/" + image + "_VerticalFlip" + ".jpg",vertical_flip)

#upsample class df
os.chdir(path4)
for file in glob.glob("*.jpg"):
    for angle in (45, 90, 135, 180, 225, 270, 315):
        image = Image.open(file)
        image_rot = image.rotate(angle)
        image_rot.save(file.replace(".jpg", "_r{0}.jpg".format(angle)))

#upsample class vasc
os.chdir(path7)
for file in glob.glob("*.jpg"):
    for angle in (45, 90, 135, 180, 225, 270, 315):
        image = Image.open(file)
        image_rot = image.rotate(angle)
        image_rot.save(file.replace(".jpg", "_r{0}.jpg".format(angle)))

#split dataset into train and validation
input_folder = "C:/HAM10000_categories/"
splitfolders.ratio(input_folder, output = "C:/split folder", ratio = (.8, .2), group_prefix=None)

path8 = "C:/split folder/train/akiec/"
path9 = "C:/split folder/train/bcc/"
path10 = "C:/split folder/train/bkl/"
path11 = "C:/split folder/train/df/"
path12 = "C:/split folder/train/mel/"
path13 = "C:/split folder/train/nv/"
path14 = "C:/split folder/train/vasc/"

#write a new csv file with the metadata of train dataset
with open('train_metadata2.csv', 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['Image ID', 'Class'])
    for filename in os.listdir(path8):
        writer.writerow([filename, 'akiec'])
    for filename in os.listdir(path9):
        writer.writerow([filename, 'bcc'])
    for filename in os.listdir(path10):
        writer.writerow([filename, 'bkl'])
    for filename in os.listdir(path11):
        writer.writerow([filename, 'df'])
    for filename in os.listdir(path12):
        writer.writerow([filename, 'mel'])
    for filename in os.listdir(path13):
        writer.writerow([filename, 'nv'])
    for filename in os.listdir(path14):
        writer.writerow([filename, 'vasc'])

path15 = "C:/split folder/val/akiec/"
path16 = "C:/split folder/val/bcc/"
path17 = "C:/split folder/val/bkl/"
path18 = "C:/split folder/val/df/"
path19 = "C:/split folder/val/mel/"
path20 = "C:/split folder/val/nv/"
path21 = "C:/split folder/val/vasc/"

#write a new csv file with the metadata of train dataset
with open('test_metadata2.csv', 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['Image ID', 'Class'])
    for filename in os.listdir(path15):
        writer.writerow([filename, 'akiec'])
    for filename in os.listdir(path16):
        writer.writerow([filename, 'bcc'])
    for filename in os.listdir(path17):
        writer.writerow([filename, 'bkl'])
    for filename in os.listdir(path18):
        writer.writerow([filename, 'df'])
    for filename in os.listdir(path19):
        writer.writerow([filename, 'mel'])
    for filename in os.listdir(path20):
        writer.writerow([filename, 'nv'])
    for filename in os.listdir(path21):
        writer.writerow([filename, 'vasc'])
"""