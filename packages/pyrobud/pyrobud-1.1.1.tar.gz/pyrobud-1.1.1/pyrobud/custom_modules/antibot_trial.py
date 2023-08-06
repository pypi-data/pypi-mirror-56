import asyncio
import string
from datetime import timezone, timedelta

import aiohttp
import telethon as tg

from .. import command, module, util


class AntibotTrialModule(module.Module):
    name = "Antibot Trial"

    suspicious_keywords = [
        "investment",
        "profit",
        "binance",
        "binanse",
        "bitcoin",
        "testnet",
        "bitmex",
        "wealth",
        "mytoken",
    ]

    suspicious_entities = [
        tg.types.MessageEntityUrl,
        tg.types.MessageEntityTextUrl,
        tg.types.MessageEntityEmail,
        tg.types.MessageEntityPhone,
        tg.types.MessageEntityCashtag,
    ]

    async def on_load(self):
        self.db = self.bot.get_db("antibot_trial")
        self.user_db = self.db.prefixed_db("users.")

        if not await self.db.has("first_msg_start_time"):
            await self.db.put("first_msg_start_time", util.time.sec())
        if not await self.db.has("enabled"):
            await self.db.put("enabled", False)

    def msg_has_suspicious_entity(self, msg):
        if not msg.entities:
            return False

        # Messages containing certain entities are more likely to be spam
        for entity in msg.entities:
            if entity.__class__ in self.__class__.suspicious_entities:
                return True

        return False

    def msg_has_suspicious_keyword(self, msg):
        if not msg.raw_text:
            return False

        # Many spam messages mention certain keywords, such as cryptocurrency exchanges
        l_text = msg.raw_text.lower()
        for kw in self.__class__.suspicious_keywords:
            if kw in l_text:
                return True

        return False

    def msg_content_suspicious(self, msg):
        # Consolidate message content checks
        return self.msg_has_suspicious_entity(msg) or self.msg_has_suspicious_keyword(msg)

    def msg_type_suspicious(self, msg):
        return msg.contact or msg.geo or msg.game

    async def msg_data_is_suspicious(self, msg):
        incoming = not msg.out
        has_date = msg.date
        forwarded = msg.forward

        # Message *could* be suspicious if we didn't send it
        # Check for a date to exonerate empty messages
        if incoming and has_date:
            # Lazily evalulate suspicious content as it is more expensive
            if forwarded:
                # Messages forwarded from a linked channel by Telegram don't have a sender
                # We can assume these messages are safe since only admins can link channels
                sender = await msg.get_sender()
                if sender is None:
                    return False

                # Spambots don't forward their own messages; they mass-forward
                # messages from central coordinated channels for maximum efficiency
                # This protects users who forward questions with links/images to
                # various support chats asking for help (arguably, that's spammy,
                # but it's not what we're defending against here)
                if msg.forward.from_id == sender.id or msg.forward.from_name == tg.utils.get_display_name(sender):
                    return False

                # Screen forwarded messages more aggressively
                return msg.photo or self.msg_type_suspicious(msg) or self.msg_content_suspicious(msg)
            else:
                # Skip suspicious entity/photo check for non-forwarded messages
                return self.msg_type_suspicious(msg) or self.msg_has_suspicious_keyword(msg)

        return False

    async def msg_is_suspicious(self, msg):
        # Check if the data in the message is suspicious
        if not await self.msg_data_is_suspicious(msg):
            return False

        # Load message metadata entities
        chat = await msg.get_chat()
        sender = await msg.get_sender()

        # Messages forwarded from a linked channel by Telegram don't have a sender
        # We can assume these messages are safe since only admins can link channels
        if sender is None:
            return False

        # Load group-specific user information
        try:
            ch_participant = await self.bot.client(tg.tl.functions.channels.GetParticipantRequest(chat, sender))
        except tg.errors.UserNotParticipantError:
            # Something else already banned the bot; we don't need to proceed
            return False
        except ValueError:
            # For some reason we don't have the access hash
            # Try loading participants to get it
            await self.bot.client.get_participants(chat)
            try:
                ch_participant = await self.bot.client(tg.tl.functions.channels.GetParticipantRequest(chat, sender))
            except ValueError as e:
                # Even that didn't help, maybe the user deleted their account; bail out
                self.log.warning(f"Unable to fetch information for user {sender.id} in group {chat.id}", exc_info=e)

        participant = ch_participant.participant

        # Exempt the group creator
        if isinstance(participant, tg.tl.types.ChannelParticipantCreator):
            return False

        delta = msg.date - participant.date
        if delta.total_seconds() <= await self.db.get("threshold_time", 30):
            # Suspicious message was sent shortly after joining
            return True

        join_time_sec = int(participant.date.replace(tzinfo=timezone.utc).timestamp())
        if join_time_sec > await self.db.get(f"first_msg_start_time"):
            # We started tracking first messages in this group before the user
            # joined, so we can run the first message check
            if not await self.user_db.get(f"{sender.id}.has_spoken_in_{msg.chat_id}", False):
                # Suspicious message was the user's first message in this group
                return True

        # Allow this message
        return False

    def profile_check_invite(self, user):
        # Some spammers have Telegram invite links in their first or last names
        return "t.me/" in user.first_name or (user.last_name and "t.me/" in user.last_name)

    async def user_is_suspicious(self, user):
        # Some spammers have invites in their names
        if self.profile_check_invite(user):
            return True

        # No profile checks matched; exonerate this user
        return False

    async def take_action(self, event, user):
        chat = await event.get_chat()
        try:
            sender = await event.get_sender()
        except AttributeError:
            sender = None

        # Log the event
        self.log.info(f'Detected spambot with ID {user.id} in group "{chat.title}"')
        await self.db.inc("num_flagged")
        num_flagged = await self.db.get("num_flagged")

        # Upload event data to del.dog
        full_data = f"""Event: {event.stringify()}

Chat: {chat.stringify()}

Sender: {sender.stringify() if sender else '`None`'}"""
        async with self.bot.http_session.post("https://del.dog/documents", data=full_data) as resp:
            try:
                resp_data = await resp.json()
            except aiohttp.ContentTypeError:
                dog_url = "(unavailable due to del.dog issues)"

            dog_url = f'https://del.dog/{resp_data["key"]}'

        # Send message to the channel
        evt_url = f"https://t.me/c/{chat.id}/"
        await self.bot.client.send_message(
            1251752449,
            f"""❯❯ **Detected spambot** with ID `{user.id}` (First `{user.first_name}` Last `{user.last_name}` — @{user.username} — [profile](tg://user?id={user.id})) in group `{chat.title}`
[Context]({evt_url}{event.id}) [-2]({evt_url}{event.id - 2}) [-1]({evt_url}{event.id - 1}) [+1]({evt_url}{event.id + 1}) [+2]({evt_url}{event.id + 2})
Total flagged: {num_flagged}

Full event data: {dog_url}""",
            schedule=timedelta(seconds=10),
        )

    async def is_enabled(self, event):
        return event.is_group and await self.db.get("enabled", False)

    async def on_message(self, msg):
        # Only run in groups where antibot is enabled
        if await self.is_enabled(msg):
            if await self.msg_is_suspicious(msg):
                # This is most likely a spambot, take action against the user
                user = await msg.get_sender()
                await self.take_action(msg, user)
            else:
                await self.user_db.put(f"{msg.sender_id}.has_spoken_in_{msg.chat_id}", True)

    async def clear_group(self, group_id):
        async for key, _ in self.user_db:
            if key.endswith(f".has_spoken_in_{group_id}"):
                await self.user_db.delete(key)

    async def clear_all(self):
        async for key, _ in self.db:
            await self.db.delete(key)

    async def on_chat_action(self, action):
        # Remove has-spoken-in flag for departing users
        if action.user_left and await self.is_enabled(action):
            await self.user_db.delete(f"{action.user_id}.has_spoken_in_{action.chat_id}")

            # Clean up antibot data if we left the group
            if action.user_id == self.bot.uid:
                self.log.info(f"Cleaning up settings for group {action.chat_id}")
                await self.clear_group(action.chat_id)

            return

        # Only filter new users
        if not action.user_added and not action.user_joined:
            return

        # Only act in groups where this is enabled
        if not await self.is_enabled(action):
            return

        # Fetch the user's data and run checks
        user = await action.get_user()
        if await self.user_is_suspicious(user):
            # This is most likely a spambot, take action against the user
            await self.take_action(action, user)

    @command.desc("Toggle the antibot global trial mode")
    async def cmd_abtrial(self, msg):
        state = not await self.db.get("enabled", False)

        if state:
            await self.db.put("enabled", True)
        else:
            await self.clear_all()

        status = "enabled" if state else "disabled"
        return f"Antibot global trial mode is now **{status}**."
