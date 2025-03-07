#!/usr/bin/env python3
import cv2
import numpy as np
import os
import tempfile
import shutil
import pyautogui
from datetime import datetime
from fpdf import FPDF

def create_temp_directory():
    """Create a temporary directory for screenshots"""
    return tempfile.mkdtemp()

def cleanup_temp_directory(temp_dir):
    """Remove temporary directory and all screenshots"""
    shutil.rmtree(temp_dir)

def take_screenshot_opencv(temp_folder):
    """Take a screenshot using pyautogui and process with OpenCV, saving to a temporary folder"""
    # Create timestamp for unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(temp_folder, filename)
    
    # Take screenshot using pyautogui
    screenshot = pyautogui.screenshot()
    
    # Convert PIL image to OpenCV format (numpy array)
    screenshot_cv = np.array(screenshot)
    # Convert RGB to BGR (OpenCV uses BGR)
    screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)
    
    # Save screenshot using OpenCV
    cv2.imwrite(filepath, screenshot_cv)
    
    print(f"Screenshot captured at {datetime.now().strftime('%H:%M:%S')}")
    return filepath

def create_pdf_with_fpdf(screenshot_files, pdf_path):
    """Create a PDF from a list of screenshot files using FPDF"""
    pdf = FPDF()
    
    for img_path in screenshot_files:
        # Get image dimensions
        img = cv2.imread(img_path)
        height, width, _ = img.shape
        
        # Add a page with appropriate orientation
        if width > height:
            pdf.add_page('L')  # Landscape
        else:
            pdf.add_page('P')  # Portrait
        
        # Calculate page dimensions
        page_width = pdf.w
        page_height = pdf.h
        
        # Calculate image size to fit the page with margins
        margin = 10
        max_width = page_width - 2 * margin
        max_height = page_height - 2 * margin - 10  # Extra 10 for timestamp text
        
        # Calculate scale factor to fit within page margins
        width_scale = max_width / width
        height_scale = max_height / height
        scale = min(width_scale, height_scale)
        
        # Calculate dimensions after scaling
        new_width = width * scale
        new_height = height * scale
        
        # Calculate position to center the image
        x = margin + (max_width - new_width) / 2
        y = margin
        
        # Add image to the PDF
        pdf.image(img_path, x=x, y=y, w=new_width, h=new_height)
        
        # Add timestamp caption
        timestamp = os.path.basename(img_path).replace("screenshot_", "").replace(".png", "")
        readable_timestamp = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
        
        pdf.set_font("Arial", size=10)
        pdf.set_xy(x, y + new_height + 5)
        pdf.cell(new_width, 10, f"Screenshot taken: {readable_timestamp}", align='C')
    
    # Save PDF
    pdf.output(pdf_path)
    print(f"PDF created: {pdf_path}")