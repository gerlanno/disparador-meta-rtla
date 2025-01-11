def convert_to_brl(value):

    """
    Converter e formatar valores para o formato de moeda Real do Brasil.
    """
    value_brl = (
        (
            f"R$ {float(value.replace(',','').replace('.', ''))/100:_.2f}"
        )
        .replace(".", ",")
        .replace("_", ".")
    )

    return value_brl


