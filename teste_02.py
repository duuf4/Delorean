import flet as ft

def main(page: ft.Page):
    page.title = "Lista de Compras"

    lista_compras = []

    def adicionar(item):
        if adicionar_item.value != "":
           lista_compras.append(adicionar_item.value)
           page.add(ft.Checkbox(label=adicionar_item.value))

    adicionar_item = ft.TextField(hint_text='O que preciso comprar ?',
                                  width=300,
                                  autofocus=True) 
    
    page.add(ft.Row([adicionar_item,
                    ft.ElevatedButton(text='+',
                                      on_click=adicionar)]))
    
ft.app(target=main)