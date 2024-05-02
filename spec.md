# API WHATSAPP WEB

## Objetivo

Criar uma API que com base em métodos POST receba requisições e faça as tarefas com um browser em HEADLESS.

- Facilitar manipulação do Whatsapp web
- Trabalhar com envio de mensagens para contatos.

## Como ?

Será criado um cluster inicialmente em EC2 q hospedará containers e persistência do perfil do whatsapp web. O usuário deverá fazer requests com alguns métodos e parâmetros que será previamente definidos.

Porém a ideia final é subir em ECS ou LAMBDA, armazenando a persitência em um storage.

## Métodos da API

- **start:**
    
    Cria um perfil do chrome caso ele não exista e inicia o navegador.

- **stop:**
    
    fecha o navegador

- **Screenshot:**

    Faz uma captura do browser q estará em segundo plano. Esse método é pensado para debug, porém se estiver na tela do QRCODE, pode ser usado como login.

- **browsers:**

    retorna um array com todas sessões do chrome ativas.

- **find-chat:**

    procura por um chat usando o campo de busca do whatsapp.

- **send-message:**

    Envia a mensagem passada por parametro em um chat. Depende que o chat seja encontrado pelo find-chat.