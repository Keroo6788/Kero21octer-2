import telebot
import threading
import time

# استخدم التوكن الخاص بك
API_TOKEN = "7829808982:AAFsKJJEzJoWwp1RamqLgzKBC0Bv-eWj-UY"
bot = telebot.TeleBot(API_TOKEN)

# دالة التذكير
def remind_user(chat_id, duration, hours, minutes):
    time.sleep(duration)
    
    # إرسال الرسالة ثلاث مرات عند انتهاء الموقت
    for _ in range(3):
        bot.send_message(chat_id, f'تم انتهاء الموقت! لقد مرت {hours} ساعة و {minutes} دقيقة.')
    
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'مرحبًا! استخدم الأمر /remind لتحديد مدة التذكير.')

@bot.message_handler(commands=['remind'])
def set_reminder(message):
    try:
        duration_str = message.text.split()[1]  # الحصول على المدة المدخلة
        hours, minutes = map(int, duration_str.split('.'))
        duration = (hours * 60 + minutes) * 60  # تحويل إلى ثواني
        
        bot.reply_to(message, f'تم تعيين التذكير لمدة {duration_str}. انتظر...')
        
        # بدء خيط جديد للتذكير
        threading.Thread(target=remind_user, args=(message.chat.id, duration, hours, minutes)).start()
        
    except (IndexError, ValueError):
        bot.reply_to(message, 'يرجى إدخال مدة صحيحة مثل 1.01 (ساعة ودقيقة).')

# بدء البوت
bot.polling()
