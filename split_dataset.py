import os
import shutil
import random
import argparse
from tqdm import tqdm
from os.path import join, isdir, normpath


def split_dataset(root_dir, split_ratio):
    output_dir = normpath(root_dir) + '_train_val'
    train_dir = join(output_dir, 'train')
    val_dir = join(output_dir, 'val')
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    video_dirs = sorted([d for d in os.listdir(root_dir) if isdir(join(root_dir, d))])
    random.shuffle(video_dirs)
    num_train_videos = int(len(video_dirs) * split_ratio)

    for video in tqdm(video_dirs[:num_train_videos], desc="create train dataset"):
        src_dir = join(root_dir, video)
        dest_dir = join(train_dir, video)
        shutil.copytree(src_dir, dest_dir)

    for video in tqdm(video_dirs[num_train_videos:], desc="create val dataset"):
        src_dir = join(root_dir, video)
        dest_dir = join(val_dir, video)
        shutil.copytree(src_dir, dest_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split dataset into train and validation sets.')
    parser.add_argument('--root-dir', '-d', type=str, help='Path to the original dataset directory.')
    parser.add_argument('--split-ratio', '-r', type=float, default=0.9, help='Ratio of train/validation split (default: 0.9).')

    args = parser.parse_args()
    split_dataset(args.root_dir, args.split_ratio)
