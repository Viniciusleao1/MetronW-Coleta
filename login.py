import requests
import mysql.connector
from datetime import datetime

url_login_post = 'https://wa-api.metronw.com.br/auth/login'

login_data = {
    'email': 'teste@teste.com.br',
    'password': 'A1cJk2!',
}
session = requests.Session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
}
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

    url_unread_messages = 'https://wa-api.metronw.com.br/tickets?withUnreadMessages=true'
    messages_response = session.get(url_unread_messages, headers=headers)

    if messages_response.status_code == 200:
        try:
            messages = messages_response.json()
            print("Mensagens não lidas:")
            print(messages)
    
            connection = mysql.connector.connect(
                host='localhost',
                user='root', 
                password='password',  
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

            for message in messages.get('tickets', []):
                name = message.get('contact', {}).get('name', 'Desconhecido')  
                filas_query = """
                INSERT INTO filas (id, name, status, createdAt, updatedAt)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE name=VALUES(name), status=VALUES(status), updatedAt=VALUES(updatedAt)
                """
                filas_values = (
                    message.get('id'), name, message.get('status'),
                    message.get('createdAt'), message.get('updatedAt')
                )
                cursor.execute(filas_query, filas_values)

                mensagens_query = """
                INSERT INTO mensagens (fila_id, message, createdAt, updatedAt)
                VALUES (%s, %s, %s, %s)
                """
                mensagens_values = (
                    message.get('id'), message.get('lastMessage'),
                    message.get('createdAt'), message.get('updatedAt')
                )
                cursor.execute(mensagens_query, mensagens_values)

            connection.commit()

            print("Dados inseridos com sucesso!")

        except requests.exceptions.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
        except mysql.connector.Error as err:
            print(f"Erro ao inserir os dados: {err}")
            connection.rollback()
        finally:
            
            cursor.close()
            connection.close()
    else:
        print("Falha na requisição de mensagens.")
        print(f"Status Code: {messages_response.status_code}")
        print(messages_response.text)
else:
    print("Falha no login.")
    print(f"Status Code: {response.status_code}")
    print(response.text)
