# Video Generation with FPS Overlay

This guide explains how to generate videos from your lane detection results with FPS counters overlaid on each frame.

## Overview

The system now tracks FPS (frames per second) for each frame during inference and can overlay this information on the generated video. This is useful for analyzing performance, especially to see if FPS drops in certain scenarios like highways.

## Step-by-Step Instructions

### Step 1: Run Inference and Save Predictions

First, run your model on the test dataset and save the predictions along with FPS data:

```bash
py -3.12 main.py test --exp_name laneatt_r34_culane --save_predictions
```

This will create two files:
- `predictions.pkl` - Contains all the lane predictions
- `fps_data.pkl` - Contains FPS measurements for each frame

### Step 2: Generate Video with FPS Overlay

#### Option A: Using the Helper Script (Recommended)

```bash
py -3.12 generate_video_with_fps.py --exp_name laneatt_r34_culane --out output_video.mp4 --fps 30
```

#### Option B: Using gen_video.py Directly

```bash
py -3.12 utils/gen_video.py --pred predictions.pkl --cfg experiments/laneatt_r34_culane/config.yaml --out output_video.mp4 --fps 30 --show_fps --fps_data fps_data.pkl
```

### Step 3: View the Video

The video will be saved with:
- Lane predictions drawn on each frame
- FPS counter overlaid in the top-left corner (green text on black background)
- Original dataset images with predictions

## Command Line Options

### For `generate_video_with_fps.py`:

- `--exp_name`: Experiment name (required)
- `--out`: Output video filename (default: `output_video.mp4`)
- `--fps`: Output video FPS (default: 30)
- `--pred_file`: Path to predictions.pkl (default: `predictions.pkl`)
- `--fps_file`: Path to fps_data.pkl (default: `fps_data.pkl`)
- `--no_fps_overlay`: Don't show FPS overlay
- `--length`: Length of output video in seconds
- `--clips`: Number of clips to include

### For `utils/gen_video.py`:

- `--pred`: Path to predictions.pkl file (required)
- `--cfg`: Config file path (required)
- `--out`: Output video filename
- `--fps`: Output video FPS
- `--show_fps`: Enable FPS overlay
- `--fps_data`: Path to fps_data.pkl file
- `--length`: Length of output video in seconds
- `--clips`: Number of clips to include
- `--legend`: Path to legend image file

## Example Workflow

```bash
# 1. Run inference on CULane dataset
py -3.12 main.py test --exp_name laneatt_r34_culane --save_predictions

# 2. Generate video with FPS overlay (30 FPS output)
py -3.12 generate_video_with_fps.py --exp_name laneatt_r34_culane --out culane_results.mp4 --fps 30

# 3. Generate video for specific clips (e.g., 60 seconds, 3 clips)
py -3.12 generate_video_with_fps.py --exp_name laneatt_r34_culane --out culane_clips.mp4 --fps 30 --length 60 --clips 3
```

## Understanding the FPS Counter

- The FPS counter shows the **inference FPS** for each frame
- Higher FPS = faster processing
- Lower FPS = slower processing (may indicate complex scenes)
- The counter is displayed in green text on a black background in the top-left corner
- Format: `FPS: XX.X` (e.g., `FPS: 45.3`)

## Analyzing FPS Drops

To analyze FPS drops in specific scenarios (like highways):

1. Generate the video with FPS overlay
2. Watch the video and note timestamps where FPS drops
3. Check the corresponding frames in the dataset to understand what causes the drop
4. Common causes:
   - Complex scenes with many lanes
   - High-resolution images
   - Multiple objects in the scene
   - GPU memory constraints

## Troubleshooting

### FPS data file not found

If you see a warning about `fps_data.pkl` not found:
- Make sure you ran inference with `--save_predictions` flag
- Check that the file exists in the current directory
- You can still generate video without FPS overlay using `--no_fps_overlay`

### Video codec issues

If the video doesn't play:
- The default codec is `mp4v` which should work on most systems
- You can try changing the codec in `utils/gen_video.py` (line 36)
- Common alternatives: `XVID`, `MJPG`, `H264`

### Video file too large

- Reduce the output FPS: `--fps 15` or `--fps 10`
- Use `--length` and `--clips` to generate shorter videos
- Consider compressing the video after generation

## Technical Details

### FPS Measurement

- FPS is measured per batch during inference
- GPU synchronization is used to ensure accurate timing
- The measurement includes:
  - Image transfer to GPU
  - Model forward pass
  - Decoding predictions
  - GPU synchronization overhead

### Video Generation

- Videos are generated using OpenCV's VideoWriter
- Default codec: `mp4v`
- Resolution matches the dataset's image size
- FPS overlay is drawn using OpenCV's text rendering

## Notes

- The FPS counter shows inference FPS, not the video playback FPS
- Average FPS is logged when saving predictions
- FPS data is saved as a list matching the order of predictions
- Each frame in a batch gets the same FPS value (batch FPS / batch_size)

