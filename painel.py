import flet as ft
from datetime import datetime, timedelta
import time
import threading

# --- Funções Auxiliares ---

def formatar_data(dt):
    """Formata um objeto datetime no estilo do painel DeLorean."""
    if not dt:
        # Retorna um placeholder se a data for Nula
        return "--- -- ---- --:--:-- --"
    # Formato: MÊS DIA ANO HORA:MINUTO:SEGUNDO AM/PM
    return dt.strftime("%b %d %Y %I:%M:%S %p").upper()

# --- Classe Principal da Aplicação ---

class PainelDeloreanApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Painel DeLorean - De Volta para o Futuro"
        self.page.bgcolor = ft.Colors.BLACK
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.fonts = {
            "DSEG7": "fonts/DSEG7Classic-Bold.ttf", 
        }
        self.font_family = "DSEG7" if "DSEG7" in self.page.fonts else "monospace"

        # --- Estado da Aplicação ---
        self.destination_time = datetime.now()
        self.present_time = datetime.now()
        self.last_departed_time = datetime.now()
        
        self.lembretes = []
        self.lock = threading.Lock()
        self.construir_layout()
        self.thread = threading.Thread(target=self.atualizar_tempos_em_loop, daemon=True)
        self.thread.start()

    def criar_display_tempo(self, titulo: str, cor_texto: str, valor_inicial: str) -> ft.Container:
        """Cria um bloco de display de tempo padronizado com destaque visual."""
        return ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(titulo, color=cor_texto, size=20, weight=ft.FontWeight.BOLD, font_family="monospace"),
                    ft.Text(
                        valor_inicial,
                        font_family=self.font_family,
                        color=cor_texto,
                        size=48,
                        weight=ft.FontWeight.W_900,
                    ),
                ]
            ),
            bgcolor="#222222",
            border=ft.border.all(3, cor_texto),
            border_radius=10,
            padding=20,
            margin=10,
            width=340,
            alignment=ft.alignment.center,
        )

    def construir_layout(self):
        """Cria e organiza todos os controles na página."""
        # Displays de tempo
        self.display_destination = self.criar_display_tempo("DESTINATION TIME", ft.Colors.GREEN_ACCENT_400, formatar_data(self.destination_time))
        self.display_present = self.criar_display_tempo("PRESENT TIME", ft.Colors.RED_ACCENT_400, formatar_data(self.present_time))
        self.display_last_departed = self.criar_display_tempo("LAST TIME DEPARTED", ft.Colors.YELLOW_ACCENT_400, formatar_data(self.last_departed_time))

        # Campos de entrada para lembretes
        self.lembrete_input = ft.TextField(
            label="Adicionar Lembrete", 
            width=300, 
            border_color=ft.Colors.BLUE_GREY_400
        )
        self.horario_input = ft.TextField(
            label="Horário (HH:MM)", 
            width=150, 
            border_color=ft.Colors.BLUE_GREY_400
        )
        
        # Botão para adicionar lembrete
        add_button = ft.ElevatedButton(
            "Adicionar",
            icon=ft.Icons.ADD_ALARM, # CORRIGIDO: ft.Icons
            on_click=self.adicionar_lembrete_click,
            bgcolor=ft.Colors.BLUE_GREY_700,
            color=ft.Colors.WHITE
        )

        # Layout principal ajustado
        self.page.add(
            ft.Container(
                content=ft.Column(
                    spacing=40,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=30,
                            controls=[
                                self.display_destination,
                                self.display_present,
                                self.display_last_departed,
                            ]
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("LEMBRETES", size=18, color=ft.Colors.BLUE_GREY_200, weight=ft.FontWeight.BOLD, font_family="monospace"),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=10,
                                        controls=[
                                            self.lembrete_input,
                                            self.horario_input,
                                            add_button,
                                        ]
                                    )
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10,
                            ),
                            bgcolor="#181C20",
                            border_radius=8,
                            padding=20,
                            margin=ft.margin.only(top=20),
                        )
                    ]
                ),
                alignment=ft.alignment.center,
                expand=True,
                padding=30,
            )
        )
        self.page.update()

    def adicionar_lembrete_click(self, e):
        """Callback para o botão de adicionar lembrete."""
        texto_lembrete = self.lembrete_input.value
        horario_str = self.horario_input.value

        if not texto_lembrete or not horario_str:
            self.mostrar_dialogo("Erro", "Preencha o lembrete e o horário.")
            return

        try:
            hora, minuto = map(int, horario_str.split(":"))
            agora = datetime.now()
            tempo_lembrete = agora.replace(hour=hora, minute=minuto, second=0, microsecond=0)

            if tempo_lembrete < agora:
                tempo_lembrete += timedelta(days=1)
            
            with self.lock:
                self.lembretes.append((tempo_lembrete, texto_lembrete))

            self.lembrete_input.value = ""
            self.horario_input.value = ""
            self.page.update()
            self.mostrar_dialogo("Sucesso", f"Lembrete '{texto_lembrete}' adicionado para as {horario_str}.")

        except ValueError:
            self.mostrar_dialogo("Erro de Formato", "Use o formato de horário HH:MM.")

    def mostrar_dialogo(self, titulo: str, conteudo: str):
        """Exibe um diálogo de alerta na tela de forma segura a partir de threads."""
        def fechar_dialogo(e):
            self.page.dialog.open = False
            self.page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(titulo),
            content=ft.Text(conteudo),
            actions=[
                ft.TextButton("Ok", on_click=fechar_dialogo)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dlg
        self.page.dialog.open = True
        self.page.update()

    def atualizar_tempos_em_loop(self):
        """Loop principal que roda em uma thread separada para atualizar a UI."""
        while True:
            try:
                agora = datetime.now()
                # Atualiza todos os relógios com segundos em tempo real
                self.display_present.content.controls[1].value = formatar_data(agora)
                self.display_destination.content.controls[1].value = formatar_data(self.destination_time)
                self.display_last_departed.content.controls[1].value = formatar_data(self.last_departed_time)

                # Verifica se há lembretes para disparar
                lembretes_a_remover = []
                with self.lock:
                    for lembrete in self.lembretes:
                        tempo_lembrete, texto = lembrete
                        if agora >= tempo_lembrete:
                            self.page.run_threadsafe(self.mostrar_dialogo, "Lembrete!", texto)
                            lembretes_a_remover.append(lembrete)

                if lembretes_a_remover:
                    with self.lock:
                        for lembrete in lembretes_a_remover:
                            self.lembretes.remove(lembrete)

                self.page.update()
            except Exception as e:
                print(f"Erro no loop de atualização: {e}")
            time.sleep(1)

# --- Ponto de Entrada da Aplicação ---
def main(page: ft.Page):
    PainelDeloreanApp(page)

if __name__ == "__main__":
    # Certifique-se de ter uma pasta 'assets' no mesmo diretório do seu script.
    ft.app(target=main, assets_dir="assets")



