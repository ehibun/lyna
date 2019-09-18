import os
import discord
import logging

logging.basicConfig(level=logging.INFO)
client = discord.Client()

token = os.environ.get('TOKEN')

new_member_role = int(os.environ.get('NEW_MEMBER_ROLE'))
moderator_role = int(os.environ.get('MODERATOR_ROLE'))

welcome_channel = int(os.environ.get('WELCOME_CHANNEL'))
rules_channel = client.get_channel(int(os.environ.get('RULES_CHANNEL')))

welcome_message = """:sparkles: **Welcome to {0.guild.name}, {0.mention}!** :sparkles:

**Please read through #{1} before continuing.** Once you're done, please let one of the <@{2}> know your gender in order to get access to the full server.

Your options are **boys**, **girls**, **nonbinary**, and **genderfluid**. You can also specify that you're **trans** on top of the other roles to get access to the transgender-specific rooms.
"""

@client.event
async def on_ready():
    logging.info('We have logged in as {0.user}'.format(client))
    activity = discord.Activity(name='for the sound of trouble', type=discord.ActivityType.listening)
    await client.change_presence(activity=activity)

@client.event
async def on_member_update(prev_user, user):
    removed_roles = (set(prev_user.roles) - set(user.roles))

    for role in removed_roles:
        if role.id == new_member_role:
            try:
                await client.get_channel(welcome_channel).send(welcome_message.format(user, rules_channel, moderator_role))
                logging.info('Welcomed {0.name} successfully.'.format(user))
                return
            except Forbidden:
                logging.error('We don\'t have permission to send welcome messages.')
                return
            except HTTPException:
                logging.error('Sending the message failed due to an HTTP error.')
                return
            except:
                logging.error('Something unknown has gone wrong.')
                return

client.run(token)
