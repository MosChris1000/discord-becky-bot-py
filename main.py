import asyncio
from discord import Client as DiscordClient
from discord import Game, Message, Server
import config
from raven import Client as SentryClient
from raven_aiohttp import AioHttpTransport
import google_service_account
from datastore import redis_db



sentry_client = SentryClient(config.SENTRY_DSN, transport=AioHttpTransport)

class BeckyBot(DiscordClient):
    async def on_ready(self):
        """Get server and channel from discord connection"""
        print("Becky Bot Start!\n")


    async def on_error(self, event_method, *args, **kwargs):
        await super().on_error(event_method, *args, **kwargs)
        sentry_client.captureException()


    async def on_message(self, message: Message):
        """Listener about message"""
        await self.wait_until_ready()
        if message.mention_everyone == True:
            return
        if self.user not in message.mentions:
            return
        #content = str(message.content).lower()
        content = str(message.clean_content).lower()
        #print(content)
        
        if message.author == self.user:
            return
        #if content == "@becky hello":
        #    await self.send_message(message.channel, "World")
        # message: @Becky luck 1-A
        #          @Becky luck thu 1-A
        if "luke" in content:
            cmd_args = message.content.split()
            group_name = ""
            weekday = ""
            team_list = []
            errMsg = ""
            #print(message.server)
            if len(cmd_args) < 3:
                await self.send_message(message.channel, '你說什麼Becky聽不懂啦>_<')
                return
            if len(cmd_args) == 3:
                group_name = cmd_args[2]
            elif len(cmd_args) >=4:
                group_name = cmd_args[3]
                weekday = cmd_args[2]
                if weekday == "thu":
                    weekday = "Thursday"
                elif weekday == "sat":
                    weekday = "Saturday"
            
            msg = f'{group_name} 該暴打爺爺囉！\n\n'
            if len(weekday) > 0:
                errMsg, team_list = google_service_account.get_Google_sheet(group_name, weekday)
            else: 
                errMsg, team_list = google_service_account.get_Google_sheet_today(group_name)
            
            if len(errMsg) > 0:
                msg += f'錯誤: {errMsg}\n'
                if "weekday" in msg:
                    return await self.send_message(message.channel, "今天沒有打爺爺喔!\n")
                return await self.send_message(message.channel, msg)
               
            if team_list == None or len(team_list)==0:
                return await self.send_message(message.channel, "這團沒有排人，爺爺平安喜樂！\n")

            for t_index, party_list in enumerate(team_list):
                msg += f'{t_index+1} 隊:\n'
                for player_with_job in party_list:
                    if not player_with_job:
                        continue
                    player = player_with_job["player"]
                    job = player_with_job["job"]
                    discord_id = redis_db.hget(player, 'discord_id')
                    character_name = redis_db.hget(player, job)

                    if discord_id != None:
                        member = message.server.get_member(discord_id)
                        player = member.mention if member is not None else player
                        #msg += f' id:{discord_id} member: {member} player: {player}'

                    msg+=f'{player} 出 {job}'
                    #log_msg = f'{player} 出 {job}\n'
                    #print(log_msg)
                    if character_name != None:
                        msg += f' [{character_name}]'
                        
                    msg += '\n'
                msg += '\n'
            await self.send_message(message.channel, msg)
            return await self.change_presence(game=Game(name=f'Luke {group_name} 團，出征！'))
            #print(msg)
                    


async def main():
    becky_bot = BeckyBot()
    sentry_client = SentryClient(config.SENTRY_DSN, transport=AioHttpTransport)

    future_tasks = [
        becky_bot.start(config.DISCORD_TOKEN),

        sentry_client.remote.get_transport().close()
    ]

    return await asyncio.gather(*future_tasks)

if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(main())