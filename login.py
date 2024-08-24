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

    endpoint = 'https://wa-api.metronw.com.br/tickets?pageNumber=1&status=pending&queueIds=[4]'

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

        cursor.execute("SHOW COLUMNS FROM aguardando LIKE 'quantidade'")
        result = cursor.fetchone()

        if not result:

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS aguardando (
                id INT AUTO_INCREMENT PRIMARY KEY,
                quantidade INT  -- Armazena o total de mensagens pendentes
            )
            """)
            connection.commit()

        messages_response = session.get(endpoint, headers=headers)
        if messages_response.status_code == 200:
            try:
                messages = messages_response.json()
            except ValueError as e:
                print(f"Erro ao decodificar JSON: {e}")
                exit(1)

            print(f"Mensagens recebidas do endpoint {endpoint}:")
            print(messages)

            if isinstance(messages, dict) and 'count' in messages:
                count = messages['count']

                update_query = """
                INSERT INTO aguardando (quantidade)
                VALUES (%s)
                ON DUPLICATE KEY UPDATE quantidade=VALUES(quantidade)
                """

                if count >= 0:
                    print(f"Inserindo ou atualizando dados na tabela 'aguardando' com {count} mensagens pendentes.")
                    cursor.execute(update_query, (count,))
                    connection.commit()

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
