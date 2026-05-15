import tkinter as tk
from tkinter import messagebox
from database import authenticate

class LoginWindow:
    def __init__(self, root, success):
        self.root = root
        self.user = None
        self.success = success
        
        self.win = tk.Toplevel(root)
        self.win.title("AutoMSF - Aluguer de Carros - Entrar")
        self.win.geometry("400x250")
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW", root.destroy)

        tk.Label(self.win, text="Área de Acesso", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(self.win, text="Utilizador:").pack()
        self.ent_user = tk.Entry(self.win)
        self.ent_user.pack(pady=5)

        tk.Label(self.win, text="Senha:").pack()
        self.ent_pass = tk.Entry(self.win, show="*")
        self.ent_pass.pack(pady=5)

        tk.Button(self.win, text="Entrar", command=self.validate).pack(pady=20)

    def validate(self):
        username = self.ent_user.get()
        password = self.ent_pass.get()
        
        user = authenticate(username, password)
        
        if user:
            self.user = user
            self.win.destroy()
            self.success() # Executa a função para mostrar a principal
        else:
            messagebox.showerror("Erro", "Utilizador ou senha inválidos")