#!/usr/bin/env python3
import argparse
import os
import time
from datetime import datetime
import utils

def main():
    parser = argparse.ArgumentParser(description='Take periodic screenshots using OpenCV and save them to a PDF only')
    parser.add_argument('-r', '--rate', type=int, default=10, 
                        help='Screenshot interval in seconds (default: 10)')
    parser.add_argument('-d', '--duration', type=int, default=1800,
                        help='Total duration in seconds (default: 1800, i.e., 30 minutes)')
    parser.add_argument('-o', '--output', type=str, default='myPDFs',
                        help='Output directory for PDF file (default: myPDFs directory)')
    parser.add_argument('-n', '--name', type=str, default=None,
                        help='Custom name for the PDF file (default: screenshots_TIMESTAMP.pdf)')
    args = parser.parse_args()
    
    # Create output folder if it doesn't exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    # Create a temporary directory for screenshots
    temp_dir = utils.create_temp_directory()
    print(f"Using temporary directory for screenshots: {temp_dir}")
    
    # Calculate number of screenshots to take
    num_screenshots = args.duration // args.rate
    
    print(f"Starting screenshot capture: {num_screenshots} screenshots at {args.rate} second intervals")
    print(f"Total duration: {args.duration} seconds ({args.duration/60:.1f} minutes)")
    print(f"Output PDF will be saved to: {args.output}")
    print("Press Ctrl+C to stop the capture early")
    
    screenshot_files = []
    
    try:
        # Take initial screenshot
        filepath = utils.take_screenshot_opencv(temp_dir)
        screenshot_files.append(filepath)
        
        # Take remaining screenshots at the specified interval
        for i in range(1, num_screenshots):
            time.sleep(args.rate)
            filepath = utils.take_screenshot_opencv(temp_dir)
            screenshot_files.append(filepath)
            
            # Display progress
            print(f"Progress: {i+1}/{num_screenshots} screenshots captured")
    
    except KeyboardInterrupt:
        print("\nScreenshot capture interrupted by user")
    
    # Create PDF from captured screenshots
    if screenshot_files:
        # Create PDF filename
        if args.name:
            pdf_filename = args.name if args.name.endswith('.pdf') else f"{args.name}.pdf"
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_filename = f"screenshots_{timestamp}.pdf"
        
        pdf_path = os.path.join(args.output, pdf_filename)
        utils.create_pdf_with_fpdf(screenshot_files, pdf_path)
        
        print(f"PDF saved to: {os.path.abspath(pdf_path)}")
    else:
        print("No screenshots were taken, no PDF created.")
    
    # Clean up - remove temporary directory and all screenshots
    print("Cleaning up temporary files...")
    utils.cleanup_temp_directory(temp_dir)
    print("Cleanup complete.")

if __name__ == "__main__":
    main()