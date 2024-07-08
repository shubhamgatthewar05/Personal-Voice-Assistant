
# Personal Voice Assistant

A Personal Voice Assistant project that can recognize speech, respond with text-to-speech, perform web searches, open system applications, get weather information, read news, set reminders, and more.

## Features

- Speech recognition
- Text-to-speech
- Get current time and date
- Open system applications and websites
- Get weather updates
- Get news headlines
- Set reminders
- Control system applications (open/close)
- Perform calculations
- Integrate with OpenAI for answering questions
- Interact with WhatsApp Web
- Play music on YouTube

## Requirements

- Python 3.x
- `speech_recognition`
- `pyttsx3`
- `datetime`
- `webbrowser`
- `subprocess`
- `os`
- `openai`
- `pyautogui`
- `re`
- `time`
- `requests`
- `selenium`
- `webdriver_manager`
- `sklearn`

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/personal-voice-assistant.git
   cd personal-voice-assistant
   ```

2. **Create a virtual environment (optional but recommended):**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required libraries:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up your API keys:**

   - Replace `"YOUR_WEATHER_API_KEY"` with your actual weather API key.
   - Replace `"YOUR_NEWS_API_KEY"` with your actual news API key.
   - Replace `"YOUR_API_KEY"` with your actual OpenAI API key.

## Usage

1. **Run the voice assistant:**

   ```sh
   python main.py
   ```

2. **Interact with the assistant:**

   - Speak commands or queries to the assistant.
   - The assistant will recognize your speech and respond accordingly.

## Commands

Here are some example commands you can use:

- **Get current time:**
  ```
  What is the time?
  ```

- **Get current date:**
  ```
  What is the date today?
  ```

- **Open applications:**
  ```
  Open YouTube
  Open Google
  Open settings
  ```

- **Get weather information:**
  ```
  What is the weather like today?
  ```

- **Get news updates:**
  ```
  Give me the latest news
  ```

- **Set reminders:**
  ```
  Set a reminder for 5 PM to attend the meeting
  ```

- **Perform calculations:**
  ```
  Calculate 5 plus 10
  ```

- **Ask questions:**
  ```
  What is the capital of France?
  ```

## Libraries and Tools

- `speech_recognition`: For speech recognition.
- `pyttsx3`: For text-to-speech conversion.
- `datetime`: For handling date and time.
- `webbrowser`: For opening web pages.
- `subprocess`: For opening system applications.
- `os`: For interacting with the operating system.
- `openai`: For integrating with OpenAI's GPT-3.
- `pyautogui`: For automating GUI interactions.
- `re`: For regular expressions.
- `time`: For handling time-related functions.
- `requests`: For making HTTP requests.
- `selenium`: For web automation.
- `webdriver_manager`: For managing web drivers.
- `sklearn`: For machine learning.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any ideas or improvements.

## License

This project is licensed under the MIT License.

---

Replace the placeholder text like `YOUR_WEATHER_API_KEY`, `YOUR_NEWS_API_KEY`, and `YOUR_API_KEY` with your actual API keys before using the README file. Save the README content in a file named `README.md` in your project directory and commit it to your GitHub repository.
