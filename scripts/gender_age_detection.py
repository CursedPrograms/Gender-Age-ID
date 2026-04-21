from deepface import DeepFace
from PIL import Image, ImageDraw, ImageFont
import os
import json

def extract_gender_and_age(input_image_path, output_directory):
    try:
        # Load the input image using Pillow
        input_img = Image.open(input_image_path)

        # Extract gender and age predictions
        result = DeepFace.analyze(input_image_path, actions=['gender', 'age'], enforce_detection=False)
        gender_stats = result[0]['gender']
        age = int(result[0]['age'])
        print("Predicted Gender:", gender_stats)
        print("Predicted Age:", age)

        # Select the dominant gender label
        gender = max(gender_stats, key=gender_stats.get)

        # Create a drawing object
        draw = ImageDraw.Draw(input_img)
        font = ImageFont.load_default()
        position_gender = (10, 10)  # Top-left corner for gender
        position_age = (10, 30)  # Below gender information

        # Write gender and age information on the image
        draw.text(position_gender, f"Gender: {gender} - {gender_stats[gender]:.2f}%", font=font, fill=(255, 255, 255))
        draw.text(position_age, f"Age: {age} years", font=font, fill=(255, 255, 255))

        # Create the output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

        # Save the output image as JPEG with a filename based on predicted gender
        output_filename = f"{gender.lower()}_age_{age}.jpg"
        output_path = os.path.join(output_directory, output_filename)
        input_img.save(output_path, format='JPEG')

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Get the directory of the current script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Load settings from the JSON file
    with open("settings.json", "r") as file:
        settings = json.load(file)

    # Specify the paths for input and output directories based on the loaded settings
    input_directory = os.path.join(script_directory, settings["directories"]["input"])
    output_directory = os.path.join(script_directory, settings["directories"]["output"])

    # Get a list of all image files in the input directory
    image_files = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]

    # Process each image file in the input directory
    for image_file in image_files:
        input_path = os.path.join(input_directory, image_file)

        extract_gender_and_age(input_path, output_directory)

    print("Gender and age extraction complete. Output saved as JPEG to", output_directory)
