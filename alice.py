import logging
import time
import pymongo
import os

from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

tok = os.environ['Telegram_token']
bot = Bot(token=tok)
db = Dispatcher(bot)

client = pymongo.MongoClient("mongodb+srv://SkyDeaD:GamerVD76@aliceskybotandother-ik6lu.mongodb.net/client.test?retryWrites=true&w=majority")
dbase = client.test
coll = dbase.coll
users = dbase.users

adminlist = [577096232, 512177277, 470455469, 1210166637, 983581488]

@db.message_handler(commands=['help'])
async def start_handler(message):
	if message.chat.type=='private':
		q = await bot.get_chat( 577096232 )
		await message.reply(F'''
Я - бот Алиса, разработанный [{q.first_name}](tg://user?id=577096232) для помощи в управлении группами.


На данный момент доступны следующие команды:

*👤me* - информация о себе.

*🌟admins* - список администраторов.

*🤐Mute* - кидает выбранного пользователя в мут.

*😀Unmute* - размучевает выбранного пользователя.

*😵Ban* - кидает в бан выбранного пользователя.

*😃Unban* - разбанивает выбранного пользователя.

*🤕Kick* - выгоняет выбранного пользователя.

*📌Pin* - закрепляет выбранное сообщение.

*❌Unpin* - открепляет закреплённое сообщение.

*🚫Delete* - удаляет выбранное сообщение.

*🧹Purge* - чистит чат. Удаляет выбранное сообщение и всё то, что ниже его.

*⏫Promote* - повышает выбранного пользователя до администратора.

*⏬Demote* - понижает выбранного администратора.


Для полноценный работы в группе мне требуются следующие разрешения:

〽️Изменения профиля группы
❌Удаление сообщений
📛Блокировка участников
📨Пригласительные ссылки
📌Закрепление сообщений
⭐️Добавление администраторов
''', parse_mode = 'markdown')
	else:
		help_msg = await message.reply('''
На данный момент доступны следующие команды:

*👤me* - информация о себе.

*🌟admins* - список администраторов.

*🤐Mute* - кидает выбранного пользователя в мут.

*😀Unmute* - размучевает выбранного пользователя.

*😵Ban* - кидает в бан выбранного пользователя.

*😃Unban* - разбанивает выбранного пользователя.

*🤕Kick* - выгоняет выбранного пользователя.

*📌Pin* - закрепляет выбранное сообщение.

*❌Unpin* - открепляет закреплённое сообщение.

*🚫Delete* - удаляет выбранное сообщение.

*🧹Purge* - чистит чат. Удаляет выбранное сообщение и всё то, что ниже его.

*⏫Promote* - повышает выбранного пользователя до администратора.

*⏬Demote* - понижает выбранного администратора.
    ''', parse_mode = 'markdown')
		time.sleep(60)
		await bot.delete_message(message.chat.id, help_msg.message_id)
		await bot.delete_message(message.chat.id, message.message_id)

@db.message_handler(content_types=['new_chat_members'])
async def handler_new_member(message):
	for user in message.new_chat_members:
		if user.id in [1166033018]:
			await bot.send_message(message.chat.id, 'Привет! Я - бот-администратор Алиса. Для полноценный работы выдай мне следующие разрешения:\n\n〽️Изменения профиля группы\n❌Удаление сообщений\n📛Блокировка участников\n📨Пригласительные ссылки\n📌Закрепление сообщений\n⭐️Добавление администраторов')
		else:
			for user in message.new_chat_members:
				sti = open('welcome.webp', 'rb')
				await bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)
				await bot.send_message(message.chat.id, F'Добро пожаловать, {user.first_name}', reply_to_message_id=message.message_id)

