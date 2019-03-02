from telegram import LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PreCheckoutQueryHandler, CallbackQueryHandler
import json
from tabulate import tabulate


# TODO: translate comments
class CoffeeBot:
    def __init__(self):
        self.cart = []
        self.prices = self.parse_items()

    def start_callback(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text="Добро пожаловать в Test Coffee Bot, где вы"
                              " можете заказывать кофе прямо из Телеграм. Нажмите /choose!")

    def order(self, bot, update):
        chat_id = update.message.chat_id
        title = 'Ваш заказ...'
        description = "Нажмите на кнопку, чтобы увидеть подробную информацию о заказе"
        payload = "Отправлено с помощью телеграм бота"
        provider_token = "401643678:TEST:5e9fcf5b-6fd3-471f-9f44-9973107b5dce"
        start_parameter = "test-payment"
        currency = "RUB"
        bot.sendInvoice(chat_id, title, description, payload,
                        provider_token, start_parameter, currency, self.prices,
                        need_name=True, need_phone_number=True,
                        need_email=False)

    # TODO: get items from "prices"
    def choose(self, bot, update):
        menu_main = [[InlineKeyboardButton('Капучино - 100р.', callback_data='m1')],
                     [InlineKeyboardButton('Латте - 100р.', callback_data='m2')],
                     [InlineKeyboardButton('Эспрессо - 70р.', callback_data='m3')],
                     [InlineKeyboardButton('Раф - 130р.', callback_data='m4')],
                     [InlineKeyboardButton('Мокачино - 120р.', callback_data='m5')],
                     [InlineKeyboardButton('🏁 Завершить заказ 🏁', callback_data='m6')]]
        reply_markup = InlineKeyboardMarkup(menu_main)
        update.message.reply_text('Нажмите на элемент, чтобы добавить его в корзину:', reply_markup=reply_markup)

    def select_menu_actions(self, bot, update):

        query = update.callback_query
        selected_item = {}

        if query.data == 'm1':

            selected_item["name"] = "Капучино"
            selected_item["price"] = "10000"
            print('Выбрали Капучино')

        elif query.data == 'm2':

            selected_item["name"] = "Латте"
            selected_item["price"] = "10000"
            print('Выбрали латте')

        elif query.data == 'm3':

            selected_item["name"] = 'Эспрессо'
            selected_item["price"] = "7000"
            print('Выбрали эспрессо')

        elif query.data == 'm4':

            selected_item["name"] = "Раф"
            selected_item["price"] = "13000"
            print('Выбрали раф')

        elif query.data == 'm5':

            selected_item["name"] = "Моккачино"
            selected_item["price"] = "12000"
            print('Выбрали латте')

        elif query.data == 'm6':
            with open('items.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(self.cart, ensure_ascii=False))
            query.edit_message_text(text="Вы сделали свой заказ\nНажмите /order, чтобы перейти к оплате")
            return

        self.cart.append(selected_item)
        print(self.cart)

    def parse_items(self):
        with open('items.json') as f:
            items = json.load(f)
        shopping_cart = []
        for item in items:
            shopping_cart.append(LabeledPrice(item["name"], item["price"]))
        return shopping_cart

    def menu(self, bot, update):
        with open('menu.json', 'r') as j:
            json_data = json.load(j)
            for d in json_data:
                name = d['name']
                price = d['price'] / 100
                labels = ['Название:', 'Цена:']
                data = [name, price]
                table = zip(labels, data)
                list = tabulate(table, tablefmt="simple")
                bot.send_message(chat_id=update.message.chat_id, text=list)

    # Первая форма сбербанк
    def precheckout_callback(self, bot, update):
        precheckout_info = update.pre_checkout_query
        bot.answer_pre_checkout_query(pre_checkout_query_id=precheckout_info.id, ok=True)
        return precheckout_info

    # TODO: send ordered items after successful payment
    # Успешная оплата (после правильного 8-ми значного пароля - проверка от банка)
    def successful_payment_callback(self, bot, update):
        update.message.reply_text("Благодарим вас за оплату")
        print(self.precheckout_callback())


# Launch all necessary functions and handlers
def main():
    coffee_bot = CoffeeBot()

    # API бота
    updater = Updater(token="718571818:AAE3kvTrfr9P7sUMeJAsMmVi7Tv8ghTAwC0")

    # Хэндлеры для выполнении функции при вводе определенных команда
    dp = updater.dispatcher

    # Старт
    dp.add_handler(CommandHandler("start", coffee_bot.start_callback))

    # Заказ
    dp.add_handler(CommandHandler("order", coffee_bot.order))

    dp.add_handler(CommandHandler("menu", coffee_bot.menu))

    dp.add_handler(CommandHandler("choose", coffee_bot.choose))

    # Заключительная проверка
    dp.add_handler(PreCheckoutQueryHandler(coffee_bot.precheckout_callback))

    # Маршрутизатор нажатий кнопок после выбора /select_coffee

    dp.add_handler(CallbackQueryHandler(coffee_bot.select_menu_actions))

    # Успешная оплата
    dp.add_handler(MessageHandler(Filters.successful_payment, coffee_bot.successful_payment_callback))

    updater.start_polling()


# Launch program
if __name__ == '__main__':
    main()
