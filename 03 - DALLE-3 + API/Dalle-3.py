from openai import OpenAI

client = OpenAI()

while True:
    # Ask for user input
    prompt = input("Enter your image description: ")

    # Generate the image
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )

    # Extract the image URL
    image_url = response.data[0].url

    # Display the image link and description
    print(f"\nDescription: {prompt}\nImage: {image_url}\n")

    # Ask if the user wants more images
    more_images = input("Do you want more images? (y/n): ").strip().lower()

    if more_images != "y":
        print("Exiting program. Goodbye!")
        break  # Exit the loop if the user does not want more images
