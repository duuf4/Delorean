import tkinter as tk
from datetime import datetime
import time
import threading

def formatar_data(dt):
    return dt.strftime("%b %d %Y %I:%M %p").upper()

class PainelDelorean:
    def __init__(self, root):
        self.root = root
        self.root.title("Painel DeLorean - Back to the Future")
        self.root.configure(bg="black")

        self.labels = {}

        for i, (label, cor) in enumerate([
            ("DESTINATION TIME", "#00FF00"),
            ("PRESENT TIME", "#FF0000"),
            ("LAST TIME DEPARTED", "#FFFF00")
        ]):
            tk.Label(root, text=label, fg=cor, bg="black",
                     font=("Courier", 16, "bold")).grid(row=i*2, column=0, sticky="w", padx=10)
            lbl = tk.Label(root, text="--- -- ---- --:-- --", fg=cor, bg="black",
                           font=("DS-Digital", 28, "bold"))  # Fonte digital
            lbl.grid(row=i*2+1, column=0, sticky="w", padx=10)
            self.labels[label] = lbl

        self.destination_time = datetime(2025, 10, 21, 16, 29)
        self.last_departed_time = None

        self.atualizar_tempos()

    def atualizar_tempos(self):
        # Atualiza data atual continuamente
        def loop():
            while True:
                now = datetime.now()
                self.labels["PRESENT TIME"].config(text=formatar_data(now))
                self.labels["DESTINATION TIME"].config(text=formatar_data(self.destination_time))

                if self.last_departed_time:
                    self.labels["LAST TIME DEPARTED"].config(text=formatar_data(self.last_departed_time))
                time.sleep(1)

        t = threading.Thread(target=loop, daemon=True)
        t.start()

# Cria janela
root = tk.Tk()
app = PainelDelorean(root)
root.mainloop()