import requests
import mysql.connector
from datetime import datetime
import pytz

url_login_post = 'https://wa-api.metronw.com.br/auth/login'

login_data = {
    'email': 'teste@teste.com.br',
    'password': 'A1cJk2!',
}

session = requests.Session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
}

def convert_to_sp_timezone(timestamp):
    if timestamp:
        utc_time = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
        sp_timezone = pytz.timezone('America/Sao_Paulo')
        sp_time = utc_time.astimezone(sp_timezone)
        return sp_time.strftime('%Y-%m-%d %H:%M:%S')
    return None

response = session.post(url_login_post, json=login_data, headers=headers)

if response.status_code == 200:
    print("Login realizado com sucesso!")
    data = response.json()

    token = data.get('token')
    if not token:
        print("Token de sessão não encontrado.")
        exit(1)

    headers.update({
        'Authorization': f'Bearer {token}',
    })

    endpoints = [
        'https://wa-api.metronw.com.br/tickets?withUnreadMessages=true',
        'https://wa-api.metronw.com.br/tickets?pageNumber=1&status=open&showAll=false&queueIds=[0]',
        'https://wa-api.metronw.com.br/tickets?pageNumber=1&status=pending&queueIds=[0]',
        'https://wa-api.metronw.com.br/whatsapp?companyId=1&session=0',
        'https://wa.metronw.com.br/tickets'
    ]

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='pass',
            database='metronw-coleta'
        )
        cursor = connection.cursor()

        cursor.execute("SHOW COLUMNS FROM aguardando LIKE 'conversas'")
        result = cursor.fetchone()

        if result:

            cursor.execute("""
            ALTER TABLE aguardando CHANGE COLUMN conversas quantidade INT;
            """)
            connection.commit()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS aguardando (
            id INT AUTO_INCREMENT PRIMARY KEY,
            grupo_id INT,
            mensagens_nao_lidas INT,
            ultima_mensagem TEXT,
            data_ultima_mensagem TIMESTAMP,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            quantidade INT,  -- Armazena o total de grupos em espera
            UNIQUE KEY(grupo_id)
        )
        """)
        connection.commit()

        total_grupos_espera = 0

        for endpoint in endpoints:
            messages_response = session.get(endpoint, headers=headers)
            if messages_response.status_code == 200:
                try:
                    messages = messages_response.json()
                except ValueError as e:
                    print(f"Erro ao decodificar JSON: {e}")
                    continue

                print(f"Mensagens recebidas do endpoint {endpoint}:")
                print(messages)

                if isinstance(messages, list):
                    print("A resposta do endpoint é uma lista, processando...")
                    for whatsapp_data in messages:
                        if 'queues' in whatsapp_data:
                            
                            grupos_em_espera = [queue for queue in whatsapp_data['queues'] if queue.get('id') and 'espera' in queue.get('name').lower()]
                            total_grupos_espera += len(grupos_em_espera)
                    continue

                for message in messages.get('tickets', []):
                    grupo_id = message.get('id')
                    mensagens_nao_lidas = message.get('unreadMessages', 0)
                    ultima_mensagem = message.get('lastMessage', '')
                    data_ultima_mensagem = convert_to_sp_timezone(message.get('updatedAt'))

                    if 'espera' in message.get('status', '').lower():
                        total_grupos_espera += 1

                    if None in [grupo_id, ultima_mensagem, data_ultima_mensagem]:
                        print(f"Dados inválidos para a mensagem: {message}")
                        continue

                    aguardando_query = """
                    INSERT INTO aguardando (grupo_id, mensagens_nao_lidas, ultima_mensagem, data_ultima_mensagem, quantidade)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                        mensagens_nao_lidas=VALUES(mensagens_nao_lidas), 
                        ultima_mensagem=VALUES(ultima_mensagem), 
                        data_ultima_mensagem=VALUES(data_ultima_mensagem), 
                        data_atualizacao=CURRENT_TIMESTAMP
                    """
                    aguardando_values = (grupo_id, mensagens_nao_lidas, ultima_mensagem, data_ultima_mensagem, total_grupos_espera)
                    print(f"Inserindo dados na tabela 'aguardando': {aguardando_values}")
                    cursor.execute(aguardando_query, aguardando_values)

                    connection.commit()

            else:
                print(f"Falha na requisição de mensagens para o endpoint {endpoint}.")
                print(f"Status Code: {messages_response.status_code}")
                print(messages_response.text)

        update_quantidade_query = "UPDATE aguardando SET quantidade = %s"
        cursor.execute(update_quantidade_query, (total_grupos_espera,))
        connection.commit()

        print(f"Total de grupos em espera: {total_grupos_espera}")

    except requests.exceptions.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
    except mysql.connector.Error as err:
        print(f"Erro ao inserir os dados: {err}")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

else:
    print("Falha no login.")
    print(f"Status Code: {response.status_code}")
    print(response.text)
