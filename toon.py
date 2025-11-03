import cv2
import streamlit as st
import numpy as np
from io import BytesIO
from PIL import Image, ImageFilter,ImageEnhance, ImageOps
import torch
from torchvision import transforms
import torch.nn as nn
import torch.nn.functional as F
import re
import os
import sys
from urllib.request import urlopen



# -----------------------
# PENCIL SKETCH
# ------------------------

def pencilSketch(imgUrl):
    # Load image
    img = cv2.imread(imgUrl)
    if img is None:
        raise ValueError("Error: Image not found or path is incorrect.")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Reduce noise and smooth (helps make cleaner edges)
    gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect edges using Laplacian (you can also try Canny)
    edges = cv2.Laplacian(gray_blur, cv2.CV_8U, ksize=5)

    # Invert the edges to look like pencil outlines
    inverted = cv2.bitwise_not(edges)

    # Optional: make it more sketchy (slightly blur)
    sketch = cv2.GaussianBlur(inverted, (3, 3), 0)

    return sketch
    
# -----------------------
# OIL PAINTING
# ------------------------
        
def oilPainting(imgUrl):
    img = Image.open(imgUrl).convert("RGB")

    # Step 1: Smooth details (simulate brush blending)
    smooth = img.filter(ImageFilter.ModeFilter(size=5))  # slightly smaller to preserve details

    # Step 2: Create soft brushstroke texture
    gray = ImageOps.grayscale(smooth)
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edges_blur = edges.filter(ImageFilter.GaussianBlur(radius=1.5))  # less blur

    # Step 3: Enhance colors for painterly vibes
    enhancer = ImageEnhance.Color(smooth)
    colored = enhancer.enhance(1.5)

    contrast = ImageEnhance.Contrast(colored)
    colored = contrast.enhance(1.2)

    brightness = ImageEnhance.Brightness(colored)
    colored = brightness.enhance(1.05)

    # Step 4: Blend edge texture into colored image
    oil_paint = Image.blend(colored, edges_blur.convert("RGB"), alpha=0.3)

    # Step 5: Optional posterize for painting feel
    oil_paint = ImageOps.posterize(oil_paint, bits=5)

    # Step 6: Final sharpening to improve clarity
    oil_paint = oil_paint.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    
    # Display or return
    return oil_paint
    
# -----------------------
# COLORED SKETCH
# ------------------------
    
# def coloredSketch(img_path: str) -> Image.Image:
def coloredSketch(img_path: str) -> Image.Image:


    # Step 1: Load image
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Image not found at {img_path}")
    
    # Convert to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Step 1: Smooth image while preserving edges
    img_smooth = cv2.bilateralFilter(img_rgb, d=9, sigmaColor=75, sigmaSpace=75)
    
    # Step 2: Convert to grayscale
    img_gray = cv2.cvtColor(img_smooth, cv2.COLOR_RGB2GRAY)
    
    # Step 3: Invert grayscale
    img_invert = cv2.bitwise_not(img_gray)
    
    # Step 4: Blur the inverted image
    img_blur = cv2.GaussianBlur(img_invert, (21, 21), 0)
    
    # Step 5: Invert the blurred image
    img_blur_invert = cv2.bitwise_not(img_blur)
    
    # Step 6: Create pencil sketch
    img_sketch = cv2.divide(img_gray, img_blur_invert, scale=256.0)
    
    # Step 7: Convert sketch back to color
    img_colored = cv2.merge((img_sketch, img_sketch, img_sketch))
    
    # Step 8: Blend sketch with original image
    blended = cv2.addWeighted(img_rgb, 0.6, img_colored, 0.4, 0)
    
    # Step 9: Enhance colors (increase saturation and contrast)
    hsv = cv2.cvtColor(blended, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)
    
    # Increase saturation and brightness
    s = np.clip(s * 1.5, 0, 255).astype(np.uint8)  # stronger colors
    v = np.clip(v * 1.1, 0, 255).astype(np.uint8)  # slightly brighter
    
    hsv_enhanced = cv2.merge((h, s, v))
    final_rgb = cv2.cvtColor(hsv_enhanced, cv2.COLOR_HSV2RGB)
    
    # Convert to PIL Image
    final =  Image.fromarray(final_rgb)
    
    return final
    
