# media-downloader-bot Media Downloader Bot
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Python 
Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/) A simple Telegram bot that downloads 
media files (audio, voice messages, videos) forwarded to it, saving them to organized local directories. Created as a workaround for the 
author's ancient tablet's Telegram client crashing when accessing media in-app. For files without direct download options (like voice 
messages), just forward the message to this bot—it handles the rest.
## Features
- **Media Download**: Automatically saves forwarded audio, voice notes, and videos from Telegram chats. - **Metadata Extraction**: For 
audio files, pulls title and artist using TinyTag and names files accordingly (e.g., "Artist - Title.mp3"). - **Smart Naming**: 
Voice/video files get descriptive names like "voice_5s_abc123.mp4" (duration + file ID snippet) to avoid conflicts. - **Error Handling & 
Logging**: Comprehensive logging to console (or file) for debugging downloads/metadata issues. - **Lightweight**: Uses Telepot for 
Telegram API, Requests for downloads—no heavy dependencies. - **Customizable Paths**: Easy to change save directories for audio/video 
via environment variables or code.
## Background
This bot was built out of frustration with a buggy old Android tablet's Telegram app (circa 2018), which crashes on media previews. Manual downloads worked for some files, but voice messages lacked options. Forwarding to the bot bypasses this— it fetches and saves everything locally for offline access or transfer.

## Prerequisites
- Python 3.6+ installed. - A Telegram Bot Token: Create one via [@BotFather](https://t.me/botfather) on Telegram (message `/newbot` and 
follow prompts). - Dependencies: Install via pip: pip install telepot requests tinytag
    - `telepot`: Telegram Bot API wrapper.
  - `requests`: For downloading files from Telegram's servers.
  - `tinytag`: Extracts metadata from audio files (title/artist).
  - Create save directories (e.g., `/home/lygre` for audio/video—adjust in code).
  ## Installation
  1. Clone or download the repo:
  
```git clone https://github.com/yourusername/media-downloader-bot.git cd media-downloader-bot```
   
   2. Set up your environment:
   - Export your bot token: `export BOT_TOKEN="your_bot_token_here"`.
   - (Optional) Create a `.env` file with `BOT_TOKEN=your_token` and load via `python-dotenv` if you add it.
   3. Install dependencies:
   
```pip install -r requirements.txt # If you create one, or run the pip command above```
   
   4. Run the bot:
   
```python cli.py```

      - It will start listening for forwarded messages. Forward any media-containing message to your bot's username.
   ## Usage
   1. **Start the Bot**: Run `python cli.py`—it logs to console (e.g., "Saved audio to ./saved_audio/Artist - Title.mp3").
   2. **Forward Media**: In Telegram:
   - Find a message with audio, voice, or video.
   - Forward it to your bot (e.g., @MediaDownloaderBot).
   - The bot downloads and saves it automatically.
   3. **Check Logs**: Watch the console for success/error messages. Files land in `./saved_audio` (audio as MP3 with metadata names, 
voice/video with duration-based names).
   4. **Customization**:
   - Edit `SAVE_AUDIO_DIR` and `SAVE_VIDEO_DIR` in the code for your paths.
   - For voice notes, it uses `.mp3` extension (Telegram's format)—adjust if needed.
   - Add file handlers for photos/documents by extending the message loop.
   Example log output:
   
```2025-12-16 19:00:00 - main - INFO - Metadata: Song Title by Artist Name
2025-12-16 19:00:01 - main - INFO - Saved audio to ./saved_audio/Artist Name - Song Title.mp3```
