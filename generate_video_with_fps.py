import argparse
import subprocess
import os
import sys


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp_name", required=True)
    parser.add_argument("--out", default="output_video.mp4")
    parser.add_argument("--fps", type=int, default=30)
    return parser.parse_args()


def main():
    args = parse_args()

    exp_dir = os.path.join("experiments", args.exp_name)
    pred_path = os.path.join(exp_dir, "predictions.pkl")
    cfg_path = os.path.join(exp_dir, "config.yaml")
    fps_path = os.path.join(exp_dir, "fps_data.pkl")

    # Error checks
    if not os.path.exists(pred_path):
        print(f"❌ ERROR: Predictions file missing: {pred_path}")
        print("Run inference with:\n  python main.py test --exp_name {} --save_predictions".format(args.exp_name))
        return

    if not os.path.exists(fps_path):
        print(f"❌ ERROR: FPS log missing: {fps_path}")
        print("Run inference (patched eval) to generate fps_data.pkl")
        return

    python_exe = sys.executable  # Correct Python (conda env)

    cmd = f"\"{python_exe}\" utils/gen_video.py --pred \"{pred_path}\" --cfg \"{cfg_path}\" --out \"{args.out}\" --fps {args.fps} --show_fps --fps_data \"{fps_path}\""

    print("\n🚀 Running video generator:")
    print(cmd + "\n")

    subprocess.run(cmd, shell=True, check=True)


if __name__ == "__main__":
    main()
