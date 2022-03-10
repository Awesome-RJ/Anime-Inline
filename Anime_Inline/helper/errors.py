from functools import wraps
import pyrogram
from Anime_Inline import logging
import traceback
import sys
from Anime_Inline.Cutiepii_Robot.inline import ALLOWED_USERS, LOG_CHANNEL


def split_limits(text):
    if len(text) < 2048:
        return [text]

    lines = text.splitlines(True)
    small_msg = ""
    result = []
    for line in lines:
        if len(small_msg) + len(line) < 2048:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line
    result.append(small_msg)

    return result


def capture_err(func):
    @wraps(func)
    async def capture(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except pyrogram.errors.exceptions.forbidden_403.ChatWriteForbidden as err:
            logging.info(
                "Bot was muted in {} {}".format(message.chat.title, message.chat.id)
            )
            await client.leave_chat(message.chat.id)
        except Exception as err:
            await message.reply("**Error:**\n" + str(err))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type, value=exc_obj, tb=exc_tb
            )
            error_feedback = split_limits(
                "**Anime ERROR** | `{}` | `{}`\n\n```{}```\n\n```{}```\n".format(
                    message.from_user.id if message.from_user else 0,
                    message.chat.id if message.chat else 0,
                    message.text or message.caption,
                    "".join(errors),
                )
            )

            for x in error_feedback:
                if LOG_CHANNEL:
                    await client.send_message(LOG_CHANNEL, x)
                else:
                    for m in ALLOWED_USERS:
                        await client.send_message(m, x)
            raise err
    return capture
