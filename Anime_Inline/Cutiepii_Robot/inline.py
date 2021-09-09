import aiohttp
import requests

from .anilist import t
from Anime_Inline import ANIME
from pyrogram import __version__
from Anime_Inline.Cutiepii_Robot.anilist import url, anime_query, manga_query, airing_query, character_query
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputTextMessageContent,
    InlineQueryResultArticle,
    InlineQueryResultPhoto
)

from Anime_Inline.helper.errors import capture_err
from Anime_Inline import OWNER_USERNAME, BOT_USERNAME, BOT_NAME, INLINE_PIC, INLINE_PIC_1
           
NEXT_OFFSET = 25

@ANIME.on_inline_query()
@capture_err
async def inline_query_handler(client, query):
    string = query.query.lower()
    if string == "":
        await client.answer_inline_query(query.id,
            results=[
                InlineQueryResultPhoto(
                    caption=f"Hello I'm {BOT_NAME} , I can help you to find everything about anime. You can use command or inline to using me 💜",
                    photo_url=f"{INLINE_PIC}",
                    parse_mode="markdown",
                    title=f"Help?",
                    description=f"Click Here..",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                        InlineKeyboardButton("Anime", switch_inline_query_current_chat="anime "),
                        InlineKeyboardButton("Manga", switch_inline_query_current_chat="manga ")                   
                        ],
                        [
                        InlineKeyboardButton("Airing", switch_inline_query_current_chat="airing "),
                        InlineKeyboardButton("Character", switch_inline_query_current_chat="character ")
                        ],
                        [
                        InlineKeyboardButton(text="Help", url=f"https://t.me/{BOT_USERNAME}?start=help")
                        ]]
                    )
                ),
                InlineQueryResultPhoto(
                    caption=f"{BOT_USERNAME} Maintained by {OWNER_USERNAME}",
                    photo_url=f"{INLINE_PIC_1}",
                    parse_mode="markdown",
                    title=f"About?",
                    description=f"Click Here..",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                        InlineKeyboardButton(text="Support", url="support group telegram url"),
                        InlineKeyboardButton(text="Channel", url="bot channel url telegram")                   
                        ],
                        [
                        InlineKeyboardButton(text="Anime_Inline", url="https://github.com/Awesome-RJ/Anime-Inline"),
                        InlineKeyboardButton(text="Owner", url=f"https://t.me/{OWNER_USERNAME}")
                        ],
                        [
                        InlineKeyboardButton(text="Help", url=f"https://t.me/{BOT_USERNAME}?start=help")
                        ]]
                    )
                ),
            ],
            switch_pm_text="bot name Inline Module",
            switch_pm_parameter="start",
            cache_time=300
        )

    answers = []
    if string.split()[0] == "anime":
        if len(string.split()) == 1:
            await client.answer_inline_query(query.id,
                                            results=answers,
                                            switch_pm_text="Search an Anime",
                                            switch_pm_parameter="start"
                                            )
            return
        search = string.split(None, 1)[1]
        variables = {'search' : search}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={'query': anime_query, 'variables': variables}) as resp:
                r = await resp.json()
                json = r['data'].get('Media', None)
                if json:
                    mal_id = int(json.get('idMal'))
                    msg = f"**{json['title']['romaji']}** (`{json['title']['native']}`)\n**Type**: {json['format']}\n**Status**: {json['status']}\n**Episodes**: {json.get('episodes', 'N/A')}\n**Duration**: {json.get('duration', 'N/A')} Per Ep.\n**Score**: {json['averageScore']}\n**Genres**: `"
                    for x in json['genres']: 
                        msg += f"{x}, "
                    msg = msg[:-2] + '`\n'
                    msg += "**Studios**: `"
                    for x in json['studios']['nodes']:
                        msg += f"{x['name']}, " 
                    msg = msg[:-2] + '`\n'
                    info = json.get('siteUrl')
                    mal_link = f"https://myanimelist.net/anime/{mal_id}"
                    trailer = json.get('trailer', None)
                    if trailer:
                        trailer_id = trailer.get('id', None)
                        site = trailer.get('site', None)
                        if site == "youtube": trailer = 'https://youtu.be/' + trailer_id
                    description = json.get('description', 'N/A').replace('<i>', '').replace('</i>', '').replace('<br>', '')
                    msg += shorten(description, info)
                    image = info.replace('anilist.co/anime/', 'img.anili.st/media/')
                    if trailer:
                        buttons = [[InlineKeyboardButton("Anilist", url=info), InlineKeyboardButton("MAL", url=mal_link)], [InlineKeyboardButton("Trailer 🎬", url=trailer)]]
                    else:
                        buttons = [[InlineKeyboardButton("Anilist", url=info), InlineKeyboardButton("MAL", url=mal_link)
                                    ]]
                    if image:
                        answers.append(InlineQueryResultPhoto(
                            caption=msg,
                            photo_url=image,
                            parse_mode="markdown",
                            title=f"{json['title']['romaji']}",
                            description=f"{json['format']} | {json.get('episodes', 'N/A')} Episode{'s' if len(str(json.get('episodes'))) > 1 else ''}",
                            reply_markup=InlineKeyboardMarkup(buttons)))
                    else:
                        answers.append(InlineQueryResultArticle(
                            title=f"{json['title']['romaji']}",
                            description=f"{json['format']} | {json.get('episodes', 'N/A')} Episode{'s' if len(str(json.get('episodes'))) > 1 else ''}",
                            input_message_content=InputTextMessageContent(msg, parse_mode="md", disable_web_page_preview=True),
                            reply_markup=InlineKeyboardMarkup(buttons)))
        await client.answer_inline_query(query.id,
                                        results=answers,
                                        cache_time=0,
                                        is_gallery=False
                                        )
        
    elif string.split()[0] == "manga":
        if len(string.split()) == 1:
            await client.answer_inline_query(query.id,
                                            results=answers,
                                            switch_pm_text="Search Manga",
                                            switch_pm_parameter="start"
                                            )
            return
        search = string.split(None, 1)[1]
        variables = {'search' : search}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={'query': manga_query, 'variables': variables}) as resp:
                r = await resp.json()
                json = r['data'].get('Media', None)
                if json:
                    msg = f"**{json['title']['romaji']}** (`{json['title']['native']}`)\n**Status**: {json['status']}\n**Year**: {json['startDate']['year']}\n**Score**: {json['averageScore']}\n**Genres**: `"
                    for x in json['genres']: 
                        msg += f"{x}, "
                    msg = msg[:-2] + '`\n'
                    description = json.get('description', 'N/A').replace('<i>', '').replace('</i>', '').replace('<br>', '')
                    info = json.get('siteUrl')
                    if info:
                        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("More Info", url=info)]])
                    else:
                        buttons = None
                    msg += shorten(description, info)
                    banner_url = json.get('bannerImage')
                    if banner_url:
                        answers.append(InlineQueryResultPhoto(
                            caption=msg,
                            photo_url=banner_url,
                            parse_mode="markdown",
                            title=f"{json['title']['romaji']}",
                            description=f"{json['startDate']['year']}",
                            reply_markup=buttons))8
                    else:
                        answers.append(InlineQueryResultArticle(
                            title=f"{json['title']['romaji']}",
                            description=f"{json['averageScore']}",
                            input_message_content=InputTextMessageContent(msg, parse_mode="markdown", disable_web_page_preview=True),
                            reply_markup=buttons))
        await client.answer_inline_query(query.id,
                                        results=answers,
                                        cache_time=0,
                                        is_gallery=False
                                        )
    elif string.split()[0] == "airing":
        if len(string.split()) == 1:
            await client.answer_inline_query(query.id,
                                            results=answers,
                                            switch_pm_text="Get the Airing Status",
                                            switch_pm_parameter="start"
                                            )
            return
        search = string.split(None, 1)[1]
        variables = {'search': search}
        response = requests.post(
            url, json={'query': airing_query, 'variables': variables}).json()['data']['Media']
        info = response['siteUrl']
        if info:
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("More Info", url=info)]])
        else:
            buttons = None
        image = info.replace('anilist.co/anime/', 'img.anili.st/media/')
        thumb = image or None
        ms_g = f"**Name**: **{response['title']['romaji']}**(`{response['title']['native']}`)\n**ID**: `{response['id']}`"
        if response['nextAiringEpisode']:
            airing_time = response['nextAiringEpisode']['timeUntilAiring'] * 1000
            airing_time_final = t(airing_time)
            in_des = f"Episode {response['nextAiringEpisode']['episode']} Airing in {airing_time_final}"
            ms_g += f"\n**Episode**: `{response['nextAiringEpisode']['episode']}`\n**Airing In**: `{airing_time_final}`"
        else:
            in_des = "N/A"
            ms_g += f"\n**Episode**:{response['episodes']}\n**Status**: `N/A`"
        answers.append(InlineQueryResultArticle(
            title=f"{response['title']['romaji']}",
            description=f"{in_des}",
            input_message_content=InputTextMessageContent(f"{ms_g}[⁠ ⁠]({image})", parse_mode="markdown", disable_web_page_preview=False),
            reply_markup=buttons,
            thumb_url=thumb))
        await client.answer_inline_query(query.id,
                                        results=answers,
                                        cache_time=0,
                                        is_gallery=False
                                        )
    elif string.split()[0] == "character":
        if len(string.split()) == 1:
            await client.answer_inline_query(query.id,
                                            results=answers,
                                            switch_pm_text="Get Character Info",
                                            switch_pm_parameter="start"
                                            )
            return
        search = string.split(None, 1)[1]
        variables = {'query': search}
        json = requests.post(url, json={'query': character_query, 'variables': variables}).json()['data']['Character']
        if json:
            ms_g = f"**{json.get('name').get('full')}**(`{json.get('name').get('native')}`)\n❤️ Favourites : {json['favourites']}\n"
            description = f"{json['description']}"
            site_url = json.get('siteUrl')
            ms_g += shorten(description, site_url)
            image = json.get('image', None)
            if image:
                image = image.get('large')
                answers.append(InlineQueryResultPhoto(
                    caption=ms_g,
                    photo_url=image,
                    parse_mode="markdown",
                    title=f"{json.get('name').get('full')}",
                    description=f"❤️{json['favourites']}",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("More Info", url=site_url)]])))
            else:
                answers.append(InlineQueryResultArticle(
                    title=f"{json.get('name').get('full')}",
                    description=f"{json['favourites']}",
                    input_message_content=InputTextMessageContent(ms_g, parse_mode="markdown", disable_web_page_preview=True),
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("More Info", url=site_url)]])))
            await client.answer_inline_query(query.id,
                                            results=answers,
                                            cache_time=0,
                                            is_gallery=False
                                            )
