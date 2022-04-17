from discord.ext import commands
from discord import *
import asyncio
import os

prefix = '!'
bot = commands.Bot(command_prefix = prefix)

class XP:
  def __init__(self, User, experiencia):
      self.user = User
      self.experiencia = experiencia

lista_usuarios = list()

@bot.command()
async def votacao(ctx, *emojis):
  msg = await ctx.send('Votação iniciada!')
  if emojis:
    for emoji in emojis:
      await msg.add_reaction(emoji)
  else:
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')

  await asyncio.sleep(10)
  msg_cached = utils.get(bot.cached_messages, id = msg.id)
  count_max = 0
  winners =[]
  #pego o maior numero de votos
  for reaction in msg_cached.reactions:
    if reaction.count > count_max:
      count_max = reaction.count
  
  if count_max == 1:
    await ctx.send('Ninguem votou...')
  else:
    #pego os vencedores
    winners = list(filter(lambda reaction: reaction.count == count_max, msg_cached.reactions))
    winners_str = ' '.join(str(winner) for winner in winners)
    await ctx.send(f'O(s) vencedor(es) da votação: {winners_str}')

  

@bot.command()
async def change_pfx(ctx, new_prefix):
  await ctx.send(f"O prefixo mudou de {bot.command_prefix} para {new_prefix}...")
  bot.command_prefix = new_prefix


@bot.command()
async def irritar(ctx, arg : Member):
  spam = '\t'.join(f"<@{arg.id}>" for _ in range(10))
  for _ in range(10):
    await ctx.send(spam)
  

@bot.command()
async def perturbar(ctx, arg : Member):
  cabecalho = f'Requisitado por: {ctx.message.author}'
  spam ='\t'.join(f"<@{arg.id}>" for _ in range(10))
  for _ in range(10):
    await arg.send(spam)
  await arg.send(cabecalho)
  await ctx.send(f"<@{arg.id}> foi pertubado com sucesso, {ctx.message.author}.")


@bot.command()
async def corazon(ctx):
    corazon = [
  '                 ██████████▄▄             ',
  '               ▀▀▀   ██   ▀▀▀             ',
  '       ▄██▄   ▄▄████████████▄▄   ▄██▄     ',
  '     ▄███▀  ▄████▀▀▀    ▀▀▀████▄  ▀███▄   ',
  '    ████▄ ▄███▀              ▀███▄ ▄████  ',
  '   ███▀█████▀▄████▄      ▄████▄▀█████▀███ ',
  '   ██▀  ███▀ ██████      ██████ ▀███  ▀██ ',
  '    ▀  ▄██▀  ▀████▀  ▄▄  ▀████▀  ▀██▄  ▀  ',
  '       ███           ▀▀           ███     ',
  '       ██████████████████████████████     ',
  '   ▄█  ▀██  ███   ██    ██   ███  ██▀  █▄ ',
  '   ███  ███ ███   ██    ██   ███▄███  ███ ',
  '   ▀██▄████████   ██    ██   ████████▄██▀ ',
  '    ▀███▀ ▀████   ██    ██   ████▀ ▀███▀  ',
  '     ▀███▄  ▀███████    ███████▀  ▄███▀   ',
  '       ▀███    ▀▀██████████▀▀▀   ███▀     ',
  '         ▀    ▄▄▄    ██    ▄▄▄    ▀       ',
  '               ▀████████████▀             ']
    for line in corazon:
        await ctx.send(line)


@bot.command()
async def xp(ctx):
    usuario = list(filter(lambda usuario: usuario.user == ctx.message.author, lista_usuarios))
    if usuario:
      await ctx.send(f'O usuário {usuario[0].user.name} tem {usuario[0].experiencia} de experiência')


@bot.event
async def on_message(message):
  if message.author.bot:
    return

  usuario = list(filter(lambda usuario: usuario.user == message.author, lista_usuarios))
  if usuario:
    usuario[0].experiencia += 1
  else:
    usuario = XP(message.author, 1)
    lista_usuarios.append(usuario)

  await bot.process_commands(message)


@bot.event
async def on_ready():
  
  print(f'O bot {bot.user.name} está funcionando.')

bot.run(os.getenv('TOKEN'))