@db.message_handler(commands=['mute'])
async def handle_message(message):
	if message.from_user.id in adminlist:
		prom = await bot.get_chat_member(message.chat.id, 1166033018)
		if prom.can_restrict_members==True:
			if message.reply_to_message!= None:
				user = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
				if user.status not in ['administrator', 'creator']:
					u_mute = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
					if u_mute.can_send_messages==True or u_mute.can_send_messages==None:
						await bot.send_message(message.chat.id, F'[{message.reply_to_message.from_user.first_name}](tg://user?id={message.reply_to_message.from_user.id}) потерял голос.', reply_to_message_i =message.reply_to_message.message_id, parse_mode='markdown')
						await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, until_date = time.time())
					else:
						await bot.send_message(message.chat.id, F'[{message.reply_to_message.from_user.first_name}](tg://user?id={message.reply_to_message.from_user.id}) и так молчит.', reply_to_message_id=message.message_id, parse_mode='markdown')
				else:
					await bot.send_message(message.chat.id, 'Я не буду мутить администратора!', reply_to_message_id = message.message_id)
			else:
				await bot.send_message(message.chat.id,' Я не понимаю, о ком идёт речь? ', reply_to_message_id = message.message_id)
		else:
			await bot.send_message(message.chat.id, 'Для выполнения данной команды требуются следующие права администратора:\n\n📛Блокировка участников', reply_to_message_id = message.message_id)

@db.message_handler(commands=['unmute'])
async def handle_message(message):
	if message.from_user.id in adminlist:
		prom = await bot.get_chat_member(message.chat.id, 1166033018)
		if prom.can_restrict_members==True:
			if message.reply_to_message!=None:
				user = await bot.get_chat_member( message.chat.id, message.reply_to_message.from_user.id)
				if user.status not in ['administrator', 'creator']:
					u_mute = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
					if u_mute.can_send_messages==False:
						await bot.send_message(message.chat.id, F'[{message.reply_to_message.from_user.first_name}](tg://user?id={message.reply_to_message.from_user.id}) снова может говорить.', reply_to_message_id = message.message_id, parse_mode = 'markdown')
						await bot.restrict_chat_member(message.chat.id,message.reply_to_message.from_user.id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
					else:
						await bot.send_message(message.chat.id, F'[{message.reply_to_message.from_user.first_name}](tg://user?id={message.reply_to_message.from_user.id}) и так может говорить.', reply_to_message_id=message.message_id, parse_mode='markdown')
				else:
					await bot.send_message(message.chat.id, ' Администратор не может быть в муте. ', reply_to_message_id = message.message_id)
			else:
				await bot.send_message(message.chat.id,' Я не понимаю, о ком идёт речь? ', reply_to_message_id = message.message_id)
		else:
			await bot.send_message(message.chat.id, 'Для выполнения данной команды требуются следующие права администратора:\n\n📛Блокировка участников', reply_to_message_id = message.message_id)

@db.message_handler(commands=['promote'])
async def handle_message(message):
	if message.from_user.id in adminlist:
		prom = await bot.get_chat_member(message.chat.id, 1166033018)
		if prom.can_promote_members==True:
			if message.reply_to_message!= None:
				user = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
				if user.status not in ['administrator', 'creator']:
					await bot.send_message(message.chat.id, F'[{message.reply_to_message.from_user.first_name}](tg://user?id={message.reply_to_message.from_user.id}) повышен(а)!', reply_to_message_id = message.message_id, parse_mode = 'markdown')
					await bot.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_change_info=True, can_delete_messages=True, can_invite_users=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=True)
				else:
					await bot.send_message(message.chat.id, ' Пользователь уже является администратором! ', reply_to_message_id = message.message_id)
			else:
				await bot.send_message(message.chat.id,' Я не понимаю, о ком идёт речь? ', reply_to_message_id = message.message_id)			
		else:
			await bot.send_message(message.chat.id, 'Для выполнения данной команды требуются следующие права администратора:\n\n⭐️Добавление администраторов', reply_to_message_id = message.message_id)

@db.message_handler(commands=['demote'])
async def handle_message(message):
	if message.from_user.id in adminlist:
		prom = await bot.get_chat_member(message.chat.id, 1166033018)
		if prom.can_promote_members==True:
			if message.reply_to_message!=None:
				user = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
				if user.status in ['administrator', 'creator']:
					try:
						await bot.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_change_info=False, can_delete_messages=False, can_invite_users=False, can_restrict_members=False, can_pin_messages=False, can_promote_members=False)
						await bot.send_message(message.chat.id, F'[{message.reply_to_message.from_user.first_name}](tg://user?id={message.reply_to_message.from_user.id}) понижен(а)!', reply_to_message_id = message.message_id, parse_mode = 'markdown')
					except:
						await bot.send_message(message.chat.id, ' Я не могу понизить данного пользвателя. ', reply_to_message_id = message.message_id)
				else:
					await bot.send_message(message.chat.id, ' Я не могу понизить пользователя, который не является администратором! ', reply_to_message_id = message.message_id)
			else:
				await bot.send_message(message.chat.id,' Я не понимаю, о ком идёт речь? ', reply_to_message_id = message.message_id)			
		else:
			await bot.send_message(message.chat.id, 'Для выполнения данной команды требуются следующие права администратора:\n\n⭐️Добавление администраторов', reply_to_message_id = message.message_id)

