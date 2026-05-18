import tkinter as tk
from tkinter import messagebox
from database import authenticate, create_user

class LoginWindow:
    def __init__(self, root, success):
        self.root = root
        self.user = None
        self.success = success
        
        self.win = tk.Toplevel(root)
        self.win.title("AutoMSF - Entrar")
        self.win.geometry("420x380")
        self.win.configure(bg="#F4F6FA")
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW", root.destroy)

        lbl_title = tk.Label(self.win, text="AutoMSF", bg="#F4F6FA", fg="#2c3e50", font=("Arial", 22, "bold"))
        lbl_title.pack(pady=(30, 5))
        lbl_subtitle = tk.Label(self.win,text="Área de Acesso",bg="#F4F6FA",fg="#7f8c8d",font=("Arial", 11))
        lbl_subtitle.pack(pady=(0, 25))
        
        lbl_user = tk.Label(self.win, text="Utilizador", bg="#F4F6FA", fg="#2c3e50", font=("Arial", 10, "bold"))
        lbl_user.pack(anchor="w", padx=40)
        self.ent_user = tk.Entry(self.win, font=("Arial", 11), relief="solid", bd=1)
        self.ent_user.pack(fill="x", padx=40, pady=(5, 15), ipady=7)


        lbl_pass = tk.Label(self.win, text="Senha", bg="#F4F6FA", fg="#2c3e50", font=("Arial", 10, "bold"))
        lbl_pass.pack(anchor="w", padx=40)
        self.ent_pass = tk.Entry(self.win, show="*", font=("Arial", 11), relief="solid", bd=1)
        self.ent_pass.pack(fill="x", padx=40, pady=(5, 25), ipady=7)
             

        btn_login = tk.Button(self.win, text="Entrar", command=self.validate, bg="#2980b9", fg="white",
            activebackground="#3498db", activeforeground="white", relief="flat", cursor="hand2", font=("Arial", 11, "bold"))
        btn_login.pack(fill="x", padx=40, ipady=8)

    def validate(self):
        username = self.ent_user.get().strip()
        password = self.ent_pass.get().strip()

        if not username or not password:
            messagebox.showwarning("Aviso", "Preencha utilizador e senha")
            return
        
        user = authenticate(username, password)
        
        if user:
            self.user = user
            self.win.destroy()
            self.success() # Executa a função para mostrar a principal
        else:
            messagebox.showerror("Erro", "Utilizador ou senha inválidos")
