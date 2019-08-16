# BFI
import sys
import json
import discord
import requests
from discord.ext import commands

# ---------------------------------------------------------------
# Object initialization
# --------------------------------------------------------------
TOKEN = ''

client = discord.Client()
client = commands.Bot(command_prefix='$')
client.remove_command('help')


# ---------------------------------------------------------------
# Bot Start
# --------------------------------------------------------------
# Logs Ready and sets Status at start
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


# ---------------------------------------------------------------
# Original Dad Bot Commands
# --------------------------------------------------------------

# Test Ping Command. Simplest Command in the bot
@client.command()
async def ping():
    await client.say('++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>++++++++++.>+++++++++++.-.-------.<<+++.')


# First hello command
@client.command()
async def hello():
    await client.say('++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>++.>+.+++++++..+++.')


@client.command()
async def close():
    await client.close()

# ---------------------------------------------------------------
# BrainFuck Interpreters
# --------------------------------------------------------------
# Brainfuck Command
# VARIABLES:
# prg = command (in brainfuck) (String)
def bfi(prg):
    c = [0] * 30000
    p = 0
    loop = []
    rv = []
    ts = list(prg)
    length = len(ts)
    i = 0
    while i < length:
        t = ts[i]
        if t == ">":
            p += 1
        elif t == "<":
            p -= 1
        elif t == "+":
            c[p] += 1
        elif t == "-":
            c[p] -= 1
        elif t == ".":
            rv.append(chr(c[p]))
        elif t == ",":
            pass
        elif t == "[":
            if len(loop) > 100:
                raise Exception
            if c[p] == 0:
                while ts[i] != "]": i += 1
                loop.pop()
            else:
                loop.append(i - 1)
        elif t == "]":
            if len(loop) > 100:
                raise Exception
            i = loop[-1]
        i += 1

    msg = "".join(rv)
    return msg

def hmi(prg):
    x = ""
    p = 0
    result = []
    ts = list(prg)
    length = len(ts)
    i = 0
    while i < length:
        t = ts[i]
        if t == "[":
            x = None
        elif t == "<":
            x = ""
        elif t == ">":
            x = 0
        elif t == "+":
            x += 1
        elif t == "-":
            x -= 1
        elif t == "^":
            if x == "":
                x = "a"
            else:
                ch = bytes(x, 'utf-8')
                s = bytes([ch[0] + 1])
                x = chr(s[0])
        elif t == "/":
            if x == "":
                x = "z"
            else :
                ch = x
                ch = bytes(ch, 'utf-8')
                s = bytes([ch[0] - 1])
                x = chr(s[0])
        elif t == "]":
            if x == "":
                result.append(" ")
            else:
                result.append(str(x))
        i += 1

    msg = "".join(result)
    return msg

def dsi(prg):
    x = 65
    p = 0
    result = []
    ts = list(prg)
    length = len(ts)
    i = 0
    while i < length:
        t = ts[i]
        if t == "+":
            x += 1
            if 97 > x > 90:
                x = 97
            elif x > 122:
                raise Exception
        elif t == "-":
            x -= 1
            if 90 < x < 97:
                x = 90
            elif x < 65:
                raise Exception
        elif t == "^":
            x = 65
        elif t == "%":
            x = 97
        elif t == "S":
            ch = x
            x = chr(ch)
            if x == "":
                result.append(" ")
            else:
                result.append(str(x))
            x = ch
        i += 1

    msg = "".join(result)
    return msg

def fivei(prg):
    c = [0] * 30000
    p = 0
    loop = []
    rv = []
    ts = list(prg)
    length = len(ts)
    i = 0
    while i < length:
        t = ts[i]
        if t == "+":
            p += 1
        elif t == "-":
            p -= 1
        elif t == "^":
            c[p] += 1
        elif t == "v" or t == "V":
            c[p] -= 1
        elif t == "P" or t == "p":
            rv.append(str(c[p]))
        i += 1

    msg = "".join(rv)
    return msg

def debugfivei(prg):
    c = [0] * 30000
    p = 0
    loop = []
    rv = []
    debug = []
    ts = list(prg)
    length = len(ts)
    i = 0
    while i < length:
        t = ts[i]
        if t == "+":
            p += 1
            debug.append("->")
        elif t == "-":
            p -= 1
            debug.append("<-")
        elif t == "^":
            c[p] += 1
            debug.append("^ %s" % c[p])
        elif t == "v" or t == "V":
            c[p] -= 1
            debug.append("v %s" % c[p])
        elif t == "P" or t == "p":
            rv.append(str(c[p]))
            debug.append("P")
        i += 1
    object = []
    msg = "".join(rv)
    object.append(msg)
    object.append(debug)
    return object


