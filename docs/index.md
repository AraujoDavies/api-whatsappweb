![Logo_do_projeto](assets/logo.png){width=300 .center} <!--{chaves} não funcionam por padrão, necessário usar o markdow_extensions-->


### HOW TO RUN

> dependencies:

    Docker.

> Configure ENV file.

In .env file SET 3 ENVS to avoid error **(USE ABSOLUTE PATH)**:

    VALID_PROFILE_PATH = # where storage chrome session
    VALID_PRINTS_PATH = # where storage prints 
    VALID_PHONE_NUMBER = # country_code + area_code + phone_number 
    
> Commands to run: (adjust port in compose.yml => default value is 80)

    git clone https://github.com/AraujoDavies/api-whatsappweb.git
    
    docker build -t api-whatsweb .
    
    docker compose up -d

### FASTAPI DOC

YOUR_IP:PORT/doc or YOUR_IP:PORT/redoc

>>> Example: http://127.0.0.1:8000/docs


### HOW TO USE

With app started.

> GET Methods

- First route: (start browser)

    http://127.0.0.1:8000/start?phone_number=5511987654321

- Check how many browsers are running:

    http://127.0.0.1:8000/browsers

- Scan QRCODE: (ignore if already scanned)

    http://127.0.0.1:8000/screenshot?phone_number=5511987654321

- Close browser:
    
    http://127.0.0.1:8000/stop?phone_number=5511987654321    


> POST Methods (Find chats and send messages.) 

It's more easyli use FASTAPI DOC: http://127.0.0.1:8000/docs