# -----------------------
# CLASSIC CARTOON
# ------------------------

def classic_cartoon(img_path: str) -> Image.Image:
    # ---- Step 1: Read and validate image ----
    img_bgr = cv2.imread(img_path)
    if img_bgr is None:
        raise ValueError(f"Image not found at path: {img_path}")
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # ---- Step 2: Clean & enhance (HD clarity) ----
    # Denoise to remove pixel noise and artifacts
    denoised = cv2.fastNlMeansDenoisingColored(img_rgb, None, 10, 10, 7, 21)
    
    # Sharpen to enhance details before toonifying
    sharpen_kernel = np.array([[0, -1, 0],
                               [-1, 5, -1],
                               [0, -1, 0]])
    sharp = cv2.filter2D(denoised, -1, sharpen_kernel)

    # ---- Step 3: Smooth colors using repeated bilateral filtering ----
    color = sharp.copy()
    for _ in range(5):
        color = cv2.bilateralFilter(color, d=9, sigmaColor=75, sigmaSpace=75)

    # ---- Step 4: Detect bold edges ----
    gray = cv2.cvtColor(sharp, cv2.COLOR_RGB2GRAY)
    gray_blur = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(gray_blur, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY,
                                  blockSize=9,
                                  C=2)

    # ---- Step 5: Color quantization (flat cartoon colors) ----
    Z = color.reshape((-1, 3))
    Z = np.float32(Z)
    K = 8  # number of color clusters for quantization
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    _, labels, centers = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    quantized = centers[labels.flatten()]
    quantized = quantized.reshape(color.shape)

    # ---- Step 6: Combine quantized color with edges ----
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    cartoon = cv2.bitwise_and(quantized, edges_colored)

    # ---- Step 7: Return cartoon image as PIL Image ----
    cartoon_pil = Image.fromarray(cartoon)
    # return cartoon_pil
    return cartoon_pil
    

# -----------------------
# SOME FUNCTIONS FOR NEURAL STYLE CARTOON

class ConvLayer(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride):
        super().__init__()
        reflection_padding = kernel_size // 2
        self.reflection_pad = nn.ReflectionPad2d(reflection_padding)
        self.conv2d = nn.Conv2d(in_channels, out_channels, kernel_size, stride)

    def forward(self, x):
        out = self.reflection_pad(x)
        out = self.conv2d(out)
        return out

class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.conv1 = ConvLayer(channels, channels, 3, 1)
        self.in1 = nn.InstanceNorm2d(channels, affine=True)
        self.conv2 = ConvLayer(channels, channels, 3, 1)
        self.in2 = nn.InstanceNorm2d(channels, affine=True)

    def forward(self, x):
        residual = x
        out = F.relu(self.in1(self.conv1(x)))
        out = self.in2(self.conv2(out))
        return out + residual

class UpsampleConvLayer(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride, upsample=None):
        super().__init__()
        self.upsample = upsample
        reflection_padding = kernel_size // 2
        self.reflection_pad = nn.ReflectionPad2d(reflection_padding)
        self.conv2d = nn.Conv2d(in_channels, out_channels, kernel_size, stride)

    def forward(self, x):
        if self.upsample:
            x = F.interpolate(x, scale_factor=self.upsample)
        out = self.reflection_pad(x)
        out = self.conv2d(out)
        return out

class TransformerNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = ConvLayer(3, 32, 9, 1)
        self.in1 = nn.InstanceNorm2d(32, affine=True)
        self.conv2 = ConvLayer(32, 64, 3, 2)
        self.in2 = nn.InstanceNorm2d(64, affine=True)
        self.conv3 = ConvLayer(64, 128, 3, 2)
        self.in3 = nn.InstanceNorm2d(128, affine=True)
        self.res1 = ResidualBlock(128)
        self.res2 = ResidualBlock(128)
        self.res3 = ResidualBlock(128)
        self.res4 = ResidualBlock(128)
        self.res5 = ResidualBlock(128)
        self.deconv1 = UpsampleConvLayer(128, 64, 3, 1, upsample=2)
        self.in4 = nn.InstanceNorm2d(64, affine=True)
        self.deconv2 = UpsampleConvLayer(64, 32, 3, 1, upsample=2)
        self.in5 = nn.InstanceNorm2d(32, affine=True)
        self.deconv3 = ConvLayer(32, 3, 9, 1)

    def forward(self, x):
        y = F.relu(self.in1(self.conv1(x)))
        y = F.relu(self.in2(self.conv2(y)))
        y = F.relu(self.in3(self.conv3(y)))
        y = self.res1(y)
        y = self.res2(y)
        y = self.res3(y)
        y = self.res4(y)
        y = self.res5(y)
        y = F.relu(self.in4(self.deconv1(y)))
        y = F.relu(self.in5(self.deconv2(y)))
        y = self.deconv3(y)
        return y
    
# -----------------------
# UDNIE, MOSAIC, CANDY STYLE CARTOON
# ------------------------

# ---------------- CARTOONIFY FUNCTION ----------------
def cartoon_neural_style(image_input, style_model_path: str, resize: int = 512, add_edges: bool = True):

    device = torch.device("cpu")

    # Load image
    if isinstance(image_input, str):
        if image_input.startswith("http://") or image_input.startswith("https://"):
            import requests
            response = requests.get(image_input)
            input_image = Image.open(BytesIO(response.content)).convert("RGB")
        else:  # local file path
            input_image = Image.open(image_input).convert("RGB")
    elif isinstance(image_input, Image.Image):
        input_image = image_input.convert("RGB")
    else:
        raise ValueError("image_input must be URL, local path, or PIL.Image")

    # Load model
    model = TransformerNet()
    state_dict = torch.load(style_model_path, map_location=device)
    # remove deprecated running stats keys
    for k in list(state_dict.keys()):
        if re.search(r'in\d+\.running_(mean|var)$', k):
            del state_dict[k]
    model.load_state_dict(state_dict, strict=False)
    model.to(device).eval()

    # Transform input
    transform = transforms.Compose([
        transforms.Resize(resize),
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.mul(255))
    ])
    img_tensor = transform(input_image).unsqueeze(0)

    # Forward pass
    with torch.no_grad():
        output = model(img_tensor).cpu()
    output = output[0].clamp(0, 255).div(255).permute(1, 2, 0).numpy()
    cartoon = np.uint8(output * 255)

    # Add edges
    if add_edges:
        edges = cv2.Canny(cartoon, 80, 150)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        edges = cv2.bitwise_not(edges)
        cartoon = cv2.bitwise_and(cartoon, edges)
        
    cartoon_img = Image.fromarray(cartoon)
    
    style_name = style_model_path[7:-4].capitalize()+" "+"Style"
    
    return cartoon_img


# -----------------------
# DISNEY STYLE CARTOON
# ------------------------

repo_path = os.path.join(os.path.dirname(__file__), "photo2cartoon")
sys.path.append(repo_path)

# Import the Photo2Cartoon class
from photo2cartoon_model import Photo2Cartoon

# Initialize the model once
c2p = Photo2Cartoon()

def disney_cartoon(image_path):
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        return None
    
    try:
        # Read image from URL
        image = Image.open(image_path).convert("RGB")
        img_array = np.array(image)
        original_h, original_w = img_array.shape[:2]

        # Run the cartoon model
        cartoon = c2p.inference(img_array)

        if cartoon is not None:
            # BGR image (for OpenCV compatibility)
            cartoon_resized = cv2.resize(cartoon, (original_w, original_h), interpolation=cv2.INTER_LINEAR)
            return cartoon_resized
        else:
            return None
    except Exception as e:
        print("Error processing image:", e)
        return None

