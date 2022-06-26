import asyncio
from datetime import datetime
import logging
from aiogram import Bot, Dispatcher, executor, types, exceptions


from init_env import *
from db_requests import *


logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')

bot = Bot(token=TG_API_TOKEN)
dp = Dispatcher(bot)

# Добавляем пользователя бота
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    manage_tg_users(True, message.from_id)
    await send_message(message.from_user.id, "Здарвствуйте! Торжественно заявляю, то, что вы подписались на рассылку просроченных поставок! \n P.S кроме команды /start у нас так-же есть /stop")

@dp.message_handler(commands="stop")
async def cmd_stop(message: types.Message):
    manage_tg_users(False, message.from_user.id)
    await send_message(message.from_id, "Досвидания. И всего хорошего")


# Отправка сообщения 
async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    return False

# Рассылка данных из БД подписчикам
async def broadcast() -> int:
    orders = read_from_database(datetime.now())
    if orders == []:
        log.info(f"notifies successful sent.")  
    else:
        try:
            for order in orders:
                   for user_id in get_users():
                        if order[5] == False :
                            await send_message(user_id, f'Заказ №{str(order[1])} просрочен от {datetime.strftime(order[4], "%d/%m/%Y")}')
                            mark_as_notified(order[1])
        except Exception as e:
            log.warning(f"{e}") 

        
'''7 строк кода ниже здесь для того, чтобы бот слушал команды от 
    пользователя и производил рассылку одновременно '''
    
def run_broadcast(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(TG_BROADCAST_DELAY, run_broadcast, coro, loop)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.call_later(TG_BROADCAST_DELAY, run_broadcast, broadcast, loop)
    executor.start_polling(dp, loop=loop)
