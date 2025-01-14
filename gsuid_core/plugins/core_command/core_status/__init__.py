from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.aps import scheduler
from gsuid_core.logger import logger
from gsuid_core.global_val import get_global_val

from .command_global_val import save_global_val

sv_core_status = SV('Core状态', pm=0)

template = '''收:{}
发:{}
命令调用:{}
生成图片：{}
当前会话调用：{}'''


@scheduler.scheduled_job('cron', hour='0', minute='0')
async def scheduled_save_global_val():
    global bot_val
    await save_global_val()
    bot_val = {}


@sv_core_status.on_command(('core状态', 'Core状态'))
async def send_core_status_msg(bot: Bot, ev: Event):
    day = ev.text.strip()
    if day and day.isdigit():
        _day = int(day)
    else:
        _day = None
    logger.info('开始执行 早柚核心 [状态]')
    local_val = await get_global_val(ev.real_bot_id, ev.bot_self_id, _day)

    if ev.group_id:
        _command = sum(
            [
                sum(list(local_val['group'][g].values()))
                for g in local_val['group']
            ]
        )
    else:
        _command = sum(list(local_val['user'][ev.user_id].values()))

    if local_val is not None:
        await bot.send(
            template.format(
                local_val['receive'],
                local_val['send'],
                local_val['command'],
                local_val['image'],
                _command,
            )
        )
    else:
        await bot.send('暂未存在当天的记录...')
