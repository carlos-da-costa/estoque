# -*- coding: utf-8 -*-

def lista_produto():
    produtos = db(db.produto).select()
    db.produto.id.represent = lambda value, row: CAT(A('Editar', _href=URL(c='estoque', f='produto', vars={'id_produto': value}), _class='btn btn-info'), ' ',
                                                     A('Lançar Estoque', _href=URL(c='estoque', f='movimento', vars={'id_produto': value}), _class='btn btn-info')
                                                    )

    return dict(produtos=SQLTABLE(produtos, headers='labels', _class='table'))


def produto():
    if request.vars.id_produto:
        form = SQLFORM(db.produto, request.vars.id_produto)
    else:
        form = SQLFORM(db.produto)

    form.process()

    return dict(form=form)


def lista_movimento():
    if request.vars.id_produto:
        movimentos = db(db.movimento.produto == request.vars.id_produto).select()
    else:
        movimentos = db(db.movimento).select()

    db.movimento.id.represent = lambda value, row: A('Editar', _href=URL(c='estoque', f='movimento.html', vars={'id_movimento': value}))

    return dict(movimentos=SQLTABLE(movimentos, headers='labels', _class='table'))


def movimento():
    db.movimento.produto.default = request.vars.id_produto

    if request.vars.id_movimento:
        form = SQLFORM(db.movimento, request.vars.id_movimento)
    else:
        form = SQLFORM(db.movimento)

    if form.process().accepted:
        soma = db.movimento.quantidade.sum()
        entradas = db((db.movimento.produto == form.vars.produto) &
                      (db.movimento.tipo == 'e')
                      ).select(soma).first()[soma] or 0
        saidas = db((db.movimento.produto == form.vars.produto) &
                    (db.movimento.tipo == 's')
                    ).select(soma).first()[soma] or 0
        total = entradas - saidas
        db(db.produto.id == form.vars.produto).update(estoque_atual=total)


    return dict(form=form)
