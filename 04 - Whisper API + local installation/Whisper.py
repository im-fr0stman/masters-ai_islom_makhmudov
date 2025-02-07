# from openai import OpenAI
# import os
#
# # Initialize OpenAI client
# client = OpenAI()
#
# # File path (assuming it's in the project directory)
# file_name = "ITPU_MS_Degree_Session_5_-_Generative_AI-20241213_153714-Meeting_Recording_1.mp3"
# file_path = os.path.join(os.getcwd(), file_name)  # Uses the current directory
#
# # Verify file exists
# if not os.path.exists(file_path):
#     raise FileNotFoundError(f"File not found: {file_path}")
#
# # Transcribe the audio file
# with open(file_path, "rb") as audio_file:
#     print(f"Transcribing: {file_path}")
#     transcript = client.audio.transcriptions.create(
#         model="whisper-1",
#         file=audio_file
#     )
#
# # Save the transcription to a file in the same directory
# output_file = os.path.join(os.getcwd(), "transcription.txt")
# with open(output_file, "w", encoding="utf-8") as f:
#     f.write(transcript.text)
#
# print(f"Transcription saved to: {output_file}")

from openai import OpenAI
import os
import re

# Function to format transcription text for readability
def format_text(text):
    # Add new lines after punctuation marks for better readability
    formatted_text = re.sub(r'([.!?]) ', r'\1\n', text)  # New line after ., !, ?
    return formatted_text

# Initialize OpenAI client
client = OpenAI()

# File path (assuming it's in the project directory)
file_name = "ITPU_MS_Degree_Session_5_-_Generative_AI-20241213_153714-Meeting_Recording_1.mp3"
file_path = os.path.join(os.getcwd(), file_name)  # Uses the current directory

# Verify file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

# Transcribe the audio file
with open(file_path, "rb") as audio_file:
    print(f"Transcribing: {file_path}")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

# Format the transcription for readability
formatted_transcription = format_text(transcript.text)

# Save the formatted transcription to a file in the same directory
output_file = os.path.join(os.getcwd(), "formatted_transcription.txt")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(formatted_transcription)

print(f"Formatted transcription saved to: {output_file}")
