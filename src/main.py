import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from colorama import Fore, Style, init
from data.templates import update_templates_list
from controller.controller import get_business_account, cadastrar_business_account
from data.extract_data import extrair_dados
from model.Models import create_tables
from database.db import create_database_if_not_exists, tables_created

# Criação do banco de dados, caso não exista.
create_database_if_not_exists()

# Chamar a criação de tabelas, caso todas
# as tabelas necessárias não estiverem criadas.
if len(tables_created) < 7:
    create_tables()


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


# Função para aguardar um comando para continuar do usuário.
def pause():
    programPause = input("\nPressione <ENTER> para continuar...")


# Função para exibir o menu
def show_menu():
    print(Fore.CYAN + logo)
    print(Fore.GREEN + "Inicializando sistema\n")
    print(
        Fore.GREEN
        + ">>> Para iniciar os "
        + Fore.CYAN
        + "disparos " + Fore.GREEN + "utilizar: "
        + Fore.MAGENTA
    )
    print(
        Fore.GREEN
        + "python "
        + Fore.LIGHTRED_EX
        + "main.py "
        + Fore.MAGENTA
        + "<<nome business account>>\n"
    )
    opt = "0"
    while opt != "x":

        # Opções do menu
        print(Fore.MAGENTA + "===================================================\n")
        print(Fore.MAGENTA + "[ 1 ] " + Fore.GREEN + "Extrair dados do XML\n")
        print(
            Fore.MAGENTA
            + "[ 2 ] "
            + Fore.GREEN
            + "Inserir dados da tabela de Contas Whatsapp business\n"
        )

        print(
            Fore.MAGENTA + "[ 3 ] " + Fore.GREEN + "Listar contas Whatsapp business\n"
        )
        print(
            Fore.MAGENTA
            + "[ 4 ] "
            + Fore.GREEN
            + "Atualizar/Inserir dados da tabela de templates "
            + Fore.RED
            + "(Obs: os dados das contas devem ter sido inseridos antes.)\n"
        )
        print(Fore.MAGENTA + "[ x ] " + Fore.GREEN + "Sair\n")
        print(Fore.MAGENTA + "===================================================\n")

        opt = input(
            Fore.MAGENTA + ">>> " + Fore.GREEN + "Digite a opção: " + Fore.LIGHTRED_EX
        )

        # Executar a opção escolhida.
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
                print(
                    Fore.MAGENTA
                    + "\n=============== "
                    + Fore.GREEN
                    + "Inserindo/Atualizando dados das Whatsapp Business Accounts.."
                    + Fore.MAGENTA
                    + " ===============\n"
                )
                cadastrar_business_account()
                pause()

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
            case "4":
                print(Style.RESET_ALL)
                update_templates_list()
                pause()

            case "x":
                print("Encerrando sistema..")
            case _:
                print("Opção inválida!")


# Verificar se foi passado parâmetro na execução do script, para exibir ou não o menu.
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
