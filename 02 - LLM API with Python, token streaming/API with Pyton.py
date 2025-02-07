from openai import OpenAI

client = OpenAI()

with open("lesson-1-transcript.txt", "r") as file:
    file_content = file.read()

user_request = f"Write a blogpost the lecture based on this content:\n{file_content}"

output_text = None

try:
    completion = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=100,
        messages=[
            {"role": "developer", "content": "You are a helpful assistant."},
            {"role": "user", "content": file_content}
        ]
    )

    if completion.choices:
        output_text = completion.choices[0].message.content
        print(output_text)

except Exception as e:
    print(f"An error occurred: {e}")

if output_text:
    save_option = input("Do you want to save the output in a text file? (yes/no): ").strip().lower()
    if save_option == "yes":
        with open("blogpost.txt", "w") as output_file:
            output_file.write(output_text)
        print("Output saved to blogpost.txt")
    else:
        print("Output not saved.")
