import requests
import mysql.connector
from datetime import datetime, timedelta

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

def convert_to_utc_minus_3(timestamp):
    if timestamp:
        utc_time = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
        utc_minus_3_time = utc_time - timedelta(hours=3)
        return utc_minus_3_time.strftime('%Y-%m-%d %H:%M:%S')
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
                    print("A resposta do endpoint é uma lista, ignorando.")
                    continue 

                for message in messages.get('tickets', []):
                    ticket_id = message.get('id')
                    status = message.get('status', 'unknown')
                    last_message = message.get('lastMessage', '')
                    created_at = convert_to_utc_minus_3(message.get('createdAt'))
                    updated_at = convert_to_utc_minus_3(message.get('updatedAt'))

                    if None in [ticket_id, status, last_message, created_at]:
                        print(f"Dados inválidos para a mensagem: {message}")
                        continue

                    mensagens_query = """
                    INSERT INTO mensagens (ticket_id, status, last_message, data_criacao)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE status=VALUES(status), last_message=VALUES(last_message), data_criacao=VALUES(data_criacao)
                    """
                    mensagens_values = (ticket_id, status, last_message, created_at)
                    print(f"Inserindo dados na tabela 'mensagens': {mensagens_values}")
                    cursor.execute(mensagens_query, mensagens_values)

                    connection.commit()
                    cursor.execute("SELECT id FROM mensagens WHERE ticket_id = %s", (ticket_id,))
                    message_data = cursor.fetchone()
                    if not message_data:
                        print(f"Erro: Mensagem com ticket_id {ticket_id} não foi inserida na tabela 'mensagens'.")
                        continue

                    message_id = message_data[0]

                    cursor.execute("""
                    SELECT COUNT(*) FROM aguardando 
                    WHERE usuario_id = %s AND last_message = %s
                    """, (ticket_id, last_message))
                    exists = cursor.fetchone()[0]

                    if exists == 0:

                        nome_usuario = message.get('contact', {}).get('name', 'Desconhecido')
                        usuarios_query = """
                        INSERT INTO usuarios (id, nome)
                        VALUES (%s, %s)
                        ON DUPLICATE KEY UPDATE nome=VALUES(nome)
                        """
                        usuarios_values = (ticket_id, nome_usuario)
                        print(f"Inserindo dados na tabela 'usuarios': {usuarios_values}")
                        cursor.execute(usuarios_query, usuarios_values)

                        aguardando_query = """
                        INSERT INTO aguardando (usuario_id, mensagem_id, data_criacao, last_message)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE data_criacao=VALUES(data_criacao), last_message=VALUES(last_message)
                        """
                        aguardando_values = (ticket_id, message_id, created_at, last_message)
                        print(f"Inserindo dados na tabela 'aguardando': {aguardando_values}")
                        cursor.execute(aguardando_query, aguardando_values)
                    else:
                        print(f"Mensagem '{last_message}' já existe na tabela 'aguardando' para o usuário {ticket_id}.")

            else:
                print(f"Falha na requisição de mensagens para o endpoint {endpoint}.")
                print(f"Status Code: {messages_response.status_code}")
                print(messages_response.text)

        connection.commit()
        print("Dados inseridos com sucesso!")

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
