""" Módulo para verificar aninhamento de listas
Este é o módulo "nester.py", e fornece uma função chamada print_lol()
que imprime listas que podem ou não incluir listas aninhadas."""

import sys
def print_lol(the_list, indent=False, level=0, fh=sys.stdout):
    """ Percorre toda a lista para encontrar sublista e mostrar o resultado na tela
    Esta função requer um argumento posicional chamado "the_list", que é qualquer lista
    Python (de possíveis listas aninhadas). Cada item de dados na lista fornecida é
    (recursivamente) impresso na tela em sua própria linha."""

    #Versão 1.4, adicionada opção para trabalhar com arquivos
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+ 1, fh)
        else:
            if indent:
                for tab_stop in range(level):
                    print('\t', end = '', file=fh)
                print(each_item, file=fh)