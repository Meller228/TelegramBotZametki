import telebot
import sqlite3

TOKEN = 'TKN'
bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('notes.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, text TEXT)')
conn.commit()

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "/add текст\n/list\n/delete ID\n/edit ID текст")

@bot.message_handler(commands=['add'])
def add(m):
    p = m.text.split(maxsplit=1)
    if len(p) < 2: return bot.reply_to(m, "Напиши текст")
    cursor.execute("INSERT INTO notes (user_id, text) VALUES (?, ?)", (m.chat.id, p[1]))
    conn.commit()
    bot.reply_to(m, "✅ Сохранено")

@bot.message_handler(commands=['list'])
def lst(m):
    cursor.execute("SELECT id, text FROM notes WHERE user_id = ?", (m.chat.id,))
    notes = cursor.fetchall()
    if not notes: return bot.reply_to(m, "Пусто")
    bot.send_message(m.chat.id, "\n".join(f"[{i}] {t}" for i, t in notes))

@bot.message_handler(commands=['delete'])
def delete(m):
    p = m.text.split()
    if len(p) < 2: return bot.reply_to(m, "Укажи ID")
    cursor.execute("DELETE FROM notes WHERE id = ? AND user_id = ?", (p[1], m.chat.id))
    conn.commit()
    bot.reply_to(m, "🗑 Удалено" if cursor.rowcount else "❌ Не найдено")

@bot.message_handler(commands=['edit'])
def edit(m):
    p = m.text.split(maxsplit=2)
    if len(p) < 3: return bot.reply_to(m, "Формат: /edit ID новый текст")
    cursor.execute("UPDATE notes SET text = ? WHERE id = ? AND user_id = ?", (p[2], p[1], m.chat.id))
    conn.commit()
    bot.reply_to(m, "✏️ Обновлено" if cursor.rowcount else "❌ Не найдено")

bot.infinity_polling()