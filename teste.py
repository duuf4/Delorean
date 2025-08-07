import flet 
from flet import Page, Row, TextField, IconButton, Icons  # Corrija aqui: use 'Icons' com I maiúsculo

def main(page: Page):
    page.title = "Meu Programa"
    page.vertical_alignment = 'center'

    valor1 = TextField(value='0',
                       text_align='right',
                       width=80,)
    
    def diminui_num(num):
        valor1.value = int(valor1.value) - 1
        page.update()

    def aumenta_num(num):
        valor1.value = int(valor1.value) + 1
        page.update()

    page.add(Row([
        IconButton(Icons.REMOVE, on_click=diminui_num),  # Corrija aqui
        valor1,
        IconButton(Icons.ADD, on_click=aumenta_num),      # Corrija aqui
    ],
    alignment='center',
    ))

flet.app(target=main)   