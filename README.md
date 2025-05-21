# Bot de Lembretes para Discord

Um bot de Discord que permite criar lembretes recorrentes e configurar exclusão automática de mensagens em canais específicos.

## Demonstração

Aqui estão algumas imagens que mostram o funcionamento do bot:

### 1. Criando um Lembrete e recorrência
![Criando Lembrete](https://github.com/user-attachments/assets/aa3996d3-3efb-4609-a8c7-54276a0ceef5)

### 2. Online no discord
![Lembrete Ativado](https://github.com/user-attachments/assets/9f6e2b22-c42f-4e06-a944-8beed2b64785)

### 3. Seleção do canal
![Exclusão Automática](https://github.com/user-attachments/assets/c7e985e5-4f63-492b-91c3-487fd7c8ab5f)


### 4. Lista de comandos disponiveis
![Lista de Lembretes](https://github.com/user-attachments/assets/e08b92be-1236-4baa-90b6-0edd8f2c02d5)


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
