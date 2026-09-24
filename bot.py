import asyncio
import logging
import os

from maxapi import Bot, Dispatcher, F
from maxapi.types import (
    Command,
    MessageCreated,
    MessageCallback,
    CallbackButton,
    MessageButton,
    ButtonsPayload,
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN", "PASTE_YOUR_TOKEN_HERE")

MAIN_MENU_TEXT = (
    "Привет! Я — кадровый бот MAX.\n\n"
    "Я помогу тебе быстро получить информацию по кадровым вопросам.\n"
    "Выбери нужный раздел в меню ниже:"
)

MENU_VACATION = "1. Хочу в отпуск"
MENU_DOCS = "2. Нужны копии документов или справки"
MENU_DONOR = "3. Донорство крови"
MENU_EKEY = "4. Получить электронный ключ"
MENU_DISMISSAL = "5. Увольнение"

VACATION_PAID_TEXT = (
    "Ежегодный оплачиваемый отпуск\n\n"
    "Продолжительность — 28 календарных дней.\n"
    "График отпусков согласовывается заранее, дополнительного заявления не требуется.\n"
    "Перенос отпуска возможен только по согласованию с руководителем."
)

VACATION_UNPAID_TEXT = (
    "Отпуск без сохранения оплаты\n\n"
    "Необходимо согласовать с руководителем за 14 и более дней.\n"
    "После согласования — подать заявление в кадровую службу."
)

DOCS_TEXT = (
    "Копии документов и справки\n\n"
    "Для получения копий документов или справок заполните бланк заявления № 1 в кадровой службе.\n"
    "Срок подготовки — 3 рабочих дня."
)

DONOR_TEXT = (
    "Донорство крови\n\n"
    "Дополнительные дни отдыха предоставляются после согласования с руководителем (за 14+ дней).\n"
    "Необходимо предоставить медицинскую справку."
)

EKEY_TEXT = (
    "Электронный ключ\n\n"
    "Для получения электронного ключа/пропуска оформите лист согласования.\n"
    "Соберите подписи ответственных лиц и получите ключ в отделе ИТ.\n"
    "Передача ключа третьим лицам и копирование запрещены."
)

DISMISSAL_TEXT = (
    "Увольнение\n\n"
    "Необходимо уведомить руководителя за 14+ дней и подать заявление в кадровую службу.\n"
    "В день увольнения подпишите обходной лист и получите документы в кадровой службе."
)


def make_main_menu_buttons():
    buttons = [
        [MessageButton(text=MENU_VACATION)],
        [MessageButton(text=MENU_DOCS)],
        [MessageButton(text=MENU_DONOR)],
        [MessageButton(text=MENU_EKEY)],
        [MessageButton(text=MENU_DISMISSAL)],
    ]
    payload = ButtonsPayload(buttons=buttons)
    return [payload.pack()]


def make_vacation_submenu():
    buttons = [
        [
            CallbackButton(
                text="Ежегодный оплачиваемый отпуск",
                payload="vacation_paid",
            ),
        ],
        [
            CallbackButton(
                text="Отпуск без сохранения оплаты",
                payload="vacation_unpaid",
            ),
        ],
    ]
    payload = ButtonsPayload(buttons=buttons)
    return [payload.pack()]


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message_created(Command("start"))
async def handle_start(event: MessageCreated):
    await event.message.answer(
        text=MAIN_MENU_TEXT,
        attachments=make_main_menu_buttons(),
    )


@dp.message_created()
async def handle_main_menu(event: MessageCreated):
    text = event.message.body.text
    attachments = None

    if text == MENU_VACATION:
        text = MAIN_MENU_TEXT
        attachments = make_vacation_submenu()
    elif text == MENU_DOCS:
        text = DOCS_TEXT
        attachments = make_main_menu_buttons()
    elif text == MENU_DONOR:
        text = DONOR_TEXT
        attachments = make_main_menu_buttons()
    elif text == MENU_EKEY:
        text = EKEY_TEXT
        attachments = make_main_menu_buttons()
    elif text == MENU_DISMISSAL:
        text = DISMISSAL_TEXT
        attachments = make_main_menu_buttons()
    else:
        text = "Извините, я вас не понял. Пожалуйста, воспользуйтесь кнопками меню."
        attachments = make_main_menu_buttons()

    await event.message.answer(text=text, attachments=attachments)


@dp.message_callback()
async def handle_vacation_callback(event: MessageCallback):
    payload = event.callback.payload

    if payload == "vacation_paid":
        text = VACATION_PAID_TEXT
    elif payload == "vacation_unpaid":
        text = VACATION_UNPAID_TEXT
    else:
        text = "Неизвестный пункт меню."

    await event.answer()
    await bot.send_message(
        user_id=event.callback.user.user_id,
        text=text,
        attachments=make_main_menu_buttons(),
    )


async def main():
    if BOT_TOKEN == "PASTE_YOUR_TOKEN_HERE":
        raise RuntimeError("Укажите токен бота в переменной окружения BOT_TOKEN")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())