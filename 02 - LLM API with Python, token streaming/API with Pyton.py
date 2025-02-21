from openai import OpenAI

client = OpenAI()

# Read the transcript
with open("lesson-1-transcript.txt", "r") as file:
    file_content = file.read()

# Construct user request
user_request = f"Write a well-structured and engaging blog post based on the following lecture transcription:\n{file_content}"

output_text = None

try:
    # Corrected API call with proper roles
    completion = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=2000,
        messages=[
            {"role": "system", "content": "You are a professional blog writer. Craft a clear, engaging, and informative blog post."},
            {"role": "user", "content": user_request}
        ]
    )

    # Extract output
    if completion.choices:
        output_text = completion.choices[0].message.content
        print(output_text)

except Exception as e:
    print(f"An error occurred: {e}")

# Save the output if user wants to
if output_text:
    save_option = input("Do you want to save the output in a text file? (yes/no): ").strip().lower()
    if save_option == "yes":
        with open("blogpost.txt", "w") as output_file:
            output_file.write(output_text)
        print("Output saved to blogpost.txt")
    else:
        print("Output not saved.")
