# Whisper Transcription Project

## Overview
This project uses OpenAI's Whisper API to transcribe an audio file into text. The transcribed text is then formatted for better readability and saved as a text file.

## Features
- Converts spoken audio into text using Whisper API.
- Automatically formats the transcription for readability.
- Saves the formatted text as a file in the project directory.
- Handles missing files and incorrect paths gracefully.

## Installation
### Prerequisites
- Python 3.7+
- OpenAI API key (set in environment variables)
- Required Python libraries: `openai`, `re`, `os`

### Install Required Libraries
Run the following command to install dependencies:
```bash
pip install openai
```

## Usage
### 1. Set OpenAI API Key
Ensure your OpenAI API key is stored as an environment variable:
```bash
setx OPENAI_API_KEY "your_api_key_here"
```
Restart your terminal for changes to take effect.

### 2. Place Audio File in Project Directory
Move the MP3 file to the project directory. Ensure it is named:
```
ITPU_MS_Degree_Session_5_-_Generative_AI-20241213_153714-Meeting_Recording_1.mp3
```

### 3. Run the Transcription Script
Execute the script to transcribe and format the text:
```bash
python whisper_transcribe.py
```

### 4. Output
The transcribed text will be saved as:
```
formatted_transcription.txt
```
in the same directory as the script.

## File Structure
```
/Project_Directory
│── whisper_transcribe.py      # Main script for transcription
│── formatted_transcription.txt # Output transcription
│── ITPU_MS_Degree_Session_5_-_Generative_AI-20241213_153714-Meeting_Recording_1.mp3 # Audio file
```

## Error Handling
- The script verifies if the file exists before processing.
- If the file is missing, it raises an error.
- The output text is formatted to enhance readability.

## Future Improvements
- Add support for multiple audio files.
- Implement a UI for better usability.
- Enable language detection and automatic formatting.



