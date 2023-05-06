import cv2
import os
import glob
import argparse
from tqdm import tqdm

# Define a function to process EACH video
def extract_frame(video_path: str, output_dir: str, n_frames_extract:int=3, temporal_stride: float=1.0, target_resolution: tuple=(512,512)):
    """
    Function to extract ONE set of n_frames from Each video, resize each frame, then save to corresponding output folder.
    Args:
      * video_path (string): path to One single input video
      * n_frames_extract (int): Number of frames that we want to extract from each video
      * temporal_stride (float): The temporal distance between frames in each set of frames in SECONDs
      * target_resolution (tuple): The target resolution that we want to resize each frame to
      * output_dir (str): Path to the output directory
    """

    # Open the video
    cap = cv2.VideoCapture(video_path)
    # Check if the video is valid
    if not cap.isOpened():
        print("Error opening video file")
        return
    
    # Calculate the length of the video
    total_num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # total number of frames in the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    length = total_num_frames / fps # length of the video in seconds
    # frame_interval = int(temporal_stride * fps) # How many frames that one temporal stride include
    
    # Check if the video is LONG ENOUGH to extract the desired number of frames
    if length < n_frames_extract * temporal_stride:
        print(f"{video_path} is too short, discarded")
        return 
    
    # Create the output directory 
    output_dir = os.path.join(output_dir, "frames_{:.2f}_seconds_interval".format(temporal_stride))
    os.makedirs(output_dir, exist_ok=True)
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(output_dir, f"{video_name}_frames")
    os.makedirs(output_path, exist_ok=True)
    
    # Extract and resize the frames
    for i in range(n_frames_extract):
        frame_idx = int(i * temporal_stride * fps) # Get index of the frame to be extracted
        # print(f"Frame index: {frame_idx}")
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx) # set the current frame position frame idx
        ret, frame = cap.read() # read the current frame
        if not ret:
            print(f"Error reading frame {frame_idx}")
            return # If ONLY ONE Frame fails to read, then Skip this video and return nothing

        # Resized the frame
        resized_frame = cv2.resize(frame, target_resolution, interpolation=cv2.INTER_AREA)
        
        # Save the frames
        frame_path = os.path.join(output_path, f"frames_{i}.jpg")
        # print(f"frame path: {frame_path}")
        cv2.imwrite(frame_path, resized_frame)

if __name__ == '__main__':
    
    # Add the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', '-i', type=str, default="downloaded_celebvhq/processed/", help="The input videos directory")
    parser.add_argument('--output_dir','-o', type=str, default="downloaded_celebvhq", help="The output directory where the frames are saved")
    parser.add_argument('--n_frames_extract', '-n', type=int, default=3, help="Number of frames to be extracted from each video")
    parser.add_argument('--interval', type=float, default=1.0, help="The temporal stride, or temporal distance between extracted frames")
    parser.add_argument('--size', '-s', type=tuple, default=(512, 512), help="The target resolution for resized frames")
    args = parser.parse_args()    
        

    # output_dir = "downloaded_celebvhq/frames_{:.2f}_seconds_interval".format(args.interval)
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir, exist_ok=True)

    # Loop through all video in the input direcotory to extract frames:
    for video in tqdm(glob.glob(args.input_dir + '/*.mp4')):
        extract_frame(video, args.output_dir, args.n_frames_extract, args.interval, args.size)
        
        
        
        
        
        

    