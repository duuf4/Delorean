import os
import tkinter as tk

# Corrige caminhos para o Tcl e Tk
os.environ['TCL_LIBRARY'] = r'C:\Users\daniel.silva\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\daniel.silva\AppData\Local\Programs\Python\Python313\tcl\tk8.6'

root = tk.Tk()
root.mainloop()
