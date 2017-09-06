from config import THE100_TOKEN, DISCORD_TOKEN

import asyncio, discord, re, the100io

client = discord.Client()
the100 = the100io.the100io(THE100_TOKEN)

COMMAND_PATTERN = re.compile("^!\s?([\w]+)(\s?.*)$")

@client.event
async def on_ready():
    print('Logged in as: %s (%s)' % (client.user.name, client.user.id))

@client.event
async def on_message(message):
    if message.channel.name != "dev":
        print (message.channel.id)
        print("Message received for ignored channel: '%s'" % (message.channel.name))

    elif re.match(COMMAND_PATTERN, message.content):
        print("Received command: %s" % (message.content))
        matches = re.match(COMMAND_PATTERN, message.content)
        cmd = matches.group(1)
        args = matches.group(2)

        func = None

        try:
            func = globals()[cmd]
        except KeyError:
            print("'%s' is an unknown command" % (cmd))
            await client.send_message(message.channel, "Unknown command.")
            return

        # call the function with the same name as the command
        await func(message, args)

async def ping(message, args):
    print("Pong!")
    await client.send_message(message.channel, "Pong!")

# Local testing
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

#loop = asyncio.get_event_loop()
# Blocking call which returns when the hello_world() coroutine is done
#loop.run_until_complete(on_message(AttrDict({"channel": AttrDict({"name": "dev", "id": "local"}), "content": "!ping"})))
#loop.close()

client.run(DISCORD_TOKEN)
