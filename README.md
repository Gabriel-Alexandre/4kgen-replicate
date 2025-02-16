
1. Crie e ative o ambiente virtual:
   - No Windows:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
   - No Linux/MacOS:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Instale as dependências do projeto:
   ```bash
   pip install -r requirements.txt
   ```

3. Crie o arquivo `.env` e configure as variáveis de ambiente:
   ```bash
   REPLICATE_API_TOKEN=seu_token_aqui
   ```
