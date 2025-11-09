#!/usr/bin/env python3
# main.py (CLI)
from re import X
import sys
import os
import argparse
from colorama import Fore, Style, init
from extract_data import extrair_dados
from database.db import create_database_if_not_exists, check_tables
from model.Models import create_tables
from sender import disparar
from controller.controller import (
    get_business_account,
    cadastrar_business_account,
    atualizar_contato,
    del_zapfailed,
    update_zapenviado,
    att_iswhatsapp,
    titulos_para_enviar,
)
from templates import update_templates_list
from utils.logger import Logger
from utils.tools import zapeviados_to_csv
from IA_classificador import classificar_mensagens

logger = Logger().get_logger()

# Criação do banco de dados, caso não exista.
db_created = create_database_if_not_exists()

# Chamar a criação de tabelas, caso todas as tabelas necessárias não estejam criadas.
if db_created:
    tables_created = check_tables()
    if len(tables_created) < 7:
        create_tables()

# Inicializa o colorama
init(autoreset=True)


def pause():
    input("\nPressione <ENTER> para continuar...")


def show_menu():
    """Menu interativo (mantive seu menu original)."""
    print(Fore.GREEN + "Inicializando sistema\n")
    print(
        Fore.GREEN
        + ">>> Para iniciar os "
        + Fore.CYAN
        + "disparos "
        + Fore.GREEN
        + "utilizar: "
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
        print(
            Fore.MAGENTA
            + "[ 5 ] "
            + Fore.GREEN
            + "Exportar tabela zapenviados para arquivo csv\n"
        )
        print(
            Fore.MAGENTA
            + "[ 6 ] "
            + Fore.GREEN
            + "Atualizar contatos sem número."
            + Fore.RED
            + "(colocar o arquivo csv com documento e telefone na pasta src/data.)\n"
        )
        print(
            Fore.MAGENTA
            + "[ 7 ] "
            + Fore.GREEN
            + "Atualizar contatos errados - Filtro IA\n"
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
                        print(extrair_dados())
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
            case "5":
                print(Style.RESET_ALL)
                zapeviados_to_csv()
                pause()
            case "6":
                print(Style.RESET_ALL)
                atualizar_contato()
                pause()
            case "7":
                print(Style.RESET_ALL)
                data = input(
                    "Deseja informar data inicial? (ex: 2025-05-05 ou em branco para todos)"
                )
                if data:
                    classificar_mensagens(data)
                else:
                    classificar_mensagens()
                pause()
            ##### #Funções Ocultas######
            case "del":
                del_zapfailed()
                pause()
            case "attzap":
                update_zapenviado()
                pause()
            case "iswhats":
                att_iswhatsapp()
                pause()
            case "titulos":
                cartorio = input("Código Cartório? (em branco para todos)")
                if cartorio:
                    print(titulos_para_enviar(cartorio=(cartorio)))
                else:
                    print(titulos_para_enviar())
                pause()
            ############################
            case "x":
                print("Encerrando sistema..")
            case _:
                print("Opção inválida!")


def cli_extract(args):
    print(extrair_dados())


def cli_cadastrar_account(args):
    cadastrar_business_account()


def cli_list_accounts(args):
    for acc in get_business_account():
        print(
            f"Nome: {acc.get('name')} - Phone ID: {acc.get('phone_id')} - Phone Number: {acc.get('display_phone_number')}"
        )


def cli_update_templates(args):
    update_templates_list()


def cli_export_zapenviados(args):
    zapeviados_to_csv()


def cli_update_contatos(args):
    atualizar_contato()


def cli_classify(args):
    if args.date:
        classificar_mensagens(args.date)
    else:
        classificar_mensagens()


def cli_del_zapfailed(args):
    del_zapfailed()


def cli_update_zapenviado(args):
    update_zapenviado()


def cli_att_iswhatsapp(args):
    att_iswhatsapp()


def cli_titulos(args):
    print(
        titulos_para_enviar(cartorio=args.cartorio, mes_ano_insert=args.mes_ano)
        if args.cartorio or args.mes_ano
        else titulos_para_enviar()
    )


def cli_disparar(args):
    business_acc_name = args.wba.upper()
    qtd_disparos = args.qtd
    mes_ano = args.mes_ano

    business_accs = get_business_account()
    for acc in business_accs:
        if business_acc_name in acc.values():
            print("Iniciando disparos..")
            try:
                print(disparar(business_acc_name=business_acc_name, qtd_disparos=(qtd_disparos if qtd_disparos else None), mes_ano=mes_ano))                
            except Exception as e:
                logger.error(e)
            break
    else:
        print(Fore.RED + f"Business account '{args.business}' não encontrada.")



def build_parser():
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="CLI para gerenciar extrações, templates, contas e disparos do sistema",
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Abrir menu interativo (GUI de terminal).",
    )
    subparsers = parser.add_subparsers(title="subcommands", dest="command")

    # extract
    p = subparsers.add_parser(
        "extract", help="Extrair dados dos XML (Coloque os arquivos em src/data)."
    )
    p.set_defaults(func=cli_extract)

    # cadastrar account
    p = subparsers.add_parser(
        "add-account", help="Inserir/Atualizar Whatsapp Business Accounts."
    )
    p.set_defaults(func=cli_cadastrar_account)

    # listar accounts
    p = subparsers.add_parser(
        "list-accounts", help="Listar Whatsapp Business Accounts."
    )
    p.set_defaults(func=cli_list_accounts)

    # update templates
    p = subparsers.add_parser("update-templates", help="Atualizar/Inserir templates.")
    p.set_defaults(func=cli_update_templates)

    # export zapenviados
    p = subparsers.add_parser(
        "export-zapenviados", help="Exportar tabela zapenviados para CSV."
    )
    p.set_defaults(func=cli_export_zapenviados)

    # atualizar contatos
    p = subparsers.add_parser(
        "update-contatos", help="Atualizar contatos sem número (usa src/data)."
    )
    p.set_defaults(func=cli_update_contatos)

    # classificar mensagens
    p = subparsers.add_parser(
        "classify",
        help="Classificar mensagens com IA (opcional: informar data inicial).",
    )
    p.add_argument("--date", "-d", help="Data inicial (ex: 2025-05-05).")
    p.set_defaults(func=cli_classify)

    # hidden / admin commands
    p = subparsers.add_parser("del-zapfailed", help=argparse.SUPPRESS)
    p.set_defaults(func=cli_del_zapfailed)
    p = subparsers.add_parser("update-zapenviado", help=argparse.SUPPRESS)
    p.set_defaults(func=cli_update_zapenviado)
    p = subparsers.add_parser("att-iswhatsapp", help=argparse.SUPPRESS)
    p.set_defaults(func=cli_att_iswhatsapp)

    # titulos
    p = subparsers.add_parser("titulos", help="Mostrar títulos para envio.")
    p.add_argument("--cartorio", "-c", help="Código do cartório (opcional).")
    p.add_argument("--mes-ano", "-m", help="Filtrar por mes_ano_insert (ex: 102025).")
    p.set_defaults(func=cli_titulos)

    # disparar (positional business)
    p = subparsers.add_parser("disparar", help="Iniciar disparos informando o nome da business account.")
    p.add_argument("--wba", "-wba", help="Nome da business account (ex: 'MINHA-ACCOUNT').")
    p.add_argument("--qtd", "-q", type=int, help="Quantidade de disparos (opcional).")
    p.add_argument("--mes-ano", "-m", help="Mês e ano do envio (ex: 102025).")
    p.set_defaults(func=cli_disparar)


    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    # Se não passou subcomando e não pediu interactive -> exibe ajuda
    if args.interactive:
        show_menu()
        return

    if not args.command:
        parser.print_help()
        return

    # Executa a função do subcomando
    try:
        args.func(args)
    except Exception as e:
        logger.error("Erro ao executar comando: %s", e, exc_info=True)


if __name__ == "__main__":
    main()
