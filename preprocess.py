#!/usr/bin/env python3
import os
import re

from scipy import misc

IMAGE_SIZE = 48
GREYSCALE = True
RELOAD_IMAGES = True

datasets = [
    {
        'name': 'full_dataset',
        'classes': None,
        'images_per_class': None,
        'train_test_same': False,
    },
    {
        'name': 'micro_dataset',
        'classes': 4,
        'images_per_class': 5,
        'train_test_same': True,
    },
]

image_dir = os.path.join('data', 'raw', 'JPEGImages')
split_dir = os.path.join('data', 'raw', 'ImageSplits')
processed_dir = os.path.join('data', 'processed')
datasets_dir = os.path.join('data', 'datasets')


def naive_square(array, target_size):
    """Scales and crops an array to a centered square"""
    shorter = min(array.shape)
    scale = float(target_size / shorter)
    scaled = misc.imresize(array, scale)
    landscape = (array.shape[0] == shorter)
    diff = max(scaled.shape) - min(scaled.shape)
    if diff == 0:
        return scaled
    margin_one = diff // 2
    margin_two = margin_one if diff % 2 == 0 else margin_one + 1
    if landscape:
        return scaled[:, margin_one:-margin_two]
    else:
        return scaled[margin_one:-margin_two, :]


def get_label(name):
    label_regex = '(\w+)_\d+.jpg'
    match = re.match(label_regex, name)
    return match.group(1)


if RELOAD_IMAGES:
    image_names = os.listdir(image_dir)
    image_arrays, names = [], []
    for image_name in image_names:
        print('Processing {}...'.format(image_name))
        input_path = os.path.join(image_dir, image_name)
        output_path = os.path.join(processed_dir, image_name)
        image_array = misc.imread(input_path, flatten=GREYSCALE)
        square_array = naive_square(image_array, IMAGE_SIZE)
        image_arrays.append(square_array)
        names.append(image_name)
        misc.imsave(output_path, square_array)

print('Loading image splits...')
split_names = os.listdir(split_dir)
train_set, test_set = ([], []), ([], [])
for split_name in split_names:
    if 'train' in split_name:
        current_set = train_set
    elif 'test' in split_name:
        curent_set = test_set
    else:
        continue
    split_path = os.path.join(split_dir, split_name)
    with open(split_path) as f:
        lines = f.read().splitlines()
    for image_name in lines:
        image_path = os.path.join(processed_dir, image_name)
        image = misc.imread(image_path)
        current_set[0].append(image)
        label = get_label(image_name)
        current_set[1].append(label)

print(train_set)
print(test_set)

for dataset in datasets:
    print('Forming {}...'.format(dataset['name']))
    pass
