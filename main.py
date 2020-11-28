#!/usr/bin/python3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import text, bold, italic, code, pre, underline, strikethrough
from xenforo import Api
import configparser
import io


"""
Получаем данные из конфигурационного файла
"""

config = None
admins = None
owner = None
path = "config.ini"

def configuration():
	global config, path, admins, owner

	config = configparser.ConfigParser()
	config.read(path)
	admins = config["Telegram"]["admins"].split("\n")
	owner = config["Telegram"]["owner"]


def save_config():
	global config, path

	with open(path, "w") as config_file:
		config.write(config_file)


configuration()


"""
Работа с правами пользователей
"""

def add_admin(telegram_id):
	global config, admins

	if not is_admin(telegram_id) and not is_owner(telegram_id):
		admins.append(str(telegram_id))
		config.set("Telegram", "admins", '\n'.join(admins))
		save_config()

		return True

	return False


def del_admin(telegram_id):
	global config, admins

	if is_admin(telegram_id):
		del admins[admins.index(str(telegram_id))]
		config.set("Telegram", "admins", '\n'.join(admins))
		save_config()

		return True

	return False


def is_admin(telegram_id):
	global admins

	if str(telegram_id) in admins:
		return True

	return False


def is_owner(telegram_id):
	global owner

	if str(telegram_id) == owner:
		return True

	return False


"""
Инициализируем Telegram бота
"""

bot = Bot(token=config["Telegram"]["token"])
dp = Dispatcher(bot)


"""
Инициализируем XenForo API
"""

xf = Api(config["XenForo"]["url"], config["XenForo"]["api_key"])


"""
Обработчик сообщений и команд
"""

@dp.message_handler()
async def echo(message: types.Message):
	mess = message.text.split(" ")
	mess[0] = mess[0].split("@")[0]

	user_id = message.from_user.id
	reply = message.reply_to_message


	if mess[0] == "/id":
		msg = text("Нет прав для проверки ID других пользователей!")
		if reply is None:
			msg = text("Ваш ID " + code(user_id))
		elif is_admin(user_id) or is_owner(user_id):
			if str(reply.from_user.id) != owner:
				msg = "ID " + code(reply.from_user.id)

			else:
				msg = "Нет прав для просмотра ID данного пользователя!"
		await message.reply(msg, parse_mode=types.ParseMode.MARKDOWN)


	elif mess[0] == "/start" or mess[0] == "/help":
		msg = bold("Помощь по командам бота @overnull\n\n") + "/help - данное сообщение\n/faq - контакты и другая полезная информация\n/userinfo <user> - получить информацию о пользователе\n/id - узнать свой Telegram ID"
		await message.reply(msg, parse_mode=types.ParseMode.MARKDOWN)


	elif mess[0] == "/faq":
		msg = bold("Контакты\n") + "Главный администратор @theovnl\nЭлектронная почта olxhydra@protonmail.com\n\n" + bold("Перенос аккаунта с другого форума\n") + "overnull.ru/threads/161\n\n" + bold("Элитный доступ\n") + "overnull.ru/threads/303\n\n" + bold("Реклама на форумеи канале\n") + "overnull.ru/help/advert"
		await message.reply(msg, parse_mode=types.ParseMode.MARKDOWN)


	elif mess[0] == "/userinfo":
		try:
			user = xf.find_user(mess[1])

			prefix = "Пользователь"
			username = user["username"]


			if user["is_admin"]:
				prefix = "Администратор"

			elif user["is_moderator"]:
				prefix = "Модератор"

			elif user["is_super_admin"]:
				prefix = "Основатель"

			if user["is_banned"]:
				username = strikethrough(username)


			msg = bold(prefix) + " " + username
			msg += bold("\nСимпатий: ") + str(user["reaction_score"])
			msg += bold("\nСообщений: ") + str(user["message_count"])

		except:
			msg = "Пользователь не найден!"

		await message.reply(msg, parse_mode=types.ParseMode.MARKDOWN_V2)


	if is_admin(user_id) or is_owner(user_id):

		if mess[0] == "/helpadmin":
			msg = bold("Помощь по командам бота для администраторов\n\n") + "/helpadmin - данное сообщение\n/admins - список администраторов\n/addadmin <id> - добавить администратора\n/deladmin <id> - удалить администратора\n/emailinfo <email> - найти пользователя по email\n/email <username> - получить почту пользователя\n/reaction <username> <count> - изменить количество симпатий\n/messages <username> <count> - изменить количество сообщений\n/ban <username> <days> - забанить пользователя форуме\n/unban <username> - разбанить пользователя"

			await message.reply(msg, parse_mode=types.ParseMode.MARKDOWN)


		elif mess[0] == "/addadmin":
			if is_owner(user_id):
				try:
					if add_admin(mess[1]):
						msg = "Готово!"

					else:
						msg = "Пользователь уже является администратором!"

				except:
					msg = "/addadmin <telegram_id>"
			else:
				msg = "Нет прав!"

			await message.reply(msg)


		elif mess[0] == "/deladmin":
			if is_owner(user_id):
				try:
					if del_admin(mess[1]):
						msg = "Готово!"

					else:
						msg = "Пользователь не является администратором!"

				except:
					msg = "/deladmin <telegram_id>"
			else:
				msg = "Нет прав!"

			await message.reply(msg)


		elif mess[0] == "/admins":
			if is_owner(user_id):
				msg = '\n'.join(admins)
			else:
				msg = "Нет прав!"

			await message.reply(msg)


		elif mess[0] == "/email":
			try:
				user = xf.find_user(' '.join(mess[1:]))
				msg = ' '.join(mess[1:]) + "\n" + pre(user["email"])

			except:
				msg = "Пользователь не найден!"
			
			await message.reply(msg, parse_mode=types.ParseMode.MARKDOWN_V2)


		elif mess[0] == "/emailinfo":
			try:
				user = xf.find_email(mess[1])
				msg = user["username"] + "\n" + pre(mess[1])

			except:
				msg = "Email не найден!"
			
			await message.reply(msg, parse_mode=types.ParseMode.MARKDOWN_V2)



"""
Точка входа программы
"""

if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)