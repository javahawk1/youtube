import telebot
import yt_dlp
import os

TOKEN = "YOUR_BOT_TOKEN"
bot = telebot.TeleBot("7607588308:AAHuS9GeQH1w-c1iisGbcrR5OXrj_Lbkkmo")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Salom! 🎬 YouTube video yuklovchi botga xush kelibsiz!\n\n"
                                      "Iltimos, YouTube havolasini yuboring.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()

    # Foydalanuvchiga xabar beramiz
    sent_msg = bot.send_message(message.chat.id, "📥 Yuklab olinmoqda, kuting...")

    try:
        # Yuklab olish sozlamalari
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'video.%(ext)s'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Yuklab olingan fayl nomini topish
        for file in os.listdir():
            if file.startswith("video.") and file.endswith((".mp4", ".mkv", ".webm")):
                video_file = file
                break
        else:
            bot.send_message(message.chat.id, "❌ Video yuklashda xatolik yuz berdi.")
            return

        # Video yuklanganligini xabar qilish
        bot.edit_message_text("📤 Video yuborilmoqda...", message.chat.id, sent_msg.message_id)

        # Foydalanuvchiga videoni yuborish
        with open(video_file, 'rb') as video:
            bot.send_video(message.chat.id, video)

        # Faylni o‘chirish
        os.remove(video_file)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Xatolik yuz berdi: {str(e)}")

bot.polling()