'''
Not quite Ready :(
And Then! Interpreter (Brainfuck + and Then!)

Problem is with and then logic at bottom.
Brainfuck interpreter works fine as far as I can tell.
Might want to check my flag logic on the loops is you are interested in giving this one a shot.

def ati(prg):
    c = [0] * 30000
    p = 0
    loop = []
    rv = []
    ts = list(prg)
    l = len(ts)
    i = 0
    msgArray = []
    bf = True
    # AndThen Variables
    andPass = False
    thenPass = False
    ctr = 0

    while i < l:
        t = ts[i]
        if bf:
            if t == ">":
                p += 1
                bf = False
            elif t == "<":
                p -= 1
                bf = False
            elif t == "+":
                c[p] += 1
                bf = False
            elif t == "-":
                c[p] -= 1
                bf = False
            elif t == ".":
                rv.append(chr(c[p]))
                pass
            elif t == ",":
                bf = False
            elif t == "[":
                if len(loop) > 100:
                    raise Exception
                if c[p] == 0:
                    while ts[i] != "]": i += 1
                    loop.pop()
                else:
                    loop.append(i - 1)
                bf = False
            elif t == "]":
                if len(loop) > 100:
                    raise Exception
                i = loop[-1]
                bf = False
        else:
            if t.lower() == "a":
                andPass = True
            elif andPass and t.lower() == "t":
                thenPass = True
            if andPass and thenPass:
                andPass = False
                thenPass = False
                bf = True
                ctr = 0
            if ctr > 2:
                raise Exception
            ctr += 1
        i += 1

    msg = "".join(rv)

    # Prints Tape if there is no message Displayed
    # It is an infinite tape after all. ;)
    # Discord can't Print Infinity
    if msg == "":
        msg = "Array Output: ["
        for x in c:
            if x != 0:
                msg += "%s, " % str(x)
        msg += "...]"
    return msg
'''

# ---------------------------------------------------------------
# BrainFuck Command
# --------------------------------------------------------------
# First hello command
@client.command()
async def bf(*, code=""):
    try:
        result = bfi(code)
        await client.say(result)
    except Exception:
        await client.say('Invalid Brainfuck Command')

'''
@client.command()
async def andThen(*, code=""):
    try:
        result = ati(code)
        await client.say(result)
    except Exception:
        await client.say('Invalid And Then! Command')
'''

# ---------------------------------------------------------------
# UnNecessary Command
# --------------------------------------------------------------
@client.command()
async def unnecessary(code="#"):
    if code == "#":
        await client.say('*')
    else:
        await client.say('Unsuccessful')

# ---------------------------------------------------------------
# Kallisti Command
# --------------------------------------------------------------
@client.command()
async def kallisti(*, msg=""):
    await client.say(msg)


# ---------------------------------------------------------------
# HQ9+ Interpreter
# --------------------------------------------------------------
@client.command()
async def hq9plus(*, msg=""):
    messagecount = 0
    try:
        while messagecount < 10:
            for x in msg:
                if x == "h":
                    await client.say("Hello World! :)")
                    messagecount += 1
                if x == "q":
                    await client.say(msg)
                    messagecount += 1
                if x == "9":
                    bottles = 99
                    while bottles > 97:
                        message = "%s bottles of beer on the wall! %s bottles of beer!" % (bottles, bottles)
                        await client.say(message)
                        bottles -= 1
                        message = "Take one down, and pass it around, %s bottles of beer on the wall!" % bottles
                        await client.say(message)
                    await client.say("....and So On")
                    messagecount += 1
                if x == "+":
                    with open('index.json', 'r') as f:
                        index = json.load(f)
                    index['index'] += 1
                    message = "Accumulator is now at %s" % index['index']
                    await client.say(message)
                    messagecount += 1
                    with open('index.json', 'w') as f:
                        json.dump(index, f)
            break
        if messagecount >= 10:
            message = "Please do not make such big programs. No one likes spam."
            await client.say(message)
    except Exception:
        await client.say("Invalid HQ9+ command!")

# ---------------------------------------------------------------
#hatemath Interpreter
# --------------------------------------------------------------
@client.command()
async def hatemath(*, code=""):
    try:
        result = hmi(code)
        await client.say(result)
    except Exception:
        await client.say('Invalid Hatemath Command')

# ---------------------------------------------------------------
#DeadSimple Interpreter
# --------------------------------------------------------------
@client.command()
async def deadsimple(*, code=""):
    try:
        result = dsi(code)
        await client.say(result)
    except Exception:
        await client.say('Invalid DeadSimple Command')

# ---------------------------------------------------------------
#5command Interpreter
# --------------------------------------------------------------
@client.command()
async def fivecommand(*, code=""):
    try:
        result = fivei(code)
        await client.say(result)
    except Exception:
        await client.say('Invalid 5command Command')

