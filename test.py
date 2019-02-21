from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# main menu
def start(bot, update):
    menu_main = [[InlineKeyboardButton('Option 1', callback_data='m1')],
                 [InlineKeyboardButton('Option 2', callback_data='m2')],
                 [InlineKeyboardButton('Option 3', callback_data='m3')]]
    reply_markup = InlineKeyboardMarkup(menu_main)
    update.message.reply_text('Choose the option:', reply_markup=reply_markup)

# all other menus
def menu_actions(bot, update):
    query = update.callback_query

    if query.data == 'm1':
        print('i work')
        # first submenu
        menu_1 = [[InlineKeyboardButton('Submenu 1-1', callback_data='m1_1')],
                  [InlineKeyboardButton('Submenu 1-2', callback_data='m1_2')]]
        reply_markup = InlineKeyboardMarkup(menu_1)
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              text='Choose the option:',
                              reply_markup=reply_markup)
    elif query.data == 'm2':
        # second submenu
        # first submenu
        menu_2 = [[InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
                  [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')]]
        reply_markup = InlineKeyboardMarkup(menu_2)
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              text='Choose the option:',
                              reply_markup=reply_markup)
    elif query.data == 'm1_1':
        ...
    elif query.data == 'm1_2':
        ...
    # and so on for every callback_data option

...
updater = Updater(token="718571818:AAE3kvTrfr9P7sUMeJAsMmVi7Tv8ghTAwC0")

dp = updater.dispatcher

# handlers
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(menu_actions))

updater.start_polling()

