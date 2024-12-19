# Disparador Meta RTLA

Sistema para envio de comunicados utilizando a API oficial da Meta para o WhatsApp Business.

## Descrição

Este projeto permite o envio automatizado de mensagens pelo WhatsApp Business, integrando-se à API oficial da Meta.

## Funcionalidades

- Envio de mensagens personalizadas para contatos específicos.
- Integração com a API oficial do WhatsApp Business.
- Troca automática de template em caso de bloqueio.

## Requisitos

- Python 3.x
- Bibliotecas listadas no arquivo `requirements.txt`

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/gerlanno/disparador-meta-rtla.git
  
    ```

2. Navegue até o diretório do projeto:
  
    ```bash
    cd disparador-meta-rtla
  
    ```

3. Crie um ambiente virtual (opcional, mas recomendado):
   
    ```bash
    python -m venv venv
    source venv/bin/activate # No Windows: venv\Scripts\activate
    ```
    
4. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

## Uso
Na primeira execução do script, será criado o banco de dados e inserido os dados de configuração inicial.
1. Execute o script principal para exibir o menu de opções:

    ```bash
    python src/main.py
    ```
2. Escolha no menu exibido as opções de atualizar os dados das contas da Meta primeiro, somente depois execute a rotina de atualização de templates.


3. Coloque os arquivos para extração dos dados na pasta data. Por exemplo, `src/data/Cancelamento....xml`.


4. Iniciar os disparos:
   
     ```bash
     python src/main.py "<<nome da business acc>>"
     ```  
     
## Estrutura do Projeto
  ```
  config/: Arquivos de configuração.
  controller/: Lógica de controle do aplicativo.
  model/: Definições de modelos de dados.
  src/: Código-fonte principal.
  ```
