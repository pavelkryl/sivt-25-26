#!/bin/bash
. .venv/bin/activate

pip install --upgrade pip

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

pip install pillow huggingface_hub ultralytics
