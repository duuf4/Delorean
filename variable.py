import flet as ft
from datetime import datetime, timedelta
import time
import threading
import sqlite3
import os

def formatar_data(dt: datetime | None) -> str:
    if not dt:
        return "--- -- ---- --:--:-- --"
    return dt.strftime("%b %d %Y %I:%M:%S %p").upper()

class PainelDeloreanApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Painel DeLorean - De Volta para o Futuro"
        #self.page.bgcolor = ft.colors.BLACK

        self.page.bgcolor = ft.Colors.BLACK
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.theme_mode = ft.ThemeMode.DARK
        


        font_path = "fonts/DSEG7Classic-Bold.ttf"
        self.page.fonts = {"DSEG7": font_path}
        self.font_family = "DSEG7" if os.path.exists(os.path.join("assets", font_path)) else "monospace"

        self.destination_time = datetime.now()
        self.present_time = datetime.now()
        self.last_departed_time = None
        self.lembretes = []
        self.lock = threading.Lock()

        self._init_database()
        self.construir_layout()

        self.thread = threading.Thread(target=self.atualizar_tempos_em_loop, daemon=True)
        self.thread.start()

    def _init_database(self):
        self.conn = sqlite3.connect('lembretes.db', check_same_thread=False)
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lembretes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mensagem TEXT NOT NULL,
                horario TEXT NOT NULL
            )
        """)
        with self.lock:
            self.lembretes.clear()
            for row in cursor.execute("SELECT horario, mensagem FROM lembretes"):
                try:
                    tempo_lembrete = datetime.fromisoformat(row[0])
                    self.lembretes.append((tempo_lembrete, row[1]))
                except ValueError:
                    print(f"Erro ao carregar lembrete: {row}")
        self.conn.commit()

    def criar_display_tempo(self, titulo: str, cor_texto: str, valor_inicial: str):
        label = ft.Text(titulo, color=cor_texto, size=18, weight=ft.FontWeight.BOLD, font_family="monospace")
        valor = ft.Text(valor_inicial, font_family=self.font_family, color=cor_texto, size=48, weight=ft.FontWeight.W_900)
        return ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[label, valor]
            ),
            bgcolor="#080808",
            border=ft.border.all(4, cor_texto),
            border_radius=12,
            padding=20,
            margin=10,
            width=400,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(blur_radius=20, color=cor_texto, spread_radius=1),
        ), valor

    def construir_layout(self):
        self.display_destination, _ = self.criar_display_tempo("DESTINATION TIME", ft.Colors.RED_ACCENT_400, formatar_data(self.destination_time))
        self.display_present, self.present_label = self.criar_display_tempo("PRESENT TIME", ft.Colors.GREEN_ACCENT_400, formatar_data(self.present_time))
        self.display_last_departed, _ = self.criar_display_tempo("LAST TIME DEPARTED", ft.Colors.YELLOW_ACCENT_400, formatar_data(self.last_departed_time))

        self.lembrete_input = ft.TextField(label="Adicionar Lembrete", width=300, border_color=ft.Colors.BLUE_GREY_400)
        self.horario_input = ft.TextField(label="Horário (HH:MM)", width=150, border_color=ft.Colors.BLUE_GREY_400)

        add_button = ft.ElevatedButton(
            "Adicionar",
            icon=ft.Icons.ADD_ALARM,
            on_click=self.adicionar_lembrete_click,
            bgcolor=ft.Colors.BLUE_GREY_700,
            color=ft.Colors.WHITE
        )

        self.page.add(
            ft.Container(
                content=ft.Column(
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            wrap=True,
                            spacing=20,
                            run_spacing=20,
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
                                        wrap=True,
                                        spacing=10,
                                        run_spacing=10,
                                        controls=[self.lembrete_input, self.horario_input, add_button]
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
                padding=20,
            )
        )
        self.page.update()

    def adicionar_lembrete_click(self, e):
        texto = self.lembrete_input.value
        horario_str = self.horario_input.value

        if not texto or not horario_str:
            self.mostrar_dialogo("Erro", "Preencha a mensagem e o horário.")
            return

        try:
            hora, minuto = map(int, horario_str.split(":"))
            agora = datetime.now()
            tempo = agora.replace(hour=hora, minute=minuto, second=0, microsecond=0)
            if tempo < agora:
                tempo += timedelta(days=1)
            with self.lock:
                self.lembretes.append((tempo, texto))
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO lembretes (horario, mensagem) VALUES (?, ?)", (tempo.isoformat(), texto))
                self.conn.commit()
            self.lembrete_input.value = ""
            self.horario_input.value = ""
            self.page.update()
        except ValueError:
            self.mostrar_dialogo("Erro", "Formato HH:MM (ex: 14:30).")

    def mostrar_dialogo(self, titulo: str, conteudo: str):
        def fechar(e):
            self.page.dialog.open = False
            self.page.update()
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(titulo),
            content=ft.Text(conteudo),
            actions=[ft.TextButton("Ok", on_click=fechar)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dlg
        self.page.dialog.open = True
        self.page.update()

    def _update_ui(self, agora, lembretes_para_mostrar):
        self.present_label.value = formatar_data(agora)
        for texto in lembretes_para_mostrar:
            self.mostrar_dialogo("Lembrete!", texto)
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
                            self.mostrar_dialogo("Lembrete!", texto)  # Remova o run_threadsafe
                            lembretes_a_remover.append(lembrete)   

                if lembretes_a_remover:
                    with self.lock:
                        for lembrete in lembretes_a_remover:
                            self.lembretes.remove(lembrete)

                self.page.update()
            except Exception as e:
                print(f"Erro no loop de atualização: {e}")
            time.sleep(1)

def main(page: ft.Page):
    PainelDeloreanApp(page)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
