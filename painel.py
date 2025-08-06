import tkinter as tk
from datetime import datetime
import time
import threading

def formatar_data(dt):
    return dt.strftime("%b %d %Y %I:%M %p").upper()

# class PainelDelorean:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Painel DeLorean - Back to the Future")
#         self.root.configure(bg="black")

#         self.labels = {}

#         for i, (label, cor) in enumerate([
#             ("DESTINATION TIME", "#00FF00"),
#             ("PRESENT TIME", "#FF0000"),
#             ("LAST TIME DEPARTED", "#FFFF00")
#         ]):
#             tk.Label(root, text=label, fg=cor, bg="black",
#                      font=("Courier", 16, "bold")).grid(row=i*2, column=0, sticky="w", padx=10)
#             lbl = tk.Label(root, text="--- -- ---- --:-- --", fg=cor, bg="black",
#                            font=("DS-Digital", 28, "bold"))  # Fonte digital
#             lbl.grid(row=i*2+1, column=0, sticky="w", padx=10)
#             self.labels[label] = lbl

#         self.destination_time = datetime(2025, 10, 21, 16, 29)
#         self.last_departed_time = None

#         self.atualizar_tempos()

#     def atualizar_tempos(self):
#         # Atualiza data atual continuamente
#         def loop():
#             while True:
#                 now = datetime.now()
#                 self.labels["PRESENT TIME"].config(text=formatar_data(now))
#                 self.labels["DESTINATION TIME"].config(text=formatar_data(self.destination_time))

#                 if self.last_departed_time:
#                     self.labels["LAST TIME DEPARTED"].config(text=formatar_data(self.last_departed_time))
#                 time.sleep(1)

#         t = threading.Thread(target=loop, daemon=True)
#         t.start()

# # Cria janela
# root = tk.Tk()
# app = PainelDelorean(root)
# root.mainloop()

# ...existing code...

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

        # Campos para lembrete
        tk.Label(root, text="Lembrete:", fg="white", bg="black").grid(row=6, column=0, sticky="w", padx=10, pady=(20,0))
        self.lembrete_entry = tk.Entry(root, width=30)
        self.lembrete_entry.grid(row=7, column=0, sticky="w", padx=10)

        tk.Label(root, text="Horário (HH:MM):", fg="white", bg="black").grid(row=8, column=0, sticky="w", padx=10)
        self.horario_entry = tk.Entry(root, width=10)
        self.horario_entry.grid(row=9, column=0, sticky="w", padx=10)

        tk.Button(root, text="Adicionar Lembrete", command=self.adicionar_lembrete).grid(row=10, column=0, sticky="w", padx=10, pady=5)

        self.lembretes = []

        self.destination_time = datetime(2025, 10, 21, 16, 29)
        self.last_departed_time = None

        self.atualizar_tempos()

    def adicionar_lembrete(self):
        texto = self.lembrete_entry.get()
        horario = self.horario_entry.get()
        try:
            hora, minuto = map(int, horario.split(":"))
            agora = datetime.now()
            lembrete_time = agora.replace(hour=hora, minute=minuto, second=0, microsecond=0)
            if lembrete_time < agora:
                lembrete_time = lembrete_time.replace(day=agora.day + 1)
            self.lembretes.append((lembrete_time, texto))
            self.lembrete_entry.delete(0, tk.END)
            self.horario_entry.delete(0, tk.END)
        except Exception:
            tk.messagebox.showerror("Erro", "Horário inválido. Use o formato HH:MM.")

    def atualizar_tempos(self):
        def loop():
            while True:
                now = datetime.now()
                self.labels["PRESENT TIME"].config(text=formatar_data(now))
                self.labels["DESTINATION TIME"].config(text=formatar_data(self.destination_time))

                if self.last_departed_time:
                    self.labels["LAST TIME DEPARTED"].config(text=formatar_data(self.last_departed_time))

                # Verifica lembretes
                for lembrete in self.lembretes[:]:
                    lembrete_time, texto = lembrete
                    if now >= lembrete_time:
                        self.root.after(0, lambda t=texto: tk.messagebox.showinfo("Lembrete", t))
                        self.lembretes.remove(lembrete)
                time.sleep(1)

        t = threading.Thread(target=loop, daemon=True)
        t.start()

# Cria janela
root = tk.Tk()
import tkinter.messagebox  # Necessário para messagebox
app = PainelDelorean(root)
root.mainloop()