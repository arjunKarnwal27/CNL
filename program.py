import slideio
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import time
import re

def extract_mpp(raw_metadata):
    """Extracts the MPP (microns per pixel) value from raw metadata."""
    mpp_match = re.search(r'MPP\s*=\s*([\d\.]+)', raw_metadata)
    if mpp_match:
        print(mpp_match.group(1))
        return float(mpp_match.group(1))
    return None

def process_svs_file(file_path, output_dir, mpp_dict):
    try:
        print(f"Processing file: {file_path}")
        
        # Open the slide
        slide = slideio.open_slide(file_path, "SVS")
        mpp_value = extract_mpp(slide.raw_metadata)
        if mpp_value is not None:
            mpp_dict[os.path.basename(file_path)] = mpp_value
        else:
            print(f"MPP value not found for file: {file_path}")


        # Get the first scene
        scene = slide.get_scene(0)

        # Define the region to read (x, y, width, height)
        x = 0
        y = 0
        width = scene.rect[2] - x
        height = scene.rect[3] - y
        region = scene.read_block(rect=(x, y, width, height))

        # Convert the region to an OpenCV-compatible format (BGR)
        region_bgr = cv2.cvtColor(region, cv2.COLOR_RGB2BGR)

        # Convert the image to HSV color space
        hsv = cv2.cvtColor(region_bgr, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        v_clahe = clahe.apply(v)
        hsv_clahe = cv2.merge([h, s, v_clahe])
        image_clahe = cv2.cvtColor(hsv_clahe, cv2.COLOR_HSV2BGR)

        # Convert the equalized image back to RGB for further processing
        image_rgb_clahe = cv2.cvtColor(image_clahe, cv2.COLOR_BGR2RGB)

        # Convert the image to HSV color space for color detection
        hsv_eq = cv2.cvtColor(image_rgb_clahe, cv2.COLOR_RGB2HSV)
        blurred = cv2.GaussianBlur(hsv_eq, (31, 31), 0)

        # Define the range for dark purple and light purple in HSV
        dark_purple_rgb = np.uint8([[[34, 22, 63]]])
        light_purple_rgb = np.uint8([[[158, 92, 142]]])
        dark_purple_hsv = cv2.cvtColor(dark_purple_rgb, cv2.COLOR_RGB2HSV)[0][0]
        light_purple_hsv = cv2.cvtColor(light_purple_rgb, cv2.COLOR_RGB2HSV)[0][0]

        # Define HSV ranges (with some tolerance)
        lower_dark_purple = np.array([dark_purple_hsv[0] - 10, 50, 50])
        upper_dark_purple = np.array([dark_purple_hsv[0] + 10, 255, 255])
        lower_light_purple = np.array([light_purple_hsv[0] - 10, 50, 50])
        upper_light_purple = np.array([light_purple_hsv[0] + 10, 255, 255])

        # Create masks for dark purple and light purple regions
        mask_dark_purple = cv2.inRange(blurred, lower_dark_purple, upper_dark_purple)
        mask_light_purple = cv2.inRange(blurred, lower_light_purple, upper_light_purple)

        kernel = np.ones((13, 13), np.uint8)
        dilated_dark_mask = cv2.dilate(mask_dark_purple, kernel, iterations=1)

        # Find contours in the masks
        contours_dark_purple, _ = cv2.findContours(dilated_dark_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_light_purple, _ = cv2.findContours(mask_light_purple, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contours_dark_purple = sorted(contours_dark_purple, key=cv2.contourArea, reverse=True)

        num_contours_to_keep = 2
        largest_contours_dark_purple = contours_dark_purple[:num_contours_to_keep]

        # Create a blank mask
        mask = np.zeros_like(dilated_dark_mask)

        # Draw the largest contour on the mask
        cv2.drawContours(mask, largest_contours_dark_purple, -1, (255), thickness=cv2.FILLED)

        # Apply dilation to the mask
        kernel = np.ones((25, 25), np.uint8)
        dilated_mask = cv2.dilate(mask, kernel, iterations=1)

        # Apply the dilated mask to the image
        result = cv2.bitwise_and(image_rgb_clahe, image_rgb_clahe, mask=dilated_mask)

        # Save the result
        output_path = os.path.join(output_dir, f'result_{os.path.basename(file_path)}.png')
        cv2.imwrite(output_path, cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
        print(f"Processed and saved: {output_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_straightened_files(initial_count, output_dir):
    processed_count = 0
    folder_path = 'straightenedfile'
    processed_files = set()  # To keep track of processed files

    while processed_count < initial_count * 2:
        while not os.path.exists(folder_path):
            print(f"Waiting for the folder '{folder_path}' to appear...")
            time.sleep(10)
        straightened_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and not f.startswith('.')]

        # Filter out already processed files
        straightened_files = [f for f in straightened_files if f not in processed_files]

        if len(straightened_files) > 0:
            for filename in straightened_files:
                file_path = os.path.join(folder_path, filename)
                print(f"Processing straightened file: {filename}")
                try:
                    # Add your specific processing for the straightened files here
                    print(file_path)
                    image = cv2.imread(file_path)
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    print(file_path)
                    # Convert the image to HSV color space
                    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                    blurred = cv2.GaussianBlur(hsv, (301, 3), 0)

                    # Define the range for dark purple and light purple in HSV
                    dark_purple_rgb = np.uint8([[[34, 22, 63]]])
                    dark_purple_hsv = cv2.cvtColor(dark_purple_rgb, cv2.COLOR_RGB2HSV)[0][0]

                    # Define HSV ranges (with some tolerance)
                    lower_dark_purple = np.array([dark_purple_hsv[0] - 10, 50, 50])
                    upper_dark_purple = np.array([dark_purple_hsv[0] + 3, 200, 200])

                    # Create masks for dark purple regions
                    mask_dark_purple = cv2.inRange(blurred, lower_dark_purple, upper_dark_purple)

                    kernel = np.ones((3, 3), np.uint8)
                    dilated_dark_mask = cv2.dilate(mask_dark_purple, kernel, iterations=1)

                    # Find contours in the masks
                    contours_dark_purple, _ = cv2.findContours(dilated_dark_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    contours_dark_purple = sorted(contours_dark_purple, key=cv2.contourArea, reverse=True)
                    num_contours_to_keep = 1
                    largest_contours_dark_purple = contours_dark_purple[:num_contours_to_keep]

                    # Draw only the largest contours on the image
                    bordered_image = image_rgb.copy()
                    cv2.drawContours(bordered_image, largest_contours_dark_purple, -1, (0, 255, 0), 2)

                    # Create a blank mask
                    mask = np.zeros_like(dilated_dark_mask)

                    # Draw the largest contour on the mask
                    cv2.drawContours(mask, largest_contours_dark_purple, -1, (255), thickness=cv2.FILLED)

                    # Apply dilation to the mask
                    kernel = np.ones((55, 55), np.uint8)
                    dilated_mask = cv2.dilate(mask, kernel, iterations=1)

                    mask_inv = cv2.bitwise_not(dilated_mask)

                    contours_dark_purple, _ = cv2.findContours(mask_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    contours_dark_purple = sorted(contours_dark_purple, key=cv2.contourArea, reverse=True)
                    largest_contours_dark_purple = contours_dark_purple[:num_contours_to_keep]

                    mask2 = np.zeros_like(dilated_dark_mask)

                    # Draw the largest contour on the mask
                    cv2.drawContours(mask2, largest_contours_dark_purple, -1, (255), thickness=cv2.FILLED)

                    kernel = np.ones((35, 35), np.uint8)
                    dilated_mask2 = cv2.dilate(mask2, kernel, iterations=1)

                    image_no_largest_contour = cv2.bitwise_and(image_rgb, image_rgb, mask=dilated_mask2)

                    # Apply the dilated mask to the image
                    result = cv2.bitwise_and(image_rgb, image_rgb, mask=dilated_mask)
                    contour_center_y = np.mean([point[0][1] for point in largest_contours_dark_purple[0]])

                    image_height = image.shape[0]
                    if contour_center_y < image_height / 2:
                        # Contour is in the upper half, so it's ONL
                        output_path_onl = os.path.join(output_dir, f'result_ONL_{filename}')
                        output_path_inl = os.path.join(output_dir, f'result_INL_{filename}')
                    else:
                        # Contour is in the lower half, so it's INL
                        output_path_onl = os.path.join(output_dir, f'result_INL_{filename}')
                        output_path_inl = os.path.join(output_dir, f'result_ONL_{filename}')

                    cv2.imwrite(output_path_onl, cv2.cvtColor(image_no_largest_contour, cv2.COLOR_RGB2BGR))
                    cv2.imwrite(output_path_inl, cv2.cvtColor(result, cv2.COLOR_RGB2BGR))

                    # Remove processed file
                    os.listdir(folder_path).remove(filename)
                    straightened_files.remove(filename)
                    processed_count += 1
                    print(f"Processed and saved: {output_path_onl}, {output_path_inl}")

                    processed_files.add(filename)
                except Exception as e:
                    print(f"Error processing straightened file {filename}: {e}")
        else:
            print("Waiting for new straightened files...")
            time.sleep(5)

def main():
    input_dir = './svsfiles'  # Set this to the directory containing your SVS files
    output_dir = './output'  # Set this to the desired output directory
    output_dir2 = './output2'  # Set this to the desired output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    mpp_dict = {}
    svs_files = [f for f in os.listdir(input_dir) if f.endswith('.svs')]
    initial_count = len(svs_files)

    for svs_file in svs_files:
        process_svs_file(os.path.join(input_dir, svs_file), output_dir, mpp_dict)

    print("Waiting for straightened files to process...")
    process_straightened_files(initial_count, output_dir2)

if __name__ == "__main__":
    main()
