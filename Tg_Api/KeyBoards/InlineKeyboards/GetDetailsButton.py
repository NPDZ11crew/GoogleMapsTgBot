from telegram import InlineKeyboardButton


def CreateDetailsButton(id:str) -> [InlineKeyboardButton]:
    text = "Дізнатися більше"
    btn = InlineKeyboardButton(text, callback_data="id:"+id)
    return [btn]
