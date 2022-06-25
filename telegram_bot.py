import asyncio
from datetime import datetime
import json
import logging
from multiprocessing.connection import wait
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import exceptions, executor


from init_env import *
from db_requests import *


logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')

bot = Bot(token=TG_API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    print(type(message.from_user.id))
    write_to_database('tg_users', message.from_user.id)
    await message.reply("Здарвствуйте! Торжественно заявляю, что вы подписались на рассылку просроченных поставок")



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


async def broadcast() -> int:
    orders = read_from_database(datetime.now())
    if not orders:
        pass
    else:
        try:
            for order in orders:
                   for user_id in get_users():
                        if order[5] == False :
                            await send_message(user_id, f'Заказ №{str(order[1])} просрочен от {datetime.strftime(order[4], "%d/%m/%Y")}')
                            mark_as_notified(order[1])
        finally:
            log.info(f"notifies successful sent.")    

        

def run_broadcast(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(TG_BROADCAST_DELAY, run_broadcast, coro, loop)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.call_later(TG_BROADCAST_DELAY, run_broadcast, broadcast, loop)
    executor.start_polling(dp, loop=loop)


    #broadcast_thread = threading.Thread(target=run).start()

    
    