import tkinter as tk
from ui.menu import MenuInicio

def main():
    root = tk.Tk()
    root.title("Simulador de Planificación de Procesos — Menú")
    root.geometry("520x360")
    MenuInicio(root).pack(fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
