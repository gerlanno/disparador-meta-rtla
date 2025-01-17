import sys
import os
from tqdm import tqdm
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".."))
)
import json
from requests import request
from config.configs import find_token
from controller.controller import get_business_account, cadastrar_template


def update_templates_list():

    accounts = get_business_account()

    for account in accounts:

        name = account.get("name")
        phone_id = account.get("phone_id")
        business_account_id = account.get("business_account_id")

        token = find_token(phone_id).replace("Bearer ", "")

        
        api_url = f"https://graph.facebook.com/v20.0/{business_account_id}/message_templates?fields=name, status,id,language,category&access_token={token}"

        response = request(method="GET", url=api_url)    

        response_data = json.loads(response.text)
        templates = response_data.get("data")
        if templates:
            for template in tqdm(templates, desc=f"Cadastrando templates - Conta: {name}", unit=" templates ", colour="MAGENTA"):
                try:
                    cadastrar_template(
                        name=template.get("name"),
                        status=template.get("status"),
                        language=template.get("language"),
                        wbaccount_id=business_account_id,
                    )
                    
                except Exception as e:
                    print("Erro cadastrando template.")
      
    return print("Atualização concluída")


