import mercadopago

public_key = 'APP_USR-385dee55-12bb-4ac9-abeb-cdd2887e082a'
token = 'APP_USR-3888656115317473-100115-e4e4d5bc890b96096cd35ae94dd0a28d-3728583515'


def criar_pagamento(itens_pedido, link):
    sdk = mercadopago.SDK(token)

    itens = []

    for item in itens_pedido:
        quantidade = int(item.quantidade)
        nome_produto = item.item_estoque.produto.nome
        preco_unitario = float(item.item_estoque.produto.preco)

        itens.append({
            "title": nome_produto,
            "quantity": quantidade,
            "unit_price": preco_unitario
        })
    print("LINK DE RETORNO:", link)
    preference_data = {
        "items": itens,
        "back_urls": {
            "success": link,
            "pending": link,
            "failure": link,
        },
        "auto_return": "approved",
        
    }
   
    resposta = sdk.preference().create(preference_data)

    print("====================================")
    print("RESPOSTA DO MERCADO PAGO:")
    print(resposta)
    print("====================================")

    response = resposta.get("response", {})

    print("RESPONSE:", response)

    link_pagamento = response.get("init_point")
    id_pagamento = response.get("id")

    print("LINK:", link_pagamento)
    print("ID:", id_pagamento)

    if not link_pagamento:
        raise Exception(f"Mercado Pago não retornou init_point: {resposta}")
        
    return link_pagamento, id_pagamento