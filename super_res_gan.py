import os

import cv2
import torch
from torch import nn

import SRGAN.imgproc as imgproc
import SRGAN.model as model
from SRGAN.utils import load_state_dict

model_names = sorted(
    name for name in model.__dict__ if
    name.islower() and not name.startswith("__") and callable(model.__dict__[name]))


def choice_device(device_type: str) -> torch.device:
    # Select model processing equipment type
    if device_type == "cuda":
        device = torch.device("cuda", 0)
    else:
        device = torch.device("cpu")
    return device


def build_model(model_arch_name: str, device: torch.device) -> nn.Module:
    # Initialize the super-resolution model
    sr_model = model.__dict__[model_arch_name](in_channels=3,
                                               out_channels=3,
                                               channels=64,
                                               num_rcb=16)
    sr_model = sr_model.to(device=device)

    return sr_model


device = choice_device('cpu')

# Initialize the model
sr_model = build_model('srresnet_x4', device)

# Load model weights
sr_model = load_state_dict(
    sr_model, 'SRGAN/results/pretrained_models/SRGAN_x4-ImageNet-8c4a7569.pth.tar')
# Start the verification mode of the model.
sr_model.eval()


def main(image):
    image = cv2.imread(image)

    lr_tensor = imgproc.preprocess_one_image(image, device)

    # Use the model to generate super-resolved images
    with torch.no_grad():
        sr_tensor = sr_model(lr_tensor)

    # Save image
    sr_image = imgproc.tensor_to_image(sr_tensor, False, False)
    sr_image = cv2.cvtColor(sr_image, cv2.COLOR_RGB2BGR)
    sr_image = cv2.cvtColor(sr_image, cv2.COLOR_BGR2RGB)

    return sr_image
