from handlers.users.api import API


async def view_orders_is_processing(message):
    order_processing = API().orders_processing_get()
    if not order_processing:
        await message.answer('Замовлень нема 🧐')
    else:
        for order in order_processing:
            await message.answer(print_order(order))


def print_order(order_info):
    text = f"<b>Замовлення №{order_info['pk']}</b>\n\n"

    text += f"<b>Дата</b> - <i>{order_info['date'][:19].replace('T', ' ')}</i>\n"

    users = {1: 'Діма', 2: 'Влад'}
    text += f"<b>Створив</b> - <i>{users[order_info['user']]}</i>\n\n"

    desc_product = ''
    for order in order_info['order_products']:
        storage_product = API().storage_product_info(order['product'])
        title = storage_product['title']
        quantity = order['quantity']

        desc_product += f"<b>{title}</b> - {quantity}шт ({users[order['user']]})\n"

    text += desc_product
    text += f"\n<b>ТТН</b> - {order_info['ttn']}\n"
    text += f"<b>Сума</b> - {order_info['price']}грн"
    return text
