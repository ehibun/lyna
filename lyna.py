import os
import discord
import logging

logging.basicConfig(level=logging.INFO)

intents = discord.Intents(guilds = True, members = True)
client = discord.Client(intents=intents)

token = os.environ.get('TOKEN')

new_member_role = int(os.environ.get('NEW_MEMBER_ROLE'))
moderator_role = int(os.environ.get('MODERATOR_ROLE'))

welcome_channel = int(os.environ.get('WELCOME_CHANNEL'))
rules_channel = int(os.environ.get('RULES_CHANNEL'))

welcome_message = """:sparkles: **Welcome to {0.guild.name}, {0.mention}!** :sparkles:

**Please read through <#{1}> before continuing.** Once you're done, please let us know your gender in order to access the rest of the server. You can do this by posting in this channel, or by sending a DM to a <@&{2}> if you would prefer.

We support a wide variety of gender roles for you to choose from - the most common are **boys**, **girls**, and **nonbinary**, and you can see a full list by typing `?roles` into this channel. You can pick more than one if you prefer, and you can also specify that you're **trans** on top of any other gender identities to get access to transgender-specific rooms.

Once you have access to the server, you can choose your own roles to display your pronouns, sexuality, and so on.
"""


@client.event
async def on_ready():
    logging.info('We have logged in as {0.user}'.format(client))
    activity = discord.Activity(
        name='tales of the Warrior of Darkness', type=discord.ActivityType.listening)
    await client.change_presence(activity=activity)


@client.event
async def on_member_update(prev_user, user):
    removed_roles = (set(prev_user.roles) - set(user.roles))

    for role in removed_roles:
        if role.id == new_member_role:
            try:
                channel = client.get_channel(welcome_channel)
                message = welcome_message.format(
                    user, rules_channel, moderator_role,)

                await channel.send(message)
                logging.info('Welcomed {0.name} successfully.'.format(user))
                return
            except Forbidden:
                logging.error(
                    'We don\'t have permission to send welcome messages.')
                return
            except HTTPException:
                logging.error(
                    'Sending the message failed due to an HTTP error.')
                return
            except:
                logging.error('Something unknown has gone wrong.')
                return

client.run(token)
