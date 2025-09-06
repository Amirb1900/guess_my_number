# -*- coding: utf-8 -*-
"""
Created on Sat Sep  6 13:02:03 2025

@author: AmirHossein
"""

import logging
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# فعال‌سازی لاگ برای خطایابی
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# دیکشنری برای ذخیره وضعیت هر کاربر
user_data = {}

# شروع بازی
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    secret_number = random.randint(1, 100)
    user_data[user_id] = {"number": secret_number, "attempts": 0}
    await update.message.reply_text(
        "سلام 👋 من یه عدد بین 1 تا 100 انتخاب کردم. حدس بزن چی هست! 🎯"
    )

# دریافت حدس کاربر
async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_data:
        await update.message.reply_text("اول با دستور /start بازی رو شروع کن!")
        return

    try:
        guess = int(update.message.text)
    except ValueError:
        await update.message.reply_text("لطفاً فقط عدد بفرست 🔢")
        return

    secret_number = user_data[user_id]["number"]
    user_data[user_id]["attempts"] += 1

    if guess < secret_number:
        await update.message.reply_text("عدد من بزرگ‌تره ⬆️")
    elif guess > secret_number:
        await update.message.reply_text("عدد من کوچیک‌تره ⬇️")
    else:
        attempts = user_data[user_id]["attempts"]
        await update.message.reply_text(
            f"آفرین 🎉 درست حدس زدی! عدد {secret_number} بود.\nتعداد تلاش‌هات: {attempts}"
        )
        # شروع بازی جدید
        secret_number = random.randint(1, 100)
        user_data[user_id] = {"number": secret_number, "attempts": 0}
        await update.message.reply_text("بازی جدید شروع شد! دوباره حدس بزن 😎")

import os
from telegram.ext import Application

TOKEN = os.environ['TOKEN']  # توکن رو از Environment Variable می‌خونه
app = Application.builder().token(TOKEN).build()


print("ربات اجرا شد ✅")

app.run_polling()

