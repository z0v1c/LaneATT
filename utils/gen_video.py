import pickle
import argparse
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import cv2
import numpy as np
from tqdm import tqdm

from lib.config import Config


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--pred", required=True)
    p.add_argument("--cfg", required=True)
    p.add_argument("--out", default="video.mp4")
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--legend")
    p.add_argument("--view", action="store_true")
    p.add_argument("--show_fps", action="store_true")
    p.add_argument("--fps_data", default="fps_data.pkl")
    return p.parse_args()


def draw_fps(img, fps, pos=(10, 30)):
    text = f"FPS: {fps:.1f}"
    (w, h), b = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)

    cv2.rectangle(img, (pos[0]-5, pos[1]-h-5),
                  (pos[0]+w+5, pos[1]+b+5), (0,0,0), -1)

    cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0,255,0), 2, cv2.LINE_AA)
    return img


def main():
    args = parse_args()
    cfg = Config(args.cfg)

    print("📂 Loading dataset...")
    dataset = cfg.get_dataset("test")

    h, w = cfg["datasets"]["test"]["parameters"]["img_size"]
    print(f"Resolution: {w}x{h}")

    # --- Load predictions ---
    print("📥 Loading predictions...")
    with open(args.pred, "rb") as f:
        predictions = pickle.load(f)

    # Ensure predictions is a list
    if isinstance(predictions, np.ndarray):
        predictions = predictions.tolist()

    print(f"Loaded {len(predictions)} predictions.")

    # --- Load FPS data ---
    fps_vals = None
    if args.show_fps:
        if os.path.exists(args.fps_data):
            print("📥 Loading FPS data...")
            with open(args.fps_data, "rb") as f:
                fps_vals = pickle.load(f)
            print(f"FPS frames: {len(fps_vals)} (avg={np.mean(fps_vals):.2f})")
        else:
            print("⚠️ FPS file missing, disabling overlay.")
            args.show_fps = False

    # --- Create Video Writer ---
    out = args.out
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(out, fourcc, args.fps, (w, h))

    print("🎥 Generating video...")

    for idx in tqdm(range(len(dataset))):
        frame, _, _ = dataset.draw_annotation(idx, pred=predictions[idx])

        if args.show_fps and fps_vals and idx < len(fps_vals):
            frame = draw_fps(frame, fps_vals[idx])

        video.write(frame)

    video.release()
    print(f"✅ Video saved to: {out}")


if __name__ == "__main__":
    main()
