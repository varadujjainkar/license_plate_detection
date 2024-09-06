# parse_annotations.py
import os
import xml.etree.ElementTree as ET
import pandas as pd

# Define paths
annotations_path = 'data/positive/annotations/'
images_path = 'data/positive/images/'
output_csv_path = 'data/annotations.csv'

# Parse XML files and create a CSV with image paths and bounding boxes
def parse_xml_annotations(annotations_path, images_path):
    data = []
    
    for xml_file in os.listdir(annotations_path):
        if xml_file.endswith('.xml'):
            xml_path = os.path.join(annotations_path, xml_file)
            tree = ET.parse(xml_path)
            root = tree.getroot()

            image_file = root.find('filename').text
            image_path = os.path.join(images_path, image_file)
            if not os.path.exists(image_path):
                continue

            for obj in root.findall('object'):
                label = obj.find('name').text
                bbox = obj.find('bndbox')
                xmin = int(bbox.find('xmin').text)
                ymin = int(bbox.find('ymin').text)
                xmax = int(bbox.find('xmax').text)
                ymax = int(bbox.find('ymax').text)
                data.append([image_path, xmin, ymin, xmax, ymax, label])

    df = pd.DataFrame(data, columns=['image_path', 'xmin', 'ymin', 'xmax', 'ymax', 'label'])
    df.to_csv(output_csv_path, index=False)

parse_xml_annotations(annotations_path, images_path)
