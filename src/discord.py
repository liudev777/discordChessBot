import hikari
import lightbulb
import os
from dotenv import load_dotenv
from model import Model
from controller import Controller

load_dotenv()

bot = lightbulb.BotApp(
    token = os.getenv('TOKEN'),
    prefix="!"
)

@bot.listen(hikari.StartedEvent)
async def start_up_message(event):
    print("Chess bot starting")
    # await event.app.rest.create_message(847165448726118453, "hi")

msg = []

@bot.command
# @lightbulb.option('col', 'column')
# @lightbulb.option('row', 'row')
@lightbulb.command('move', 'move a piece')
@lightbulb.implements(lightbulb.SlashCommand)
async def move(ctx):
    msg.append(await bot.rest.create_message(847165448726118453, "https://fen2png.com/api/?fen=r1b1k1nr/p2p1ppp/n2B4/1p1NPN1P/6P1/3P1Q2/P1P1K3/q5b1%20w%20kq%20-%20-&raw=true"))
    msg[0]
    await ctx.respond(msg[0].channel_id, flags=hikari.MessageFlag.EPHEMERAL)
    # await s.getCtx().message().edit("hi")

messages = [
    "https://fen2png.com/api/?fen=5rk1/pp4pp/4p3/2R3Q1/3n4/2q4r/P1P2PPP/5RK1%20b%20-%20-%20-&raw=true",
    "https://fen2png.com/api/?fen=r1b1k1nr/p2p1ppp/n2B4/1p1NPN1P/6P1/3P1Q2/P1P1K3/q5b1%20w%20kq%20-%20-&raw=true"
    ]

count = 0

@bot.command
@lightbulb.command('edit', 'edit')
@lightbulb.implements(lightbulb.SlashCommand)
async def edit(ctx):
    global count
    m = msg[-1]
    num = 0
    if count % 2 == 0:
        num = 0
    else:
        num = 1

    count += 2
    await bot.rest.edit_message(m.channel_id, m.id, messages[num])
    await ctx.respond("changed", flags=hikari.MessageFlag.EPHEMERAL)

c = Controller()
@bot.command
@lightbulb.option('notation', 'input chess notation')
@lightbulb.command('ping', 'ping')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond(c.processInput(ctx.options.notation))



bot.run()