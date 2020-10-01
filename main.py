# -*- coding: utf-8 -*-
import random

from vkwave.api import BotSyncSingleToken, API
from vkwave.bots import SimpleLongPollBot, BaseEvent
from vkwave.client import AIOHTTPClient

import config
import settings
from config import raw_bot_token, group_id, raw_wall_token
from util import wrap_attachments

# A bot object (LongPoll) to check updates.
bot = SimpleLongPollBot(tokens=raw_bot_token, group_id=group_id)

# A bot api wrapper. Main api to work with.
bot_api = API(tokens=BotSyncSingleToken(raw_bot_token), clients=AIOHTTPClient()).get_context()

# An api wrapper to work with wall. VK restricts that when using a group token.
wall_api = API(tokens=BotSyncSingleToken(raw_wall_token), clients=AIOHTTPClient()).get_context()


@bot.message_handler(settings.random_post_trigger)
async def send_random_post(event: BaseEvent):
    message_text = event.object.object.message.text
    owner_id = '-' + str(group_id)

    if len(message_text.split()) > 1:
        # If we've found that command is followed by some text, then search posts with it.
        query = ' '.join(message_text.split()[1:])
        posts = await wall_api.wall.search(query=query, owner_id=owner_id)
        tag = config.selection_types['custom'].format(query)
    else:
        # Otherwise, just select a random post.
        posts = await wall_api.wall.get(owner_id=owner_id)
        tag = config.selection_types['all']

    if not posts.response.items:
        # If nothing was found, we notice the user.
        await event.api_ctx.messages.send(
            peer_id=event.object.object.message.peer_id,
            message=config.no_posts_template,
            random_id=0
        )
        return

    feed = random.choice(posts.response.items)
    link = F"https://vk.com/wall{owner_id}_{feed.id}"

    await event.api_ctx.messages.send(
        peer_id=event.object.object.message.peer_id,
        message=config.post_template.format(link, tag, feed.text),
        attachment=wrap_attachments(feed.attachments),
        random_id=0
    )


@bot.message_handler(settings.welcome_trigger)
async def say_hello(event: BaseEvent) -> str:
    raw_users = await event.api_ctx.users.get(user_ids=[event.object.object.message.from_id])
    if raw_users is not None and len(raw_users.response) != 0:
        first_name = raw_users.response[0].first_name
    else:
        # I actually don't know in which cases this may occur.
        first_name = '?'

    return config.welcome_template.format(first_name)


bot.run_forever()
