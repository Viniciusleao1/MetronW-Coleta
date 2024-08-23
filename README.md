# MetronW-Coleta

**Repositório para desenvolvimento e manutenção de scripts de coleta de dados do MetronW.**

## 🚀 Introdução

Este projeto visa coletar e analisar dados do sistema MetronW, utilizando scripts em Python para interagir com a API e o banco de dados MySQL.

## 🛠️ Requisitos

- **Python 3.6+**: Certifique-se de que você tem o Python instalado.
- **MySQL 5.7+**: Um banco de dados MySQL deve estar configurado.
- **Git**: Para clonar o repositório.

## 📥 Instalação

Siga os passos abaixo para configurar o projeto:

1. **Clonar o Repositório**

   Clone o repositório para o seu ambiente local:

   ```bash
   git clone https://github.com/Viniciusleao1/MetronW-Coleta.git
   
   cd MetronW-Coleta
   

#### 🛠️ Guia de Uso 🎨: 

Siga as etapas abaixo para configurar e executar o projeto:


#### 1. Clonar o Repositório

Clone o repositório para o seu ambiente local:

git clone https://github.com/Viniciusleao1/MetronW-Coleta.git

cd MetronW-Coleta

#### 2. Configurar o Ambiente Virtual

Crie e ative um ambiente virtual para isolar as dependências do projeto:

python -m venv venv

source venv/bin/activate  # No Windows, use: .\venv\Scripts\activate

#### 3. Instalar Dependências

Instale as dependências necessárias usando o pip:

pip install -r requirements.txt

#### 4. Configurar o Script

Antes de executar o script, certifique-se de que o banco de dados MySQL está configurado corretamente e que o script login.py está com as credenciais e URLs ajustadas conforme suas necessidades.

#### 5. Importando o Arquivo SQL**

Para importar o arquivo SQL, siga estes passos:

1. **Selecione o arquivo:**
   * Clique no botão "Escolher arquivo" e localize o arquivo `metronw-coleta.sql` no seu computador.

   2. **Configure as opções:**
   * **Formato:** Certifique-se que esteja definido como "SQL".
   * **Delimitador:** Geralmente é `;`.
   * **Encoding:** Selecione o encoding correto, normalmente UTF-8.

3. **Inicie a importação:**
   * Clique no botão "Executar". Você verá uma barra de progresso enquanto o processo ocorre.

**Após a importação:**

Uma vez que o arquivo SQL tenha sido importado com sucesso, você pode **remover o arquivo original** do seu computador. 

**Lembre-se:** A segurança dos seus dados é fundamental. **Recomendamos que você crie uma cópia de segurança** do arquivo SQL em um local seguro e de fácil acesso, como o Google Drive ou Dropbox. Essa medida é essencial para garantir a recuperação dos seus dados em caso de problemas. 

**Dica:** Utilize um serviço de armazenamento em nuvem para garantir a segurança e o acesso aos seus backups de qualquer lugar.





#### 6. Executar o Script

Para executar o script de coleta de dados, use o comando:

python login.py

#### 🧑‍💻 Contribuições

Se você deseja contribuir para o projeto, siga os passos abaixo:

Faça um fork do repositório.
Crie uma branch para a sua nova funcionalidade ou correção de bug.
Faça suas alterações e commit.
Envie um pull request para revisão.

📧 Contato
Para mais informações ou suporte, entre em contato com Viniciusleao1.



#### Obrigado por conferir o projeto MetronW-Coleta! 🚀