@client.command()
async def debugfivecommand(*, code=""):
    try:
        object = debugfivei(code)
        await client.say("Result : %s" % object[0])
        await client.say("Debug : %s" % object[1])
    except Exception:
        await client.say('Invalid 5command Command')

# ---------------------------------------------------------------
# Help Function
# --------------------------------------------------------------
@client.command(pass_context=True)
async def help(ctx, msg="help"):
    author = ctx.message.author

    if msg == "help":
        embed = discord.Embed(
            colour=discord.Colour.orange()
        )
        embed.set_author(name='Help')
        embed.add_field(name='$ping', value='Returns pong in Brainfuck', inline=False)
        embed.add_field(name='$hi', value='Returns hello in Brainfuck', inline=False)
        embed.add_field(name='$bf <code>', value='Interpreter that Runs Brainfuck Programs', inline=False)
        embed.add_field(name='$kallisti <code>', value='Interpreter that Runs Kallisti Programs', inline=False)
        embed.add_field(name='$unnecessary <code>', value='Interpreter that Runs Unnecessary Programs', inline=False)
        embed.add_field(name='$hq9plus <code>', value='Interpreter that Runs HQ9+ Programs', inline=False)
        embed.add_field(name='$hatemath <code>', value='Interpreter that Runs hatemath Programs', inline=False)
        embed.add_field(name='$deadsimple <code>', value='Interpreter that Runs DeadSimple Programs', inline=False)
        embed.add_field(name='$fivecommand <code>', value='Interpreter that Runs 5command Programs', inline=False)
        embed.add_field(name='$help', value='Returns this embed', inline=False)
        embed.add_field(name='$help <command>', value='Returns information about that commands language. ex #help bf',
                        inline=False)
        await client.say(embed=embed)
        # await client.send_message(author, embed=embed)
    elif msg == "bf":
        embed = discord.Embed(
            colour=discord.Colour.red()
        )
        embed.set_author(name='BrainFuck')
        embed.add_field(name='More Information:', value='https://esolangs.org/wiki/brainfuck', inline=False)
        embed.add_field(name='English-to-Brainfuck Converter:', value='https://www.dcode.fr/brainfuck-language',
                        inline=False)
        embed.add_field(name='There are only 8 symbols allowed.', value='-------------------------------', inline=False)
        embed.add_field(name='>', value='Move to Next Element', inline=False)
        embed.add_field(name='<', value='Move to Previous Element', inline=False)
        embed.add_field(name='+', value='Increment Current Element', inline=False)
        embed.add_field(name='-', value='Decrement Current Element', inline=False)
        embed.add_field(name=',', value='Await Input(Currently Not Implemented)', inline=False)
        embed.add_field(name='.', value='Output Current Element(in ASCII)', inline=False)
        embed.add_field(name='[', value='Jump past matching ] if Element is 0', inline=False)
        embed.add_field(name=']', value='Jump back to matching [ if Element is not 0', inline=False)
        embed.add_field(name='---', value='All Other Commands are Ignored', inline=False)
        await client.say(embed=embed)
    elif msg == "kallisti":
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(name='Kallisti')
        embed.add_field(name='EsoLangs.org Link:', value="https://bit.ly/2SdwN4b", inline=False)
        embed.add_field(name='<anything> ::= <anything>', value='-------------------------------', inline=False)
        embed.add_field(name='Rule 1:', value="Obey as many rules as possible", inline=False)
        embed.add_field(name='Rule 2:', value="There is plenty nothing", inline=False)
        embed.add_field(name='Rule 3:', value="Everything is true", inline=False)
        embed.add_field(name='Rule 4:', value="Everything is false", inline=False)
        embed.add_field(name='Rule 5:', value="There is only nothing", inline=False)
        embed.add_field(name='Rule 6:', value="Obey as few rules as possible", inline=False)
        await client.say(embed=embed)
    elif msg == "unnecessary":
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(name='Unnecessary')
        embed.add_field(name='Official Site', value='http://yiap.nfshost.com/esoteric/unnecessary/unnecessary.html',
                        inline=False)
        embed.add_field(name='Esolangs.org Link:', value='https://esolangs.org/wiki/unnecessary', inline=False)
        embed.add_field(name='TL;DR', value='-------------------------------', inline=False)
        embed.add_field(name='Rule 1:', value='If a program file exists, report error and fail', inline=False)
        embed.add_field(name='Rule 2:',
                        value='If no program file exists, create program with NOP(No Operation) instruction',
                        inline=False)
        await client.say(embed=embed)
    elif msg == "hq9plus":
        embed = discord.Embed(
            colour=discord.Colour.orange()
        )
        embed.set_author(name='HQ9+')
        embed.add_field(name='Official Site', value='https://goo.gl/jKpbSk',
                        inline=False)
        embed.add_field(name='Esolangs.org Link:', value='https://esolangs.org/wiki/HQ9%2B', inline=False)
        embed.add_field(name='There are only 4 symbols allowed.', value='-------------------------------', inline=False)
        embed.add_field(name='h', value='Prints Hello World', inline=False)
        embed.add_field(name='q', value='Print Source Code(Quine)', inline=False)
        embed.add_field(name='9', value='Starts 99 Bottles of Beer on the wall', inline=False)
        embed.add_field(name='+', value='Increments the counter that is always running.', inline=False)
        embed.add_field(name='Example:', value='code: qhq prints \"qhq\",\"Hello World! :)\",\"qhq\"', inline=False)
        await client.say(embed=embed)
    elif msg == "hatemath":
        embed = discord.Embed(
            colour=discord.Colour.red()
        )
        embed.set_author(name='hatemath')
        embed.add_field(name='Esolangs.org Link:', value='https://esolangs.org/wiki/Hatemath', inline=False)
        embed.add_field(name='There are only 8 symbols, working on 1 variable named x', value='-------------------------------', inline=False)
        embed.add_field(name='[', value='Sets type of X to None', inline=False)
        embed.add_field(name='<', value='Sets type of X to \'\'', inline=False)
        embed.add_field(name='>', value='Sets type of X to 0', inline=False)
        embed.add_field(name='+', value='Increment if it is an integer', inline=False)
        embed.add_field(name='-', value='Decrement if it is an integer', inline=False)
        embed.add_field(name='^', value='Move forward in alphabet(Only lowercase supported)', inline=False)
        embed.add_field(name='/', value='Move down the alphabet(Only lowercase supported)', inline=False)
        embed.add_field(name=']', value='Print Value', inline=False)
        await client.say(embed=embed)

    elif msg == "deadsimple":
        embed = discord.Embed(
            colour=discord.Colour.dark_blue()
        )
        embed.set_author(name='DeadSimple')
        embed.add_field(name='Esolangs.org Link:', value='https://esolangs.org/wiki/DeadSimple', inline=False)
        embed.add_field(name='There are only 4 symbols allowed. Starts at A', value='-------------------------------', inline=False)
        embed.add_field(name='+', value='Move up Alphabet', inline=False)
        embed.add_field(name='-', value='Move down Alphabet', inline=False)
        embed.add_field(name='S', value='Print', inline=False)
        embed.add_field(name='_', value='Reset to 0(see Note Below)', inline=False)
        embed.add_field(name='Note:', value='Because of message limits, to cut down on input, I added two replacements for _', inline=False)
        embed.add_field(name='^', value='Start at Uppercase A', inline=False)
        embed.add_field(name='%', value='Start at Lowercase a', inline=False)
        embed.add_field(name='Example: S%+S^++S', value='Output: AbC', inline=False)
        await client.say(embed=embed)
    elif msg == "fivecommand":
        embed = discord.Embed(
            colour=discord.Colour.purple()
        )
        embed.set_author(name='5command')
        embed.add_field(name='Esolangs.org Link:', value='https://esolangs.org/wiki/5command', inline=False)
        embed.add_field(name='There are only 5 symbols allowed.', value='-------------------------------', inline=False)
        embed.add_field(name='+', value='Move pointer right on the tape', inline=False)
        embed.add_field(name='-', value='Move pointer left on the tape', inline=False)
        embed.add_field(name='^', value='Increments current cell at pointer', inline=False)
        embed.add_field(name='v', value='Decrements current cell at pointer', inline=False)
        embed.add_field(name='P', value='Prints current cell at pointer', inline=False)
        embed.add_field(name='Example: ^p+^^^p+^^^p+^^^^^^^p', value='Output: 1337', inline=False)
        embed.add_field(name='Note:', value='If you want to see debug logs, call program with $debugfivecommands', inline=False)
        await client.say(embed=embed)
    elif msg == "debugfivecommand":
        embed = discord.Embed(
            colour=discord.Colour.purple()
        )
        embed.set_author(name='Debug version of 5command')
        embed.add_field(name='Esolangs.org Link:', value='https://esolangs.org/wiki/5command', inline=False)
        embed.add_field(name='-------------------------------', value='Returns a Debug Log Along with a message', inline=False)
        embed.add_field(name='There are only 5 symbols allowed.', value='-------------------------------', inline=False)
        embed.add_field(name='+', value='Move pointer right on the tape', inline=False)
        embed.add_field(name='-', value='Move pointer left on the tape', inline=False)
        embed.add_field(name='^', value='Increments current cell at pointer', inline=False)
        embed.add_field(name='v', value='Decrements current cell at pointer', inline=False)
        embed.add_field(name='P', value='Prints current cell at pointer', inline=False)
        embed.add_field(name='Example: ^p+^^^p+^^^p+^^^^^^^p', value='Output: 1337', inline=False)
        await client.say(embed=embed)
    else:
        await client.say("Invalid Command")


client.run(TOKEN)
