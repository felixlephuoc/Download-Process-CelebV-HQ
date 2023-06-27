import cv2
import os
import glob
import argparse
import multiprocessing
from tqdm import tqdm

def extract_frame(video_path: str, output_dir: str, n_frames_extract:int=3, temporal_stride: float=1.0, target_resolution: tuple=(512,512)):
    """
    Extract one set of n_frames from each video.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file")
        return
    
    # Calculate the length of the video
    total_num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    length = total_num_frames / fps
    
    if length < n_frames_extract * temporal_stride:
        print(f"{video_path} is too short, discarded")
        return 
    
    # Create the output directory 
    output_dir = os.path.join(output_dir, "celebvhq_{}_frames_{:.1f}_seconds_interval_{}".format(n_frames_extract, temporal_stride, target_resolution[0]))
    os.makedirs(output_dir, exist_ok=True)
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(output_dir, f"{video_name}_frames")
    os.makedirs(output_path, exist_ok=True)
    
    # Extract and resize the frames
    for i in range(n_frames_extract):
        frame_idx = int(i * temporal_stride * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx) 
        ret, frame = cap.read()
        if not ret:
            print(f"Error reading frame {frame_idx}")
            return 

        # Resize
        resized_frame = cv2.resize(frame, target_resolution, interpolation=cv2.INTER_AREA)
        
        frame_path = os.path.join(output_path, f"frames_{i}.png")
        cv2.imwrite(frame_path, resized_frame)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', '-i', type=str, default="downloaded_celebvhq/processed/", help="The input videos directory")
    parser.add_argument('--output_dir','-o', type=str, default="celebvhq_frames", help="The output directory where the frames are saved")
    parser.add_argument('--n_frames', '-n', type=int, default=3, help="Number of frames to be extracted from each video")
    parser.add_argument('--interval', type=float, default=1.0, help="The temporal stride, or temporal distance between extracted frames")
    parser.add_argument('--size', '-s', type=int, default=512, help="The target resolution for resized frames")
    # parser.add_argument('--n_workers', type=int, default=4, help="Number of workers")
    args = parser.parse_args()    
        

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir, exist_ok=True)

    for video in tqdm(glob.glob(args.input_dir + '/*.mp4')):
        extract_frame(video, args.output_dir, args.n_frames, args.interval, (args.size, args.size))
     
    
    
        

        
        
        
        
        
        

    