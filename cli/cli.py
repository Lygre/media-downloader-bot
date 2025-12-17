
import logging
import os
import requests
import telepot
import tempfile
from tinytag import TinyTag
from telepot.loop import MessageLoop


logging.basicConfig(
    level=logging.INFO,  # Or DEBUG for more details, ERROR for less
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),  # Logs to file
        logging.StreamHandler()  # Also prints to console
    ]
)

LOGGER = logging.getLogger(__name__)  # Use this for your logs
BOT_TOKEN = os.environ["BOT_TOKEN"]
SAVE_AUDIO_DIR = './saved_audio'  # Create this folder first
SAVE_VIDEO_DIR = './saved_video'


bot = telepot.Bot(BOT_TOKEN)



def extract_metadata(file_path) -> tuple:
    try:
        tag = TinyTag.get(file_path) 
        title=tag.title
        artist=tag.artist
        LOGGER.info(f"tag: {tag}, title: {title}, artist: {artist}")

        return title if title != 'Unknown Title' else None, artist if artist != 'Unknown Artist' else None
    except Exception as e:
        LOGGER.info(f"Metadata error: {e}")
        return None, None


def save_media_file(file_id, chat_id, bot_token, media_type='audio', duration=None):
    """Generic save function for audio/video—parametrized by media_type."""
    try:
        # Set dir and ext based on media_type
        save_dir = SAVE_AUDIO_DIR if media_type == 'audio' else SAVE_VIDEO_DIR
        ext = '.mp4' if media_type == 'video' else '.mp3'
        #if media_type == 'voice':
         #   ext = '.wav'

        # Get file info from Telegram
        file_info = bot.getFile(file_id)
        file_path = file_info['file_path']
        download_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"

        # Download the file
        response = requests.get(download_url)
        if response.status_code!= 200:
            raise Exception("Download failed")
        file_content = response.content

        # Temp save to extract metadata (audio only)
        temp_path = f"/tmp/{file_id}.tmp"
        with open(temp_path, 'wb') as f:
            f.write(file_content)

        if media_type == 'audio':
            title, artist = extract_metadata(temp_path)
            LOGGER.info(f"Metadata: {title} by {artist}")
            safe_name = f"{artist} - {title}".replace('/', '_').replace('\\', '_')[:100]
            return_info = title, artist
        elif media_type == 'voice':
            duration = duration or 0
            file_id_snip = file_id[:8]
            safe_name = f"voice_{duration}s_{file_id_snip}".replace('/', '_')[:100]
            return_info = safe_name, duration
        
        else:  # video
            duration = duration or 0
            file_id_snip = file_id[:8]
            safe_name = f"video_{duration}s_{file_id_snip}".replace('/', '_')[:100]
            return_info = safe_name, duration

        # Create dir and save permanently
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, safe_name + ext)
        with open(save_path, 'wb') as f:
            f.write(file_content)

        # Clean temp
        os.unlink(temp_path)

        LOGGER.info(f"Saved {media_type} to {save_path}")
        return save_path, *return_info
    except Exception as e:
        LOGGER.error(f"Save error: {str(e)}")
        return None, None, None


def handle_audio(msg):
    """Handle audio messages."""
    content_type, _, chat_id = telepot.glance(msg)
    if 'audio' not in msg and 'voice' not in msg:
        return
    if 'audio' in msg:
        typ = 'audio'
    if 'voice' in msg:
        typ = 'voice'
    
    file_id = msg[typ]['file_id']
        
    LOGGER.info(f"Processing audio {file_id} in chat {chat_id}")
    bot.sendMessage(chat_id, "Got an MP3! 🎶")
    save_path, title, artist = save_media_file(file_id, chat_id, BOT_TOKEN, media_type=typ)
    if save_path:
        bot.sendMessage(chat_id, f"Saved '{title}' by {artist} to disk! 📁\nPath: {save_path}")
    else:
        bot.sendMessage(chat_id, "Couldn't save the audio—check logs! 😕")

def handle_video(msg):
    """Handle video messages."""
    content_type, _, chat_id = telepot.glance(msg)
    
    key = 'document' if 'video' not in msg else 'video'
    
    file_id = msg[key]['file_id']
    duration = msg[key].get('duration', 0)
    
    LOGGER.info(f"Processing video {file_id} ({duration}s) in chat {chat_id}")
    bot.sendMessage(chat_id, "Got a video!")
    
    save_path, name, dur = save_media_file(file_id, chat_id, BOT_TOKEN, media_type='video', duration=duration)
    
    if save_path:
        bot.sendMessage(chat_id, f"Saved video '{name}.mp4' ({dur}s) to disk! 📹\nPath: {save_path}")
    else:
        bot.sendMessage(chat_id, "Couldn't save the video—check logs! 😕")


def handle_all(msg):
    """Main handler—routes to audio/video."""
    content_type, _, chat_id = telepot.glance(msg)
    LOGGER.info(f"Received {content_type} in chat {chat_id}")
    
    if 'audio' in msg:
        handle_audio(msg)
    elif 'voice' in msg:
        handle_audio(msg)
    elif 'document' in msg and msg['document'].get('mime_type') == 'audio/mpeg':
        handle_audio(msg)
    elif 'video' in msg: 
        handle_video(msg)
    elif 'document' in msg and msg['document'].get('mime_type').startswith('video/'):
        handle_video(msg)
    else:
        bot.sendMessage(chat_id, "Send me audio or video files to save! 🎵📹")


if __name__ == '__main__':
    print("Bot running—send an audio or video file!")
    MessageLoop(bot, handle_all).run_as_thread()  # Catches everything
    while True:
        pass
        
