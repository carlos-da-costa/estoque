# -*- coding: utf-8 -*-

def lista_produto():
    # faz select que retorna todos os produtos
    # retorn Rows
    produtos = db(db.produto).select()

    # cria uma representação para o campo id
    # que passará a ser um conjunto de links
    # CAT - helper que concatena elementos HTML
    # A - helper que cria um link 
    #   _class - define as classes css do elemento
    # URL - helper que cria uma url apropriada,
    #
    # o lançamento de estoque passa o 
    db.produto.id.represent = lambda value, row: CAT(A('Editar', _href=URL(c='estoque', f='produto', vars={'id_produto': value}), _class='btn btn-info'), ' ',
                                                     A('Lançar Estoque', _href=URL(c='estoque', f='movimento', vars={'id_produto': value}), _class='btn btn-info')
                                                    )

    # retorna um SQLTABLE, que vai transformar um Rows em TABLE HTML,
    # headers='labels' indica para pegar os títulos das colunas a partir dos rótulos dos campos
    # _class='table', classe table do bootstrap
    return dict(produtos=SQLTABLE(produtos, headers='labels', _class='table'))


def produto():

    if request.vars.id_produto:
        # se foi passao id do produto como variável na url, cria form de edição
        form = SQLFORM(db.produto, request.vars.id_produto)
    else:
        # caso contrário cria forma de inserção
        form = SQLFORM(db.produto)

    # processão validação do form
    form.process()

    return dict(form=form)


def lista_movimento():
    if request.vars.id_produto:
        # se foi passao id do produto como variável na url, lista apenas moviemtnação do produto
        movimentos = db(db.movimento.produto == request.vars.id_produto).select()
    else:
        # caso contrário lista moviemntação de todos produtos
        movimentos = db(db.movimento).select()

    # define a representação do campo id como um link para edição do mesmo
    db.movimento.id.represent = lambda value, row: A('Editar', _href=URL(c='estoque', f='movimento.html', vars={'id_movimento': value}))

    return dict(movimentos=SQLTABLE(movimentos, headers='labels', _class='table'))


def movimento():
    # define valor padrão do campo produto como a variável id_produto da url
    # válido somente a partir daqui e até terminar o request
    db.movimento.produto.default = request.vars.id_produto

    if request.vars.id_movimento:
        # se foi passao id do produto como variável na url, cria form de edição
        form = SQLFORM(db.movimento, request.vars.id_movimento)
    else:
        # caso contrário cria forma de inserção
        form = SQLFORM(db.movimento)

    # processa validação do form e checa se passou
    if form.process().accepted:
        # define soma do campo, mas não executa nada ainda
        soma = db.movimento.quantidade.sum()

        # executa a consulta filtrando o produto para o qual foi feito o movimento 
        # de estoque, e que seja de entrada
        # define que será retornado somente a soma
        # form.vars contém todas as variáveis do form
        # .first pega o primeiro registro
        # no primeiro registro, pegar a soma
        # or 0, para caso não hajam movimentações, retorna 0 para poder fazer o cálculo posterior
        entradas = db((db.movimento.produto == form.vars.produto) &
                      (db.movimento.tipo == 'e')
                      ).select(soma).first()[soma] or 0

        # mesma coisa com a saída
        saidas = db((db.movimento.produto == form.vars.produto) &
                    (db.movimento.tipo == 's')
                    ).select(soma).first()[soma] or 0

        # calcula
        total = entradas - saidas

        # atualiza produto por id
        db(db.produto.id == form.vars.produto).update(estoque_atual=total)


    return dict(form=form)
