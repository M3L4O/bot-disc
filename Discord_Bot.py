from discord.ext import commands
from discord import *
from discord.ext.commands import context
from discord.ext.commands.core import command
from discord.message import Message
from discord.reaction import Reaction
from discord.user import User
from time import sleep
import os
prefix = '!'
intents = Intents.all()
intents.reactions = True
bot = commands.Bot(command_prefix = prefix, intents = intents)
class XP:
  usuario = User
  experiencia = 0
  def __init__(self):
      usuario = User
      experiencia = 0
lista_usuarios = list()

@bot.command()
async def votacao(ctx, *emojis):
  msg = await ctx.send('Votação iniciada!')
  if emojis.__len__() > 0:
    for emoji in emojis:
      await msg.add_reaction(emoji)
  else:
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')
  await asyncio.sleep(10)
  msg_cached = utils.get(bot.cached_messages, id = msg.id)
  winner = msg_cached.reactions[0]
  for reacao in msg_cached.reactions:
    if reacao.count > winner.count:
      winner = reacao
  empate = list()
  for reacao in msg_cached.reactions:
    if winner.count == reacao.count:
      empate.append(reacao.emoji)
  if empate.__len__() == 1:
    await ctx.send(f"A reação {winner.emoji} ganhou...")
  else: 
    winners = (',').join(empate)
    await ctx.send(f"Houve um empate entre {winners} com {winner.count} reações...")
  

@bot.command()
async def change_pfx(ctx, new_prefix):
  await ctx.send(f"O prefixo mudou de {bot.command_prefix} para {new_prefix}...")
  bot.command_prefix = new_prefix


@bot.command()
async def irritar(ctx, arg:Member):
  if ctx.author.id != 354037985278296064:
    return
  spam = '\t'.join(f"<@{arg.id}>" for x in range(10))
  for x in range(10):
    await ctx.send(spam)
  
@bot.command()
async def pertubar(ctx, arg:Member):
  if ctx.author.id != 354037985278296064:
    return
  spam ='\t'.join(f"<@{arg.id}>" for x in range(10))
  for x in range(30):
    await arg.send(spam)
  

@bot.command()
async def xp(ctx):
  for x in lista_usuarios:
    if x.usuario == ctx.author:
      await ctx.send(f'O usuário {ctx.author.name} tem {x.experiencia} pontos de experiência')

@bot.event
async def on_message(message):
  if message.author.bot:
    return
  else:
    if lista_usuarios.__len__() == 0:
      usuarios = XP()
      usuarios.usuario = message.author
      usuarios.experiencia += 1
      lista_usuarios.append(usuarios)
    else:
      for x in lista_usuarios:
        if message.author == x.usuario:
          x.experiencia += 1
          await bot.process_commands(message)
          return
      usuarios = XP()
      usuarios.usuario = message.author
      usuarios.experiencia += 1
      lista_usuarios.append(usuarios)
  await bot.process_commands(message)


@bot.event
async def on_ready():
  activity = Game(name=f"A morte é como o vento, está sempre ao meu lado. prefix = {prefix}", type=1)
  await bot.change_presence(status=Status.idle, activity=activity)
  print('Bot {0.user} está em execução'.format(bot))

bot.run(os.getenv('TOKEN'))
