import cv2
import numpy as np
import pandas as pd
import os
def measure_egg_size(image_path, output_folder,scale):

    x=scale[0]
    y=scale[1]
    usescale=y/x
    # Read the image
    image = cv2.imread(image_path)

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply blur 
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)

    # Use thresholding to separate eggs from background
    _, thresholded = cv2.threshold(blurred, 120, 400, cv2.THRESH_BINARY)

    # Find contours in the image
    contours, _ = cv2.findContours(thresholded, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

    area_list = []
    conotur_list=[]
    area_str=''

    # Measure the size of each contour (assumes each contour corresponds to an egg)
    for contour in contours:
        # Calculate the area of the contour
        area = cv2.contourArea(contour)


        # Filter out smaller contours (background noise)
        if 3000 < area < 4010721:  # Adjust the threshold as needed
            # Store the coordinates of the contour
            scaledarea=area*usescale
            scaledarea = round(scaledarea, 3)
            area_str=str(scaledarea)+'sq.mm'

            area_list.append(area_str)
            conotur_list.append(contour)


    for contour in conotur_list:
        cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)

    output_image_path = os.path.join(output_folder, os.path.basename(image_path).split('.')[0] + '_contours.jpg')
    cv2.imwrite(output_image_path, image)

    # Create DataFrame from lists
    measurements_df = pd.DataFrame({'Area': area_list})

    # Save measurements to Excel file
    filename = os.path.basename(image_path).split('.')[0] + '_measurements.xlsx'
    output_path = os.path.join(output_folder, filename)
    measurements_df.to_excel(output_path, index=False)

# Path to the folder containing images
input_folder = '/Users/jaeeponde/image processing/eggimages'

# Folder to save output Excel files
output_folder = '/Users/jaeeponde/image processing/egg_measurements'

#input scale in the formal of a tuple (x pixel, y mm^2)
myscale=(10000,1)
# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Iterate over each file in the input folder
for file in os.listdir(input_folder):
    if file.endswith('.jpg') or file.endswith('.png'):  # Filter only image files
        image_path = os.path.join(input_folder, file)
        measure_egg_size(image_path, output_folder,myscale)