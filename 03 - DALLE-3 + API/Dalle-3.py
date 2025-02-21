import os
from openai import OpenAI

# Load API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client with API key
client = OpenAI(api_key=api_key)

# Predefined styles
styles = [
    "photorealistic", "cartoon", "watercolor", "cyberpunk", "anime",
    "oil painting", "sketch", "pixel art", "sci-fi concept art"
]

while True:
    # Ask for user input
    prompt = input("Enter your image description: ")

    # Generate and display 9 images in different styles
    for idx, style in enumerate(styles):
        styled_prompt = f"{prompt}, in {style} style"

        # Generate the image
        response = client.images.generate(
            model="dall-e-3",
            prompt=styled_prompt,
            n=1,
            size="1024x1024"
        )

        # Extract the image URL
        image_url = response.data[0].url

        # Display the image link and description
        print(f"\nImage {idx + 1} - {style} style:")
        print(f"Description: {styled_prompt}")
        print(f"Image URL: {image_url}\n")

    # Ask if the user wants more images
    more_images = input("Do you want to generate images for another prompt? (y/n): ").strip().lower()

    if more_images != "y":
        print("Exiting program. Goodbye!")
        break
