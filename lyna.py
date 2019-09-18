import os
import discord

client = discord.Client()

token = os.environ.get('TOKEN')
new_member_role = os.environ.get('NEW_MEMBER_ROLE')
moderator_role = os.environ.get('MODERATOR_ROLE')
welcome_channel = os.environ.get('WELCOME_CHANNEL')

rules_channel = client.get_channel(os.environ.get('RULES_CHANNEL'))
welcome_message = """:sparkles: **Welcome to {0.guild.name}, {0.mention}!** :sparkles:

**Please read through #{1} before continuing.** Once you're done, please let one of the <@{2}> know your gender in order to get access to the full server.

Your options are **boys**, **girls**, **nonbinary**, and **genderfluid**. You can also specify that you're **trans** on top of the other roles to get access to the transgender-specific rooms.
"""

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    activity = discord.Activity(name='for signs of trouble', type=discord.ActivityType.listening)
    await client.change_presence(activity=activity)

@client.event
async def on_member_update(before, after):
    new_roles = (set(before.roles) - set(after.roles))

    for role in new_roles:
        if role.id == new_member_role:
            welcome_channel = client.get_channel(welcome_channel)
            await welcome_channel.send(welcome_message.format(after, rules_channel, moderator_role))

client.run(token)
