""" 
1 - como será a escolha de qual conta da meta vai ser usada para os disparos.

2 - Salvar todos os templates no banco de dados, junto aos dados como os ids das contas e seus respectivos status.
    2.1 - endpoint para modelos de mensagem: message_templates?fields=name,status,id,language -(obs: usa-se o ID da Conta)
        Ex. output: {
  "data": [
    {
      "name": "cancelamento28",
      "status": "APPROVED",
      "id": "992043572641665",
      "language": "pt_BR",      
    },]

    2.2 - O Model dessa tabela será a seguinte:__tablename__("templates") id(int, fk) name(String), status(string), id(String), language(string), id_conta_wb(String, FK)

3 - Model dos id da conta da meta: __tablename__("wb_accounts") id(int, pk), wbAccountId(), cartorioID(int, fk(cartorio.id))

4 - Criar Script para o envio das mensagens, salvar o response a cada envio, e em caso de erro de template, atualizar o status do template na tabela e selecionar um outro. (Obs. pode ser criado uma função, em paralelo as inserções de template, uma para atualizar todos os status)

5 -     
"""
