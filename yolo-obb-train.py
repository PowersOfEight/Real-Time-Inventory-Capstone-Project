from ultralytics import YOLO
import torch
import cv2
import numpy as np
import multiprocessing


def train_your_model():
    model = YOLO("yolov8n-obb.pt")
    model.train(data = "data.yaml", epochs = 50, device = 0)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    train_your_model()