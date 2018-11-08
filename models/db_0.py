# -*- coding: utf-8 -*-

# variável auxiliar para os tipos de entrada de estoque
# a chave será gravada no banco (ex. 'e', 's')
# o valor será exibido no <SELECT>
TIPO_MOVIMENTO = {'e':'Entrada', 's': 'Saída'}

db.define_table('produto',
                Field('nome','string',label='Nome do Produto'),
                Field('estoque_atual','integer',label='Quantidade', default=0),
                format='%(nome)s' # string exibida nos campos de referência
                )


db.define_table('movimento',
                Field('tipo',
                      requires=IS_IN_SET(TIPO_MOVIMENTO), # valida entrada e monta SELECT no html
                      represent=lambda value, row: TIPO_MOVIMENTO.get(value, '') # se houver valor no campo mostra o texto correspondente
                      ),
                Field('produto', db.produto, label='Produto'),
                Field('quantidade', 'integer', label='Quantidade de Produto'),
                )
