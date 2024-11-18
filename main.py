import telebot
import json
import random

TOKEN = "7734283851:AAGoDL2hTgfuzItRsdXBq_JpeaaFBNjSYYs"

bot = telebot.TeleBot(TOKEN)

with open("user_data.json", "r", encoding="utf-8") as file:
    user_data = json.load(file)


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот для изучения английских слов!")


@bot.message_handler(commands=["learn"])
def handle_learn(message):
    user_words = user_data.get(str(message.chat.id), {})

    try:
        words_number = int(message.text.split()[1])
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, укажите количество слов для повторения.")
        return

    ask_translation(message.chat.id, user_words, words_number)


def ask_translation(chat_id, user_words, words_left):
    if words_left > 0:
        word = random.choice(list(user_words.keys()))
        translation = user_words[word]
        bot.send_message(chat_id, f"Напиши перевод слова {word}")

        bot.register_next_step_handler_by_chat_id(chat_id, check_translation, translation, words_left)
    else:
        bot.send_message(chat_id, "Слова закончились.")


def check_translation(message, expected_translation, words_left):
    user_translation = message.text.strip().lower()

    if user_translation == expected_translation.lower():
        bot.send_message(message.chat.id, "Правильно! Молодец!")
    else:
        bot.send_message(message.chat.id, f"Неправильно. Правильный перевод: {expected_translation}")

    words_left -= 1
    ask_translation(message.chat.id, user_data[str(message.chat.id)], words_left)


@bot.message_handler(commands=["addword"])
def handle_addword(message):
    global user_data
    chat_id = str(message.chat.id)
    user_dict = user_data.get(chat_id, {})

    try:
        words = message.text.split()[1:]

        if len(words) == 2:
            word, translation = words[0].lower(), words[1].lower()
            user_dict[word] = translation

            user_data[chat_id] = user_dict

            with open("user_data.json", "w", encoding="utf-8") as file:
                json.dump(user_data, file, ensure_ascii=False, indent=4)
            bot.send_message(chat_id, "Слово добавлено.")
        else:
            bot.send_message(chat_id, "Пожалуйста, укажите слово и перевод в формате: /addword слово перевод.")

    except Exception as e:
        bot.send_message(chat_id, "Произошла ошибка. Попробуйте еще раз.")
        print(f"Ошибка: {e}")


@bot.message_handler(commands=["help"])
def handle_help(message):
    bot.send_message(message.chat.id, """Для чего этот бот?
    Этот бот создан для удобного изучения английских слов и их переводов!
    Команды:
    - `/start` — Запустить бота.
    - `/learn` — Начать обучение.
    - `/help` — Получить справочную информацию о боте.
    Автор бота:
    @Pocketic""")


@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if message.text.lower() == "кто ты такой?":
        bot.send_message(message.chat.id, "Я бот для изучения английских слов!")
    elif message.text.lower() == "как у тебя дела?":
        bot.send_message(message.chat.id, "У меня всё хорошо!")
    else:
        bot.send_message(message.chat.id, "Я не распознал твой ответ.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
