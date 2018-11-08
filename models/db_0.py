# -*- coding: utf-8 -*-
TIPO_MOVIMENTO = {'e':'Entrada', 's': 'Saída'}

db.define_table('produto',
                Field('nome','string',label='Nome do Produto'),
                Field('estoque_atual','integer',label='Quantidade', default=0),
                format='%(nome)s'
                )


db.define_table('movimento',
                Field('tipo',
                      requires=IS_IN_SET(TIPO_MOVIMENTO),
                      represent=lambda value, row: TIPO_MOVIMENTO.get(value, '')
                      ),
                Field('produto', db.produto, label='Produto'),
                Field('quantidade', 'integer', label='Quantidade de Produto'),
                )
