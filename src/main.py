import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from colorama import Fore, Style, init
from data.templates import update_templates_list
from controller.controller import get_business_account
from data.extract_data import extrair_dados

def pause():
    programPause = input("\nPressione <ENTER> para continuar...")


# Inicializa o colorama
init(autoreset=True)


# ASCII Art do Logo
logo = r"""
-------------------------------------------------------------------
   _____                _           
  / ____|              | |          
 | (___   ___ _ __   __| | ___ _ __ 
  \___ \ / _ \ '_ \ / _` |/ _ \ '__|
  ____) |  __/ | | | (_| |  __/ |   
 |_____/ \___|_| |_|\__,_|\___|_|   

 --------------------------------------------------------------------                               
"""


# Função para exibir o menu
def show_menu():
    print(Fore.CYAN + logo)
    print(Fore.GREEN + "Inicializando sistema\n")
    print(
        Fore.GREEN
        + ">>> Para iniciar os "
        + Fore.CYAN
        + "disparos utilizar: "
        + Fore.MAGENTA
    )
    print(
        Fore.GREEN
        + "python "
        + Fore.LIGHTRED_EX
        + "main.py "
        + Fore.MAGENTA
        + "<<business account>>\n"
    )
    opt = "0"
    while opt != "x":

        print(Fore.MAGENTA + "===================================================\n")
        print(Fore.MAGENTA + "[ 1 ] " + Fore.GREEN + "Extrair dados do XML\n")
        print(Fore.MAGENTA + "[ 2 ] " + Fore.GREEN + "Atualizar tabela de templates\n")
        print(
            Fore.MAGENTA + "[ 3 ] " + Fore.GREEN + "Listar contas Whatsapp business\n"
        )
        print(Fore.MAGENTA + "[ x ] " + Fore.GREEN + "Sair\n")
        print(Fore.MAGENTA + "===================================================\n")
        opt = input(
            Fore.MAGENTA + ">>> " + Fore.GREEN + "Digite a opção: " + Fore.LIGHTRED_EX
        )

        match opt:

            case "1":

                print(
                    "Para iniciar a extração os arquivos XML devem seguir o padrão de nome <<CartaCancelamento****.xml>, e devem estar localizados na pasta: 'src/data'"
                )

                iniciar = input("Iniciar extração (s/n)? ")

                match iniciar:
                    case "s":
                        extrair_dados()
                        pause()
                    case "n":
                        continue
                    case _:
                        print("Opção inválida!")

            case "2":
                ...

            case "3":
                print(
                    Fore.MAGENTA
                    + "\n=============== "
                    + Fore.GREEN
                    + "Lista Whatsapp business Accounts"
                    + Fore.MAGENTA
                    + " ===============\n"
                )
                for acc in get_business_account():
                    print(
                        Fore.MAGENTA
                        + "Nome: "
                        + Fore.GREEN
                        + acc.get("name")
                        + Fore.MAGENTA
                        + " - Phone ID: "
                        + Fore.GREEN
                        + acc.get("phone_id")
                        + Fore.MAGENTA
                        + " - Phone Number: "
                        + Fore.GREEN
                        + acc.get("display_phone_number")
                    )
                pause()
            case "x":
                print("Encerrando sistema..")
            case _:
                print("Opção inválida!")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            operacao = sys.argv[1].lower()

            if operacao == "disparo":
                print(operacao)
            else:
                ...
        except Exception as e:
            print(f"erro: {e}")
    else:
        show_menu()
