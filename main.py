import tkinter as tk
from database import init_db
from login import LoginWindow

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AutoMSF - Aluguer de Carros")
        self.root.geometry("600x400")
        self.root.withdraw() # Ocultar
        
        init_db()
        self.login = LoginWindow(self.root, self.show)
        
        self.root.mainloop()

    def show(self):
        self.user = self.login.user
        tk.Label(self.root, text="SISTEMA DE GESTÃO DE ALUGUER DE CARROS", font=("Arial", 18)).pack(expand=True)
        tk.Label(self.root, text=f"Bem-vindo, {self.user['name']}!", font=("Arial", 14)).pack(expand=True)
        tk.Button(self.root, text="Sair", command=self.root.quit).pack(pady=10)
                
        self.root.deiconify() # Mostrar

if __name__ == "__main__":
    MainWindow()