@db.message_handler(commands=['kick'])
async def handle_message(message):
	if message.from_user.id in adminlist:
		prom = await bot.get_chat_member(message.chat.id, 1166033018)
		if prom.can_restrict_members==True:
			if message.reply_to_message!=None:
				user = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
				if user.status not in ['administrator', 'creator']:
					users = await bot.get_chat(message.chat.id)
					if user.status=='member':
						sti = open('kick.webp', 'rb')
						await bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
						await bot.send_message(message.chat.id, F'[{message.reply_to_message.from_user.first_name}](tg://user?id={message.reply_to_message.from_user.id}) решил(а) отойти 😄', reply_to_message_id = message.message_id, parse_mode = 'markdown')
						await bot.send_sticker(message.chat.id, sti)
						await bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
					else:
						await bot.send_message(message.chat.id, F'[{message.reply_to_message.from_user.first_name}](tg://user?id={message.reply_to_message.from_user.id}) не является участником чата.', reply_to_message_id = message.message_id, parse_mode = 'markdown')
				else:
					await bot.send_message(message.chat.id, ' Я не могу кикнуть администратора... ', reply_to_message_id = message.message_id)
			else:
				await bot.send_message(message.chat.id,' Я не понимаю, о ком идёт речь? ', reply_to_message_id = message.message_id)			
		else:
			await bot.send_message(message.chat.id, 'Для выполнения данной команды требуются следующие права администратора:\n\n📛Блокировка участников', reply_to_message_id = message.message_id)

@db.message_handler(commands=['ban'])
async def handle_message(message):
	if message.from_user.id in adminlist:
		prom = await bot.get_chat_member(message.chat.id, 1166033018)
		if prom.can_restrict_members==True:
			if message.reply_to_message!=None:
				user = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
				if user.status not in ['administrator', 'creator']:	
					sti = open('ban.webp', 'rb')
					await bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
					await bot.send_message(message.chat.id, F'[{message.reply_to_message.from_user.first_name}](tg://user?id={message.reply_to_message.from_user.id}) решил(а) отойти, долгосрочно...🙂', reply_to_message_id = message.message_id, parse_mode = 'markdown')
					await bot.send_sticker(message.chat.id, sti )
				else:
					await bot.send_message(message.chat.id, ' Я не могу забанить администратора... ', reply_to_message_id = message.message_id)
			else:
				await bot.send_message(message.chat.id,' Я не понимаю, о ком идёт речь? ', reply_to_message_id = message.message_id)			
		else:
			await bot.send_message(message.chat.id, 'Для выполнения данной команды требуются следующие права администратора:\n\n📛Блокировка участников', reply_to_message_id = message.message_id)
		
@db.message_handler(commands=['unban'])
async def handle_message(message):
	if message.from_user.id in adminlist:
		prom = await bot.get_chat_member(message.chat.id, 1166033018)
		if prom.can_restrict_members==True:
			if message.reply_to_message!=None:
				user = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
				if user.status not in ['administrator', 'creator']:	
					if user.status=='restricted':
						sti = open('unban.webp', 'rb')
						await bot.send_message(message.chat.id, F'Ладно, [{message.reply_to_message.from_user.first_name}](tg://user?id={message.reply_to_message.from_user.id}) может вернуться.', reply_to_message_id = message.message_id, parse_mode = 'markdown')
						await bot.send_sticker(message.chat.id, sti)
						await bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
					else:
						await bot.send_message(message.chat.id, F'[{message.reply_to_message.from_user.first_name}](tg://user?id={message.reply_to_message.from_user.id}) не забанен.', reply_to_message_id=message.message_id, parse_mode='markdown')
				else:
					await bot.send_message(message.chat.id, 'Администратор не может быть забанен.', reply_to_message_id = message.message_id)
			else:
				await bot.send_message(message.chat.id, 'Я не понимаю, о ком идёт речь?', reply_to_message_id = message.message_id)			
		else:
			await bot.send_message(message.chat.id, 'Для выполнения данной команды требуются следующие права администратора:\n\n📛Блокировка участников', reply_to_message_id = message.message_id)

