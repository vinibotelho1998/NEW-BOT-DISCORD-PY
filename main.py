import discord
import asyncio
from datetime import datetime, timedelta
import csv

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
TOKEN = 'SEU_TOKEN_AQUI'

lembretes = []
auto_delete_configs = []

def analisar_recorrencia(recorrencia_str):
    recorrencia_str = recorrencia_str.strip()
    if not recorrencia_str:
        return None, None

    if recorrencia_str.isdigit():
        return int(recorrencia_str) * 86400, 'd'

    if len(recorrencia_str) >= 3:
        unidade = recorrencia_str[-3:].lower()
        try:
            valor = int(recorrencia_str[:-3]) if unidade == 'seg' else int(recorrencia_str[:-1])
        except ValueError:
            return None, None
    else:
        unidade = recorrencia_str[-1].lower()
        try:
            valor = int(recorrencia_str[:-1])
        except ValueError:
            return None, None

    if unidade == 'seg':
        return valor, 'segundos'
    elif unidade == 'd':
        return valor * 86400, 'dias'
    elif unidade == 's':
        return valor * 604800, 'semanas'
    elif unidade == 'm':
        return valor * 60, 'minutos'
    else:
        return None, None

def carregar_lembretes_csv():
    try:
        with open('lembretes.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data_hora = datetime.strptime(row['data_hora'], '%d/%m/%Y %H:%M')
                recorrencia_segundos, unidade_recorrencia = analisar_recorrencia(row['recorrencia'])
                if recorrencia_segundos is None:
                    recorrencia_segundos = 0
                canal = discord.utils.get(client.get_all_channels(), name=row['canal'], type=discord.ChannelType.text)
                if canal is None:
                    canal = discord.utils.get(client.get_all_channels(), id=int(row['canal']), type=discord.ChannelType.text)
                lembretes.append({
                    'usuario': client.get_user(int(row['usuario'])),
                    'data_hora': data_hora,
                    'mensagem': row['mensagem'],
                    'recorrencia_segundos': recorrencia_segundos,
                    'unidade_recorrencia': unidade_recorrencia,
                    'canal': canal
                })
    except FileNotFoundError:
        print('Arquivo CSV de lembretes não encontrado.')

def salvar_lembretes_csv():
    with open('lembretes.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['usuario', 'data_hora', 'mensagem', 'recorrencia', 'canal']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for lembrete in lembretes:
            writer.writerow({
                'usuario': lembrete['usuario'].id,
                'data_hora': lembrete['data_hora'].strftime('%d/%m/%Y %H:%M'),
                'mensagem': lembrete['mensagem'],
                'recorrencia': lembrete['recorrencia_segundos'] if lembrete['recorrencia_segundos'] > 0 else '',
                'canal': lembrete['canal'].id
            })

@client.event
async def on_ready():
    print(f'Logado como {client.user}')
    carregar_lembretes_csv()
    client.loop.create_task(lembrete_loop())
    client.loop.create_task(auto_delete_loop())

@client.event
async def on_message(message):
    global lembretes
    global auto_delete_configs

    if message.author == client.user:
        return

    if message.content.startswith('!ajuda'):
        ajuda_msg = ("Comandos disponíveis:\n"
                     "!lembrar dd/mm/aaaa HH:MM - Cria um novo lembrete.\n"
                     "!listar_lembretes - Lista todos os lembretes salvos.\n"
                     "!excluir <número do lembrete> - Exclui o lembrete especificado.\n"
                     "!config_auto_excluir <nome do canal> <intervalo em segundos> - Configura a exclusão automática de mensagens no canal especificado.\n"
                     "!cancelar_auto_excluir <nome do canal> - Cancela a configuração de exclusão automática no canal especificado.\n"
                     "!mostrar_exclusoes - Mostra todas as auto exclusões em andamento.\n")
        await message.channel.send(ajuda_msg)

    elif message.content.startswith('!lembrar'):
        try:
            _, data_hora = message.content.split(' ', 1)
            data_hora = data_hora.strip()

            try:
                data_hora = datetime.strptime(data_hora, '%d/%m/%Y %H:%M')
            except ValueError:
                await message.channel.send('Formato de data e hora inválido. Use dd/mm/aaaa HH:MM.')
                return

            await message.channel.send('Agora, por favor, informe a mensagem associada ao lembrete:')
            msg = await client.wait_for('message', check=lambda m: m.author == message.author)
            mensagem = msg.content.strip()

            await message.channel.send('Informe a recorrência em dias (d), semanas (s) ou segundos (seg) (ex: 2d, 1s, 30seg). Digite 0 para um lembrete único:')
            try:
                resposta_recorrencia = await client.wait_for('message', check=lambda m: m.author == message.author, timeout=30.0)
                recorrencia_segundos, unidade_recorrencia = analisar_recorrencia(resposta_recorrencia.content)
                if recorrencia_segundos is None:
                    await message.channel.send('Formato de recorrência inválido. O lembrete será definido como único.')
                    recorrencia_segundos = 0
                    unidade_recorrencia = None
            except asyncio.TimeoutError:
                await message.channel.send('Tempo esgotado para informar a recorrência. O lembrete será definido como único.')
                recorrencia_segundos = 0
                unidade_recorrencia = None

            await message.channel.send('Informe o nome do canal onde deseja receber o lembrete:')
            resposta_canal = await client.wait_for('message', check=lambda m: m.author == message.author, timeout=30.0)
            nome_canal = resposta_canal.content.strip()
            canal = discord.utils.get(message.guild.channels, name=nome_canal, type=discord.ChannelType.text)
            if canal is None:
                await message.channel.send(f'Canal "{nome_canal}" não encontrado. O lembrete será definido para este canal.')
                canal = message.channel

            lembretes.append({
                'usuario': message.author,
                'data_hora': data_hora,
                'mensagem': mensagem,
                'recorrencia_segundos': recorrencia_segundos,
                'unidade_recorrencia': unidade_recorrencia,
                'canal': canal
            })

            salvar_lembretes_csv()

            if unidade_recorrencia:
                await message.channel.send(f'Ok, vou te lembrar em {data_hora} com recorrência de {resposta_recorrencia.content} no canal {canal.mention}.')
            else:
                await message.channel.send(f'Ok, vou te lembrar em {data_hora} no canal {canal.mention}.')

        except (ValueError, IndexError):
            await message.channel.send('Formato incorreto. Use: !lembrar dd/mm/aaaa HH:MM\n'
                                       'Exemplo: !lembrar 25/06/2024 20:53')

    elif message.content.startswith('!listar_lembretes'):
        if not lembretes:
            await message.channel.send('Não há lembretes salvos.')
            return

        resposta = 'Lembretes salvos:\n'
        for idx, lembrete in enumerate(lembretes, 1):
            lembrete_info = f'{idx}. {lembrete["data_hora"].strftime("%d/%m/%Y %H:%M")} - {lembrete["mensagem"]} (Recorrência: {lembrete["unidade_recorrencia"]}, Canal: {lembrete["canal"].mention})\n'
            if len(resposta) + len(lembrete_info) > 2000:
                await message.channel.send(resposta)
                resposta = ''
            resposta += lembrete_info

        if resposta:
            await message.channel.send(resposta)

    elif message.content.startswith('!excluir'):
        if not lembretes:
            await message.channel.send('Não há lembretes para excluir.')
            return

        try:
            _, idx = message.content.split(' ', 1)
            idx = int(idx.strip()) - 1
            if 0 <= idx < len(lembretes):
                lembrete_excluido = lembretes.pop(idx)
                salvar_lembretes_csv()
                await message.channel.send(f'Lembrete "{lembrete_excluido["mensagem"]}" excluído com sucesso.')
            else:
                await message.channel.send('Índice de lembrete inválido.')
        except (ValueError, IndexError):
            await message.channel.send('Formato incorreto. Use: !excluir <número do lembrete>\n'
                                       'Exemplo: !excluir 1')

    elif message.content.startswith('!config_auto_excluir'):
        try:
            _, nome_canal, intervalo_str = message.content.split(' ', 2)
            nome_canal = nome_canal.strip()
            intervalo = int(intervalo_str.strip())
            canal = discord.utils.get(message.guild.channels, name=nome_canal, type=discord.ChannelType.text)
            if canal is None:
                await message.channel.send(f'Canal "{nome_canal}" não encontrado.')
                return

            auto_delete_configs.append({
                'canal': canal,
                'intervalo': intervalo,
                'ultimo_check': datetime.now()
            })

            await message.channel.send(f'Configuração de exclusão automática definida para o canal {canal.mention} com intervalo de {intervalo} segundos.')
        except (ValueError, IndexError):
            await message.channel.send('Formato incorreto. Use: !config_auto_excluir <nome do canal> <intervalo em segundos>\n'
                                       'Exemplo: !config_auto_excluir geral 3600')

    elif message.content.startswith('!cancelar_auto_excluir'):
        try:
            _, nome_canal = message.content.split(' ', 1)
            nome_canal = nome_canal.strip()
            canal = discord.utils.get(message.guild.channels, name=nome_canal, type=discord.ChannelType.text)
            if canal is None:
                await message.channel.send(f'Canal "{nome_canal}" não encontrado.')
                return

            auto_delete_configs = [config for config in auto_delete_configs if config['canal'] != canal]

            await message.channel.send(f'Configuração de exclusão automática cancelada para o canal {canal.mention}.')
        except (ValueError, IndexError):
            await message.channel.send('Formato incorreto. Use: !cancelar_auto_excluir <nome do canal>\n'
                                       'Exemplo: !cancelar_auto_excluir geral')

    elif message.content.startswith('!mostrar_exclusoes'):
        if not auto_delete_configs:
            await message.channel.send('Não há auto exclusões configuradas.')
            return

        resposta = 'Auto exclusões em andamento:\n'
        for config in auto_delete_configs:
            resposta += f'Canal: {config["canal"].mention}, Intervalo: {config["intervalo"]} segundos\n'

        await message.channel.send(resposta)

async def lembrete_loop():
    while True:
        agora = datetime.now()
        for lembrete in lembretes:
            diff = lembrete['data_hora'] - agora
            if diff.total_seconds() <= 0:
                try:
                    await lembrete['canal'].send(f'@here, está na hora! Você pediu para te lembrar de: "{lembrete["mensagem"]}"')
                except Exception as e:
                    print(f'Erro ao enviar lembrete: {e}')
                if lembrete['recorrencia_segundos'] == 0:
                    lembretes.remove(lembrete)
                else:
                    lembrete['data_hora'] += timedelta(seconds=lembrete['recorrencia_segundos'])
                salvar_lembretes_csv()
        await asyncio.sleep(1)

async def auto_delete_loop():
    while True:
        agora = datetime.now()
        for config in auto_delete_configs:
            if (agora - config['ultimo_check']).total_seconds() >= config['intervalo']:
                await processar_auto_delete(config)
                config['ultimo_check'] = agora
        await asyncio.sleep(1)

async def processar_auto_delete(config):
    canal = config['canal']
    async for message in canal.history(limit=None):
        try:
            await message.delete()
        except Exception as e:
            print(f'Erro ao excluir mensagem: {e}')
    try:
        await canal.send('Novos Avisos irão aparecer aqui.')
    except Exception as e:
        print(f'Erro ao enviar mensagem: {e}')

async def main():
    async with client:
        await client.start(TOKEN)

asyncio.run(main())
