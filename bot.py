from discord.ext import commands
from discord.ext.commands import Bot
from discord import (
    Embed, 
    Member, 
    Intents, 
    Colour, 
    Activity, 
    ActivityType,
)

from googlesearch import search
import datetime
import random


bot: Bot = commands.Bot(
    command_prefix=["m, ", "macaco, "],
    intents=Intents.all(),
    help_command=None
)

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=Activity(type=ActivityType.listening, name="m, help")
    )

    print(f'Logado como {bot.user} (ID: {bot.user.id if bot.user is not None else bot.user})')


@bot.command(
    brief="Retorna ping.", 
    description="Retorna o ping do bot."
)
async def ping(ctx):
    embed: Embed = Embed(colour=Colour.green())

    embed.add_field(
        name="",
        value=f"""
            Pong! 
            Latência: **{round(bot.latency * 1000)}ms**
        """,
        inline=False
    )

    await ctx.send(embed=embed)


@bot.command(
    name="help",
    brief="Mostra os comandos do bot.",
    description="""
        `help`: Retorna todos os comandos do bot e uma descrição breve da cada um.
        `help [comando]`: Retorna a descrição de um comando em específico.
    """
)
async def bot_help(ctx, comm: str | None = None):
    embed: Embed
    
    if comm is not None:
        c = bot.get_command(comm)

        if c is not None:
            embed = Embed(
                title=f"`{c.name}`",
                colour=Colour.yellow(),
                timestamp=datetime.datetime.now(),
            )

            embed.add_field(
                name="",
                value="{}".format(c.description),
                inline=False
            )
        else:
            embed = Embed(colour=Colour.red())

            embed.add_field(
                name="",
                value="**:x: O comando informado não existe!**",
                inline=False
            )
    else:
        embed = Embed(
            title=f"{ctx.author.nick if ctx.author.nick else ctx.author.name}, aqui está a lista de comandos: ",
            colour=Colour.yellow(),
        )

        comms_desc: str = ""

        for c in bot.walk_commands():
            comms_desc += f"`{c.name}` - {c.brief}\n"

        embed.add_field(
            name="",
            value=comms_desc, 
            inline=False
        )

    await ctx.send(embed=embed)


@bot.command(
    name="userinfo",
    brief="Retorna informação de um usuário em específico.",
    description="""
        `userinfo`: Retorna as informações do próprio usuário.
        `userinfo @[nome/nick]`: Retorna as informações de um usuário em específico.
    """
)
async def user_info(ctx, member: Member | None = None):
    if member:
        target: Member = member
    else:
        target: Member = ctx.author

    embed: Embed = Embed(
        title=f"Informações de {target.name}",
        colour=target.colour,
    )

    embed.set_thumbnail(url=target.avatar)
    embed.add_field(
        name="Nome: ", 
        value=target.name, 
        inline=False
    )
    embed.add_field(
        name="É um bot? ",
        value="Sim" if target.bot else "Não",
        inline=False
    )
    embed.add_field(
        name="Status: ",
        value=str(target.status).title() if str(target.status) != "dnd" else "Não pertube",
        inline=False
    )
    embed.add_field(
        name="Atividade: ",
        value=f"{str(target.activity.type).split('.')[-1].title()} {target.activity.name}" if target.activity else f"{target.nick if target.nick else target.name} não está em nenhuma atividade no momento!",
        inline=False
    )

    await ctx.send(embed=embed)


@bot.command(
    name="serverinfo",
    brief="Retorna informações sobre o server.",
    description="""
        `serverinfo`: Retorna as informações gerais do servidor em que o comando for usado.
    """
)
async def server_info(ctx):
    embed = Embed(
        title="Informação de {}".format(ctx.guild.name),
        colour=ctx.guild.owner.colour,
    )

    status = [
        len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
        len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
        len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
        len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))
    ]

    embed.set_thumbnail(url=ctx.guild.icon)
    embed.add_field(
        name="Criado em: ",
        value=ctx.guild.created_at.strftime("%d/%m/%Y"),
        inline=False
    )
    embed.add_field(
        name="Total de membros: ",
        value=len(ctx.guild.members),
        inline=False
    )
    embed.add_field(
        name="Total de humanos: ",
        value=len(list(filter(lambda m: not m.bot, ctx.guild.members))),
        inline=False
    )
    embed.add_field(
        name="Total de bots: ",
        value=len(list(filter(lambda m: m.bot, ctx.guild.members))),
        inline=False
    )
    embed.add_field(
        name="Status: ",
        value=f"""
            :green_circle: {status[0]} 
                
            :yellow_circle: {status[1]} 
                    
            :red_circle: {status[2]} 
                    
            :black_circle: {status[3]}
        """,
        inline=False
    )

    await ctx.send(embed=embed)


@bot.command(
    name="members",
    brief="Retorna o número de membros no server.",
    description="""
        `members`: Retorna o número de membros no server (contando os bots).
    """
)
async def all_members(ctx):
    embed = Embed(colour=Colour.green())

    embed.add_field(
        name="",
        value=f"O número de membros em {ctx.guild.name} é de: {len(ctx.guild.members)}",
        inline=False
    )

    await ctx.send(embed=embed)


@bot.command(
    name="search",
    brief="Procura e retorna links.",
    description="""
        `search [pesquisa]`: Retorna 5 links relacionados com a pesquisa.
        `search [pesquisa] [número de links]`: Retorna um número de links definido relacionados com a pesquisa.
        `search "[pesquisa]" [número de links]`: Caso sua pesquisa seja mais longa que uma palavra digite ela entre aspas.
    """
)
async def search_google(ctx, query: str, num_links: int = 5):
    embed: Embed = Embed()

    if 20 >= num_links > 0:
        embed.title = f"{ctx.author.nick if ctx.author.nick else ctx.author.name}, aqui estão os links relacionados com '{query}': "
        embed.colour = Colour.green()

        links = [x for x in search(query, safe="on", num_results=num_links)]

        for i, link in enumerate(links):
            embed.add_field(
                name=f"**{i + 1}.** {link}",
                value="",
                inline=False
            )
    else:
        embed.colour = Colour.red()

        embed.add_field(
            name="",
            value="**:x: O número de links deve ser menor ou igual a 20 e maior que 0!**",
            inline=False
        )

    await ctx.send(embed=embed)


@bot.command(
    brief="Retorna um número aleatório entre 1 e 100 ou 1 e um número escolhido.",
    description="""
        `roll`: Retorna um número aleatório entre 1 e 100.
        `roll [número limite]`: Retorna um número aleatório entre 1 e o número de escolha do usuário.
    """
)
async def roll(ctx, max_num: int = 100):
    embed: Embed = Embed()

    if max_num > 1:
        embed.colour = Colour.green()

        embed.add_field(
            name="",
            value=f"Número escolhido: {random.randint(1, max_num + 1)}",
            inline=False
        )
    else:
        embed.colour = Colour.red()

        embed.add_field(
            name="",
            value="**:x: O número máximo deve ser maior que 1!**",
            inline=False
        )

    await ctx.send(embed=embed)
    

@bot.command(
    brief="Retorna uma escolha aleatória.",
    description="""
        `choose [elemento 1] [elemento 2] [elemento 3] ...`: Retorna um escolha aleatória entre N elementos.
    """
)
async def choose(ctx, *choices):
    embed: Embed = Embed(colour=Colour.green())

    embed.add_field(
        name="",
        value=f"A minha escolha foi: **{random.choice(choices)}**",
        inline=False
    )

    await ctx.send(embed=embed)