@db.message_handler(commands=['pin'])
async def handle_message(message):
	if message.from_user.id in adminlist:
		prom = await bot.get_chat_member(message.chat.id, 1166033018)
		if prom.can_pin_messages==True:
			if message.reply_to_message!=None:
				await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
				await bot.delete_message(message.chat.id, message.message_id)
			else:
				await bot.send_message(message.chat.id,' Выберите сообщение, которое нужно закрепить ', reply_to_message_id = message.message_id)			
		else:
			await bot.send_message(message.chat.id, 'Для выполнения данной команды требуются следующие права администратора:\n\n📌Закрепление сообщений', reply_to_message_id = message.message_id)

@db.message_handler(commands=['unpin'])
async def handle_message(message):
	if message.from_user.id in adminlist:
		prom = await bot.get_chat_member(message.chat.id, 1166033018 )
		if prom.can_pin_messages == True:
			await bot.unpin_chat_message(message.chat.id)
			await bot.delete_message(message.chat.id, message.message_id)
		else:
			await bot.send_message(message.chat.id, 'Для выполнения данной команды требуются следующие права администратора:\n\n📌Закрепление сообщений\n❌Удаление сообщений', reply_to_message_id = message.message_id)

@db.message_handler(commands=['del'])
async def handle_message(message):
	if message.from_user.id in adminlist:
		prom = await bot.get_chat_member(message.chat.id, 1166033018)
		if prom.can_delete_messages==True:
			if message.reply_to_message!=None:
				await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
				await bot.delete_message(message.chat.id, message.message_id)
			else:
				await bot.send_message(message.chat.id,' Выберите сообщение, которое нужно удалить ', reply_to_message_id = message.message_id)
		else:
			await bot.send_message(message.chat.id, 'Для выполнения данной команды требуются следующие права администратора:\n\n❌Удаление сообщений', reply_to_message_id = message.message_id)
		
@db.message_handler(commands=['purge'])
async def handle_message(message):
	if message.from_user.id in adminlist:
		prom = await bot.get_chat_member(message.chat.id, 1166033018)
		if prom.can_delete_messages==True:
			if message.reply_to_message!=None:
				i = message.reply_to_message.message_id
				q = message.message_id
				for d in range(i, q):
					try:
						await bot.delete_message(message.chat.id, d)
					except:
						pass
				await bot.delete_message(message.chat.id, message.message_id)
				await bot.send_message(message.chat.id, ' Чистка завершена. ')
			else:
				await bot.send_message(message.chat.id, 'Для выполнения данной команды требуются следующие права администратора:\n\n❌Удаление сообщений.', reply_to_message_id = message.message_id)

@db.message_handler(commands=["report"])
async def mandle_message(message):
	if message.reply_to_message!= None:
		adm = await bot.get_chat_administrators(message.chat.id)
		text = 'На данное сообщение поступила жалоба.\n\n'
		for i in adm:
			text += f"\n@{i.user.username}"
		await bot.send_message(message.chat.id, text, reply_to_message_id = message.reply_to_message.message_id)
	else:
		await bot.send_message(message.chat.id, " Выберите сообщение, на которое хотите пожаловаться. ", reply_to_message_id = message.message_id)


@db.message_handler(commands=['me'])
async def handle_message(message):
	if message.chat.type!='private':
		await bot.send_message( message.chat.id, F''' 
*Ваше имя*: `{message.from_user.first_name}`
*Ваш юзернейм*: `@{message.from_user.username}`
*Ваш ID*: `{message.from_user.id} `
*ID этой группы*: `{message.chat.id}`
			                                ''', reply_to_message_id = message.message_id, parse_mode = 'markdown')

@db.message_handler(commands=['admins'])
async def handle_message(message):
	if message.chat.type!='private':
		adm = await bot.get_chat_administrators(message.chat.id)
		text = 'Администраторы чата:\n'
		for i in adm:
			text += f'\n{i.user.first_name} - @{i.user.username}'
		await bot.send_message(message.chat.id, text)






























if __name__ == '__main__':
    executor.start_polling(db, skip_updates=True)
