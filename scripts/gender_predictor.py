from deepface import DeepFace
import cv2
import shutil
import os

def extract_gender(input_image_path, output_image_path):
    try:
        # Load the input image
        input_img = cv2.imread(input_image_path)

        if input_img is None:
            raise ValueError(f"Unable to read the image at path: {input_image_path}")

        # Create a copy of the input image
        output_img = input_img.copy()
        
        # Extract gender prediction
        result = DeepFace.analyze(input_image_path, actions=['gender'], enforce_detection=False)        
        gender = result[0]['gender']
        print("Predicted Gender:", gender)

        # Save the output image
        cv2.imwrite(output_image_path, output_img)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Get the directory of the current script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Specify the paths for input and output images relative to the script's location
    input_directory = os.path.join(script_directory, '../input/')
    output_directory = os.path.join(script_directory, '../output/')

    # Get a list of all image files in the input directory
    image_files = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]

    # Process each image file in the input directory
    for image_file in image_files:
        input_path = os.path.join(input_directory, image_file)
        output_path = os.path.join(output_directory, image_file)

        extract_gender(input_path, output_path)

    print("Gender extraction complete. Output saved to", output_directory)
