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
        'https://wa-api.metronw.com.br/tickets?pageNumber=1&status=open&showAll=false&queueIds=[4]',
        'https://wa-api.metronw.com.br/tickets?pageNumber=1&status=pending&queueIds=[4]',
        'https://wa-api.metronw.com.br/whatsapp?companyId=1&session=0',
        'https://wa.metronw.com.br/tickets'  
    ]

    connection = None

    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='pass',
            database='metronw-coleta'
        )
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS filas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            status VARCHAR(50) NOT NULL,
            createdAt DATETIME,
            updatedAt DATETIME
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensagens (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fila_id INT NOT NULL,
            message TEXT NOT NULL,
            createdAt DATETIME,
            updatedAt DATETIME,
            FOREIGN KEY (fila_id) REFERENCES filas(id) ON DELETE CASCADE
        )
        """)

        for endpoint in endpoints:
            messages_response = session.get(endpoint, headers=headers)
            if messages_response.status_code == 200:
                messages = messages_response.json()
                print(f"Mensagens recebidas do endpoint {endpoint}:")
                print(messages)

                for message in messages.get('tickets', []):
                    name = message.get('contact', {}).get('name', 'Desconhecido')
                    status = message.get('status')
                    createdAt = convert_to_utc_minus_3(message.get('createdAt'))
                    updatedAt = convert_to_utc_minus_3(message.get('updatedAt'))
                    lastMessage = message.get('lastMessage', '')

                    filas_query = """
                    INSERT INTO filas (id, name, status, createdAt, updatedAt)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE name=VALUES(name), status=VALUES(status), updatedAt=VALUES(updatedAt)
                    """
                    filas_values = (
                        message.get('id'), name, status, createdAt, updatedAt
                    )
                    cursor.execute(filas_query, filas_values)

                    mensagens_query = """
                    INSERT INTO mensagens (fila_id, message, createdAt, updatedAt)
                    VALUES (%s, %s, %s, %s)
                    """
                    mensagens_values = (
                        message.get('id'), lastMessage, createdAt, updatedAt
                    )
                    cursor.execute(mensagens_query, mensagens_values)

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
