import tkinter as tk
from tkinter import ttk
from operaciones_finalizadas import create_operaciones_finalizadas_tab
from historicos import create_historicos_tab

# Create the main application window
root = tk.Tk()
root.title("HTML Parser")

# Create a Notebook (Tabbed Interface)
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Create the "Operaciones Finalizadas" tab
create_operaciones_finalizadas_tab(notebook)

# Create the "Históricos" tab
create_historicos_tab(notebook)

# Start the tkinter main loop
root.mainloop()
