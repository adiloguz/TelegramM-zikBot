import telebot
from yt_dlp import YoutubeDL
import os
import re
import time
import glob

TOKEN = 'TELEGRAM BOTUNUZUN API ANAHTARINI BURAYA GİRİN'
bot = telebot.TeleBot(TOKEN)

DOWNLOAD_FOLDER = 'downloads'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def clean_file_name(file_name):
    # Dosya adından geçersiz karakterleri temizle
    cleaned = re.sub(r'[<>:"/\\|?*]', '', file_name)
    # Boşlukları alt çizgi ile değiştir
    cleaned = cleaned.replace(' ', '_')
    # Türkçe karakterleri değiştir
    turkish_chars = {'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
                    'İ': 'I', 'Ğ': 'G', 'Ü': 'U', 'Ş': 'S', 'Ö': 'O', 'Ç': 'C'}
    for turkish, eng in turkish_chars.items():
        cleaned = cleaned.replace(turkish, eng)
    return cleaned[:200]

def clear_download_folder():
    """İndirme klasörünü temizle"""
    try:
        files = glob.glob(os.path.join(DOWNLOAD_FOLDER, '*'))
        for f in files:
            try:
                os.remove(f)
            except Exception as e:
                print(f"Dosya silme hatası {f}: {e}")
    except Exception as e:
        print(f"Klasör temizleme hatası: {e}")

# yt_dlp ayarları
ydl_opts = {
    'format': 'bestaudio[filesize<50M]/bestaudio',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
    'ignoreerrors': True,
    'no_color': True,
    'extract_flat': False,
    'socket_timeout': 10,
    'retries': 3
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Merhaba! Dinlemek istediğiniz şarkının adını gönderin.")

@bot.message_handler(content_types=['text'])
def download_and_send_audio(message):
    song_name = message.text
    chat_id = message.chat.id
    
    # İşlem başlangıç mesajı
    processing_msg = bot.reply_to(message, f"'{song_name}' aranıyor ve indiriliyor...")
    
    try:
        # Önce klasörü temizle
        clear_download_folder()
        
        with YoutubeDL(ydl_opts) as ydl:
            # Önce video bilgilerini al
            print(f"Arama yapılıyor: {song_name}")
            info = ydl.extract_info(f"ytsearch1:{song_name}", download=False)
            
            if not info or ('entries' in info and not info['entries']):
                bot.edit_message_text("Şarkı bulunamadı. Lütfen başka bir şarkı adı deneyin.", 
                                    chat_id, 
                                    processing_msg.message_id)
                return

            # Video bilgilerini al
            video = info['entries'][0] if 'entries' in info else info
            video_url = video['webpage_url']
            
            # İndirme mesajını güncelle
            bot.edit_message_text(f"'{video['title']}' indiriliyor...", 
                                chat_id, 
                                processing_msg.message_id)

            # Videoyu indir
            ydl.download([video_url])
            
            # İndirilen dosyayı bul
            mp3_files = glob.glob(os.path.join(DOWNLOAD_FOLDER, '*.mp3'))
            
            if not mp3_files:
                bot.edit_message_text("İndirme başarısız oldu. Lütfen tekrar deneyin.", 
                                    chat_id, 
                                    processing_msg.message_id)
                return

            # En son indirilen dosyayı al
            latest_file = max(mp3_files, key=os.path.getctime)
            
            print(f"Dosya bulundu: {latest_file}")
            
            try:
                with open(latest_file, 'rb') as audio_file:
                    # Dosyayı gönder
                    bot.send_audio(
                        chat_id,
                        audio_file,
                        title=video.get('title', 'Bilinmeyen'),
                        performer=video.get('uploader', 'Bilinmeyen'),
                        caption=f"🎵 {video.get('title', 'Bilinmeyen')}"
                    )
                # İşlem başarılı mesajı
                bot.edit_message_text("✅ Şarkı başarıyla gönderildi!", 
                                    chat_id, 
                                    processing_msg.message_id)
            except Exception as e:
                print(f"Dosya gönderme hatası: {e}")
                bot.edit_message_text("Dosya gönderilirken bir hata oluştu.", 
                                    chat_id, 
                                    processing_msg.message_id)
                
    except Exception as e:
        print(f"Genel hata: {e}")
        error_msg = "Bir hata oluştu. Lütfen tekrar deneyin."
        if "Video unavailable" in str(e):
            error_msg = "Bu şarkı şu anda kullanılamıyor. Lütfen başka bir şarkı deneyin."
        elif "No video results" in str(e):
            error_msg = "Aradığınız şarkı bulunamadı. Lütfen farklı bir arama terimi deneyin."
        
        bot.edit_message_text(error_msg, chat_id, processing_msg.message_id)
    
    finally:
        # Temizlik yap
        try:
            clear_download_folder()
        except Exception as e:
            print(f"Temizlik hatası: {e}")

# Hata ayıklama modunda çalıştır
print("Bot başlatılıyor...")
bot.polling(none_stop=True)
