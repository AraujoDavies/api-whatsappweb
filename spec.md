# API WHATSAPP WEB

## Objetivo

Criar uma API que com base em métodos POST receba requisições e faça as tarefas com um browser em HEADLESS.

- Facilitar manipulação do Whatsapp web
- Trabalhar com envio de mensagens para contatos.

## Como ?

Será criado um cluster inicialmente em EC2 q hospedará containers e persistência do perfil do whatsapp web. O usuário deverá fazer requests com alguns métodos e parâmetros que será previamente definidos.

Porém a ideia final é subir em ECS ou LAMBDA, armazenando a persitência em um storage.

## Métodos da API

- **Login:**
    
    A forma de login DEFAULT será por meio do código, ou seja, sem QRCODE code nesse método.

- **Screenshot:**

    Faz uma captura do browser q estará em segundo plano. Esse método é pensado para debug, porém se estiver na tela do QRCODE, pode ser usado como login.

- **send_messsage:**

    Envia a mensagem em um determinando chat.

- **healthcheck:**

    Verifica se o browser está saudável e se usuário está conectado.