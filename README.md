# Bot de Lembretes para Discord

Um bot de Discord que permite criar lembretes recorrentes e configurar exclusão automática de mensagens em canais específicos.

## Demonstração

Aqui estão algumas imagens que mostram o funcionamento do bot:

### 1. Criando um Lembrete e recorrência
![Image](https://github.com/user-attachments/assets/c46d8ebb-909b-4a8b-a52a-d12a764fe1f5)

### 2. Online no discord
[Image](https://github.com/user-attachments/assets/73e825aa-0e7b-4d47-aabd-b768adb9c655)

### 3. Seleção do canal
![Image](https://github.com/user-attachments/assets/ce9a97ee-8a6a-4f30-96d6-b72ee57a9d50)


### 4. Lista de comandos disponiveis
![Image](https://github.com/user-attachments/assets/e0e0aeda-da1f-4ef6-9731-4ca3181059b7)


## Funcionalidades

- **Lembretes Personalizados**: Crie lembretes com data e hora específicas
- **Recorrência**: Configure lembretes recorrentes (diários, semanais ou em segundos)
- **Exclusão Automática**: Configure a exclusão automática de mensagens em canais específicos
- **Persistência**: Os lembretes são salvos em um arquivo CSV e mantidos após reinicialização
- **Interface por Comandos**: Fácil de usar com comandos simples

## Pré-requisitos

- Python 3.8 ou superior
- Discord.py
- Conta de desenvolvedor Discord
- Token de bot do Discord

## Instalação

1. Clone o repositório:
   ```bash
   git clone [URL_DO_REPOSITORIO]
   cd Discordvini
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
   
   (Crie um arquivo `requirements.txt` com: `discord.py`)

3. Configure o token do bot:
   - No arquivo `main.py`, substitua `'SEU_TOKEN_AQUI'` pelo token do seu bot do Discord
   - **Importante**: Nunca compartilhe ou faça commit do token real

4. Execute o bot:
   ```bash
   python main.py
   ```

## Comandos

### Lembretes
- `!ajuda` - Mostra todos os comandos disponíveis
- `!lembrar dd/mm/aaaa HH:MM` - Inicia a criação de um novo lembrete
  - O bot irá pedir:
    1. A mensagem do lembrete
    2. A recorrência (ex: 2d para 2 dias, 1s para 1 semana, 30seg para 30 segundos)
    3. O canal onde o lembrete será enviado
- `!listar_lembretes` - Lista todos os lembretes ativos
- `!excluir <número>` - Remove um lembrete da lista

### Exclusão Automática
- `!config_auto_excluir <canal> <segundos>` - Configura a exclusão automática de mensagens em um canal
- `!cancelar_auto_excluir <canal>` - Desativa a exclusão automática em um canal
- `!mostrar_exclusoes` - Mostra todas as configurações de exclusão ativas

## Exemplos de Uso

1. **Criar um lembrete único**:
   ```
   !lembrar 31/12/2024 23:59
   ```
   Em seguida, siga as instruções do bot para completar a criação do lembrete.

2. **Criar um lembrete recorrente**:
   ```
   !lembrar 31/12/2024 23:59
   ```
   Quando solicitado, informe a recorrência, por exemplo:
   - `7d` para lembrar a cada 7 dias
   - `1s` para lembrar a cada semana
   - `3600seg` para lembrar a cada hora

3. **Configurar exclusão automática**:
   ```
   !config_auto_excluir #geral 3600
   ```
   Isso irá configurar a exclusão automática de mensagens no canal #geral a cada hora.

## Segurança

- **NUNCA** compartilhe seu token de bot
- Mantenha o arquivo `lembretes.csv` em um local seguro
- Certifique-se de que apenas administradores confiáveis tenham acesso aos comandos sensíveis

## Solução de Problemas

- **Bot não responde**: Verifique se o token está correto e se o bot tem as permissões necessárias
- **Comandos não funcionam**: Verifique se o bot tem a intenção `message_content` habilitada no portal do desenvolvedor Discord
- **Erros de permissão**: Certifique-se de que o bot tem permissão para enviar mensagens e gerenciar mensagens nos canais desejados



---

Desenvolvido por Vinicius Botelho - 2024
