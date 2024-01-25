from deepface import DeepFace
from PIL import Image, ImageDraw, ImageFont
import os

def extract_gender(input_image_path, output_directory):
    try:
        # Load the input image using Pillow
        input_img = Image.open(input_image_path)

        # Extract gender prediction
        result = DeepFace.analyze(input_image_path, actions=['gender'], enforce_detection=False)
        gender_stats = result[0]['gender']
        print("Predicted Gender:", gender_stats)

        # Select the dominant gender label
        gender = max(gender_stats, key=gender_stats.get)

        # Create a drawing object
        draw = ImageDraw.Draw(input_img)
        font = ImageFont.load_default()
        position = (10, 10)  # Top-left corner

        # Create the output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

        # Save the output image as JPEG with a filename based on predicted gender
        output_filename = f"{gender.lower()}.jpg"
        output_path = os.path.join(output_directory, output_filename)
        input_img.save(output_path, format='JPEG')

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Specify the paths for input images and the output directory
    input_directory = "input/"
    output_directory = "output/"

    # Get a list of all image files in the input directory
    image_files = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]

    # Process each image file in the input directory
    for image_file in image_files:
        input_path = os.path.join(input_directory, image_file)

        extract_gender(input_path, output_directory)

    print("Gender extraction complete. Output saved as JPEG to", output_directory)
