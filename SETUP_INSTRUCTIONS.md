# LaneATT Setup Instructions for RTX 5070 Ti (CUDA 12.8)

This guide will help you set up LaneATT to work with your NVIDIA GeForce RTX 5070 Ti GPU.

## Prerequisites
- Windows 10/11
- CUDA 12.8 installed
- Visual Studio Build Tools (for compiling NMS module)

## Step-by-Step Setup

### 1. Install Python 3.12
```powershell
winget install Python.Python.3.12
```

### 2. Uninstall old PyTorch (if any)
```powershell
py -3.12 -m pip uninstall torch torchvision torchaudio -y
```

### 3. Install PyTorch with CUDA 12.8 support
```powershell
py -3.12 -m pip install -U https://huggingface.co/w-e-w/torch-2.6.0-cu128.nv/resolve/main/torch-2.6.0%2Bcu128.nv-cp312-cp312-win_amd64.whl https://huggingface.co/w-e-w/torch-2.6.0-cu128.nv/resolve/main/torchvision-0.20.0a0%2Bcu128.nv-cp312-cp312-win_amd64.whl
```

### 4. Install project requirements
```powershell
cd C:\Users\zovic\Documents\LaneATT
py -3.12 -m pip install -r requirements.txt
```

### 5. Fix NumPy compatibility (imgaug requires NumPy < 2.0)
```powershell
py -3.12 -m pip install "numpy<2.0"
```

### 6. Update NMS module to support RTX 50 series (sm_120)
The file `lib/nms/setup.py` should already have this change, but verify it includes:
```python
'-gencode=arch=compute_120,code=sm_120',  # RTX 50 series support
```

### 7. Compile NMS module
```powershell
cd lib\nms
py -3.12 setup.py install
cd ..\..
```

### 8. Fix deprecated NumPy usage
The file `lib/models/laneatt.py` line 323 should use `bool` instead of `np.bool`:
```python
# Change from: .astype(np.bool)
# To: .astype(bool)
```

### 9. Verify PyTorch recognizes your GPU
```powershell
py -3.12 -c "import torch; print('PyTorch:', torch.__version__); print('CUDA:', torch.version.cuda); print('Available:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"
```

Expected output:
- PyTorch: 2.6.0+cu128.nv
- CUDA: 12.8
- Available: True
- Device: NVIDIA GeForce RTX 5070 Ti

### 10. Run CULane test
```powershell
cd C:\Users\zovic\Documents\LaneATT
py -3.12 main.py test --exp_name laneatt_r34_culane
```

## Quick Reference - All Commands in Order

```powershell
# Install Python 3.12
winget install Python.Python.3.12

# Navigate to project
cd C:\Users\zovic\Documents\LaneATT

# Install PyTorch with CUDA 12.8
py -3.12 -m pip uninstall torch torchvision torchaudio -y
py -3.12 -m pip install -U https://huggingface.co/w-e-w/torch-2.6.0-cu128.nv/resolve/main/torch-2.6.0%2Bcu128.nv-cp312-cp312-win_amd64.whl https://huggingface.co/w-e-w/torch-2.6.0-cu128.nv/resolve/main/torchvision-0.20.0a0%2Bcu128.nv-cp312-cp312-win_amd64.whl

# Install requirements
py -3.12 -m pip install -r requirements.txt

# Fix NumPy version
py -3.12 -m pip install "numpy<2.0"

# Compile NMS module
cd lib\nms
py -3.12 setup.py install
cd ..\..

# Run test
py -3.12 main.py test --exp_name laneatt_r34_culane
```

## Notes

- Always use `py -3.12` to ensure you're using Python 3.12
- The NMS module has been updated to support sm_120 (RTX 50 series)
- The code fix for `np.bool` → `bool` has been applied to `lib/models/laneatt.py`
- Make sure your CULane dataset is downloaded and set up in `datasets/culane/`

## Available Models

You can test any of these pretrained models:
- `laneatt_r18_culane` - ResNet-18 on CULane
- `laneatt_r34_culane` - ResNet-34 on CULane (recommended)
- `laneatt_r122_culane` - ResNet-122 on CULane
- `laneatt_r18_tusimple` - ResNet-18 on TuSimple
- `laneatt_r34_tusimple` - ResNet-34 on TuSimple
- `laneatt_r122_tusimple` - ResNet-122 on TuSimple
- `laneatt_r18_llamas` - ResNet-18 on LLAMAS
- `laneatt_r34_llamas` - ResNet-34 on LLAMAS
- `laneatt_r122_llamas` - ResNet-122 on LLAMAS

## With Visualization

To see the predictions visually:
```powershell
py -3.12 main.py test --exp_name laneatt_r34_culane --view all
```

