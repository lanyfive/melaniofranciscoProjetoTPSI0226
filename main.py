import tkinter as tk
from tkinter import ttk, messagebox
from database import init_db, get_connection, statistics
from login import LoginWindow
from service import CustomerService, CarService, RentalService, InvoiceService

class MainWindow (tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        self.title("AutoMSF - Aluguer de Carros")
        self.geometry("1000x680")
        self.minsize(880, 560)
        self.configure(bg="#F4F6FA")

        self.withdraw() # Ocultar
        
        init_db()
        self.login = LoginWindow(self, self.show)
        
        self.car_service = CarService()
        self.customer_service = CustomerService()
        self.rental_service = RentalService()
        self.invoice_service = InvoiceService()

        self.mainloop()

# =========================================
# HANDLERS - CUSTOMERS
# =========================================
    def handle_insert_customer(self, name, nif, idcard, birthdate, email, phone, address, drivinglicense):
        try:
            self.customer_service.create_customer(name, nif, idcard, birthdate, email, phone, address, drivinglicense)            
            messagebox.showinfo("Sucesso", "Cliente criado com sucesso.")
            self.show_customers()
        except ValueError as e:
            messagebox.showerror("Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

# =========================================
# HANDLERS - CARS
# =========================================
    def handle_insert_car(self, brand, model, year, plate, category, fuel_type, insurance, daily_rate):
        try:
            self.car_service.create_car(brand, model, year, plate, category, fuel_type, insurance, daily_rate)
            messagebox.showinfo("Sucesso", "Carro criado com sucesso.")
            self.show_insert_car()
        except ValueError as e:
            messagebox.showerror("Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

# =========================================
# HANDLERS - RENTALS
# =========================================
    def handle_insert_rental(self):
        pass

# =========================================
# HANDLERS - INVOICES
# =========================================
    def handle_insert_invoice(self):
        pass

# =========================================
# HANDLERS - USERS
# =========================================
    def handle_insert_user(self, nome, login, role):
        try:
            self.login.insert_user(nome, login, role)
            messagebox.showinfo("Sucesso", "Utilizador criado com sucesso.")
        except ValueError as e:
            messagebox.showerror("Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro", str(e))


    def show(self):
        navbar = tk.Frame(self, bg="#2c3e50", height=50)
        navbar.pack(fill="x")

        btn_dashboard = tk.Button(navbar, text="Dashboard", bg="#34495e", fg="white", relief="flat", padx=20, command=self.show_dashboard)
        btn_dashboard.pack(side="left", padx=5, pady=10)

        btn_customers = tk.Button(navbar, text="Clientes", bg="#34495e", fg="white", relief="flat", padx=20, command=self.show_customers)
        btn_customers.pack(side="left", padx=5, pady=10)

        if self.login.user['role'] == 'admin':
            btn_fleet = tk.Button(navbar, text="Frota", bg="#34495e", fg="white", relief="flat", padx=20, command=self.show_fleet)
            btn_fleet.pack(side="left", padx=5, pady=10)

        btn_rentals = tk.Button(navbar, text="Aluguer", bg="#34495e", fg="white", relief="flat", padx=20, command=self.show_rentals)
        btn_rentals.pack(side="left", padx=5, pady=10)

        btn_invoices = tk.Button(navbar, text="Faturas", bg="#34495e", fg="white", relief="flat", padx=20, command=self.show_invoices)
        btn_invoices.pack(side="left", padx=5, pady=10)

        if self.login.user['role'] == 'admin':
            btn_users = tk.Button(navbar, text="Utilizadores", bg="#34495e", fg="white", relief="flat", padx=20, command=self.show_users)
            btn_users.pack(side="left", padx=5, pady=10)

        btn_logout = tk.Button(navbar, text="Terminar Sessão", bg="#34495e", fg="white", relief="flat", padx=20, command=self.logout)
        btn_logout.pack(side="right", padx=5, pady=10)

        logged_user = tk.Label(navbar, text=self.login.user['name'], bg="#2c3e50", fg="white", font=("Arial", 14, "bold"))
        logged_user.pack(side="right", padx=15)

        self.main_content = tk.Frame(self, bg="#F4F6FA")
        self.main_content.pack(fill="both", expand=True)

        self.show_dashboard()
                
        self.deiconify() # Mostrar
    
    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

# =========================================
# DASHBOARD
# =========================================
    def show_dashboard(self):
        self.clear_main_content()

        self.statistics = statistics()

        center_frame = tk.Frame(self.main_content, bg="#F4F6FA")
        center_frame.place(relx=0.5, rely=0.4, anchor="center")
        label = tk.Label(center_frame, text="SISTEMA DE GESTÃO DE ALUGUER DE CARROS", font=("Arial", 22), bg="#F4F6FA", fg="#2c3e50")
        label.pack(pady=40)
        cards_frame = tk.Frame(center_frame, bg="#F4F6FA")
        cards_frame.pack(padx=20, pady=10, fill="x")       
        
        # DADOS ESTÁTICOS {"total_cars": stat[0], "available_cars": stat[1], "total_customers": stat[2], "active_rentals": stat[3], "total_revenue": stat[4], "unpaid_invoices": stat[5]}
        cards = [("🚗", self.statistics["total_cars"] if self.statistics else 0, "Total Carros"),
                ("📄", self.statistics["available_cars"] if self.statistics else 0, "Carros Disponíveis"),
                ("👤", self.statistics["total_customers"] if self.statistics else 0, "Clientes"),
                ("📅", self.statistics["active_rentals"] if self.statistics else 0, "Alugueres Ativos"),
                ("💰", self.statistics["total_revenue"] if self.statistics else 0, "Receita Mensal"),
                ("📄", self.statistics["unpaid_invoices"] if self.statistics else 0, "Faturas Não Pagas")]
       
        for i, (icon, big_text, small_text) in enumerate(cards):
            card = tk.Frame(cards_frame, bg="#F4F6FA", width=200, height=180, bd=0, highlightthickness=0)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="n")
            lbl_icon = tk.Label(card, text=icon, font=("Arial", 34), bg="#F4F6FA")
            lbl_icon.pack(pady=(25, 10))
            lbl_big = tk.Label(card, text=big_text, font=("Arial", 20, "bold"), bg="#F4F6FA", fg="#2c3e50")
            lbl_big.pack()
            lbl_small = tk.Label(card, text=small_text, font=("Arial", 10), bg="#F4F6FA", fg="#7f8c8d")
            lbl_small.pack(pady=(5, 0))

# =========================================
# CLIENTES
# =========================================
    def show_customers(self):
        self.clear_main_content()

        # NAVBAR LATERAL
        sidebar = tk.Frame(self.main_content, bg="#34495e", width=220)
        sidebar.pack(side="left", fill="y")

        # ÁREA DE CONTEÚDO
        self.customers_content = tk.Frame(self.main_content, bg="#F4F6FA")
        self.customers_content.pack(side="right", fill="both", expand=True)

        # TÍTULO SIDEBAR
        lbl_customers = tk.Label(sidebar, text="Clientes", bg="#34495e", fg="white", font=("Arial", 16, "bold"))
        lbl_customers.pack(pady=20)

        # BOTÕES SIDEBAR
        btn_insert = tk.Button(sidebar, text="Inserir", width=20, bg="#34495e", fg="white", relief="groove", command=self.show_insert_customer)
        btn_insert.pack(pady=5)
        btn_update = tk.Button(sidebar, text="Atualizar", width=20, bg="#34495e", fg="white", relief="groove", command=self.show_update_customer)
        btn_update.pack(pady=5)
        btn_delete = tk.Button(sidebar, text="Apagar", width=20, bg="#34495e", fg="white", relief="groove")
        btn_delete.pack(pady=5)
        btn_list = tk.Button(sidebar, text="Listar", width=20, bg="#34495e", fg="white", relief="groove")
        btn_list.pack(pady=5)
       
        self.show_insert_customer() # Mostrar a janela de inserção por padrão

    # LIMPAR ÁREA
    def clear_customers_content(self):
        for widget in self.customers_content.winfo_children():
            widget.destroy()

    # INSERIR CLIENTE
    def show_insert_customer(self):
        self.clear_customers_content()

        titulo = tk.Label(self.customers_content, text="Inserir Cliente", font=("Arial", 20, "bold"), bg="#F4F6FA")
        titulo.pack(pady=20)

        form = tk.Frame(self.customers_content, bg="#F4F6FA")
        form.pack(pady=20)

        tk.Label(form, text="Nome:", bg="#F4F6FA", font=("Arial", 12)).grid(row=0, column=0, pady=10, sticky="w")
        entry_nome = tk.Entry(form, width=35)
        entry_nome.grid(row=0, column=1, pady=10)
        tk.Label(form, text="NIF:", bg="#F4F6FA", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="w")
        entry_nif = tk.Entry(form, width=35)
        entry_nif.grid(row=1, column=1, pady=10)
        tk.Label(form, text="Nº Doc. Identificação:", bg="#F4F6FA", font=("Arial", 12)).grid(row=2, column=0, pady=10, sticky="w")
        entry_idcard = tk.Entry(form, width=35)
        entry_idcard.grid(row=2, column=1, pady=10)
        tk.Label(form, text="Data de Nascimento:", bg="#F4F6FA", font=("Arial", 12)).grid(row=3, column=0, pady=10, sticky="w")
        entry_birthdate = tk.Entry(form, width=35)
        entry_birthdate.grid(row=3, column=1, pady=10)
        tk.Label(form, text="E-mail:", bg="#F4F6FA", font=("Arial", 12)).grid(row=4, column=0, pady=10, sticky="w")
        entry_email = tk.Entry(form, width=35)
        entry_email.grid(row=4, column=1, pady=10)
        tk.Label(form, text="Telefone:", bg="#F4F6FA", font=("Arial", 12)).grid(row=5, column=0, pady=10, sticky="w")
        entry_phone = tk.Entry(form, width=35)
        entry_phone.grid(row=5, column=1, pady=10)
        tk.Label(form, text="Morada:", bg="#F4F6FA", font=("Arial", 12)).grid(row=6, column=0, pady=10, sticky="w")
        entry_address = tk.Entry(form, width=35)
        entry_address.grid(row=6, column=1, pady=10)
        tk.Label(form, text="Carta de Condução:", bg="#F4F6FA", font=("Arial", 12)).grid(row=7, column=0, pady=10, sticky="w")
        entry_drivinglicense = tk.Entry(form, width=35)
        entry_drivinglicense.grid(row=7, column=1, pady=10)

        btn_save = tk.Button(self.customers_content, text="Salvar Cliente", bg="#2980b9", fg="white", width=20, 
                             command=lambda: self.handle_insert_customer(entry_nome.get(), entry_nif.get(), 
                                                                         entry_idcard.get(), entry_birthdate.get(), 
                                                                         entry_email.get(), entry_phone.get(), 
                                                                         entry_address.get(), entry_drivinglicense.get()))
        btn_save.pack(pady=20)

    # ATUALIZAR CLIENTE
    def show_update_customer(self):
        self.clear_customers_content()

        titulo = tk.Label(self.customers_content,text="Atualizar Cliente",font=("Arial", 20, "bold"),bg="#F4F6FA")
        titulo.pack(pady=20)

        form = tk.Frame(self.customers_content, bg="#F4F6FA")
        form.pack(pady=20)

        tk.Label(form, text="ID:", bg="#F4F6FA", font=("Arial", 12)).grid(row=0, column=0, pady=10, sticky="w")
        entry_id = tk.Entry(form, width=35)
        entry_id.grid(row=0, column=1, pady=10)
        tk.Label(form, text="Novo Nome:", bg="#F4F6FA", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="w")
        entry_nome = tk.Entry(form, width=35)
        entry_nome.grid(row=1, column=1, pady=10)
        tk.Label(form, text="Novo NIF:", bg="#F4F6FA", font=("Arial", 12)).grid(row=2, column=0, pady=10, sticky="w")
        entry_nif = tk.Entry(form, width=35)
        entry_nif.grid(row=2, column=1, pady=10)
        tk.Label(form, text="Novo Nº Doc. Identificação:", bg="#F4F6FA", font=("Arial", 12)).grid(row=3, column=0, pady=10, sticky="w")
        entry_idcard = tk.Entry(form, width=35)
        entry_idcard.grid(row=3, column=1, pady=10)
        tk.Label(form, text="Nova Data de Nascimento:", bg="#F4F6FA", font=("Arial", 12)).grid(row=4, column=0, pady=10, sticky="w")
        entry_birthdate = tk.Entry(form, width=35)
        entry_birthdate.grid(row=4, column=1, pady=10)
        tk.Label(form, text="Novo E-mail:", bg="#F4F6FA", font=("Arial", 12)).grid(row=5, column=0, pady=10, sticky="w")
        entry_email = tk.Entry(form, width=35)
        entry_email.grid(row=5, column=1, pady=10)
        tk.Label(form, text="Novo Telefone:", bg="#F4F6FA", font=("Arial", 12)).grid(row=6, column=0, pady=10, sticky="w")
        entry_phone = tk.Entry(form, width=35)
        entry_phone.grid(row=6, column=1, pady=10)
        tk.Label(form, text="Nova Morada:", bg="#F4F6FA", font=("Arial", 12)).grid(row=7, column=0, pady=10, sticky="w")
        entry_address = tk.Entry(form, width=35)
        entry_address.grid(row=7, column=1, pady=10)
        tk.Label(form, text="Nova Carta de Condução:", bg="#F4F6FA", font=("Arial", 12)).grid(row=8, column=0, pady=10, sticky="w")
        entry_drivinglicense = tk.Entry(form, width=35)
        entry_drivinglicense.grid(row=8, column=1, pady=10)

        btn_save = tk.Button(self.customers_content, text="Atualizar Cliente", bg="#2980b9", fg="white", width=20, 
                             command=lambda: self.handle_update_customer(entry_id.get(), entry_nome.get(), entry_nif.get(), 
                                                                         entry_idcard.get(), entry_birthdate.get(), 
                                                                         entry_email.get(), entry_phone.get(), 
                                                                         entry_address.get(), entry_drivinglicense.get()))
        btn_save.pack(pady=20)

    # ATUALIZAR CLIENTE
    def show_update_customer(self):
        self.clear_customers_content()

        titulo = tk.Label(self.customers_content,text="Atualizar Cliente",font=("Arial", 20, "bold"),bg="#F4F6FA")
        titulo.pack(pady=20)

        form = tk.Frame(self.customers_content, bg="#F4F6FA")
        form.pack(pady=20)

# =========================================
# FROTA
# =========================================
    def show_fleet(self):
        self.clear_main_content()

        # NAVBAR LATERAL
        sidebar = tk.Frame(self.main_content, bg="#34495e", width=220)
        sidebar.pack(side="left", fill="y")

        # ÁREA DE CONTEÚDO
        self.fleet_content = tk.Frame(self.main_content, bg="#F4F6FA")
        self.fleet_content.pack(side="right", fill="both", expand=True)

        # TÍTULO SIDEBAR
        lbl_fleet = tk.Label(sidebar, text="Frota", bg="#34495e", fg="white", font=("Arial", 16, "bold"))
        lbl_fleet.pack(pady=20)

        # BOTÕES SIDEBAR
        btn_insert = tk.Button(sidebar, text="Inserir", width=20, bg="#34495e", fg="white", relief="groove", command=self.show_insert_car)
        btn_insert.pack(pady=5)
        btn_update = tk.Button(sidebar, text="Atualizar", width=20, bg="#34495e", fg="white", relief="groove")
        btn_update.pack(pady=5)
        btn_delete = tk.Button(sidebar, text="Apagar", width=20, bg="#34495e", fg="white", relief="groove")
        btn_delete.pack(pady=5)
        btn_list = tk.Button(sidebar, text="Listar", width=20, bg="#34495e", fg="white", relief="groove")
        btn_list.pack(pady=5)
       
        self.show_insert_car()

    # LIMPAR ÁREA
    def clear_fleet_content(self):
        for widget in self.fleet_content.winfo_children():
            widget.destroy()

    # INSERIR CARRO
    def show_insert_car(self):
        self.clear_fleet_content()

        titulo = tk.Label(self.fleet_content, text="Inserir Carro", font=("Arial", 20, "bold"), bg="#F4F6FA")
        titulo.pack(pady=20)

        form = tk.Frame(self.fleet_content, bg="#F4F6FA")
        form.pack(pady=20)

        tk.Label(form, text="Marca:", bg="#F4F6FA", font=("Arial", 12)).grid(row=0, column=0, pady=10, sticky="w")
        entry_brand = tk.Entry(form, width=35)
        entry_brand.grid(row=0, column=1, pady=10)
        tk.Label(form, text="Modelo:", bg="#F4F6FA", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="w")
        entry_model = tk.Entry(form, width=35)
        entry_model.grid(row=1, column=1, pady=10)
        tk.Label(form, text="Ano:", bg="#F4F6FA", font=("Arial", 12)).grid(row=2, column=0, pady=10, sticky="w")
        entry_year = tk.Entry(form, width=35)
        entry_year.grid(row=2, column=1, pady=10)
        tk.Label(form, text="Matrícula:", bg="#F4F6FA", font=("Arial", 12)).grid(row=3, column=0, pady=10, sticky="w")
        entry_plate = tk.Entry(form, width=35)
        entry_plate.grid(row=3, column=1, pady=10)
        tk.Label(form, text="Categoria:", bg="#F4F6FA", font=("Arial", 12)).grid(row=4, column=0, pady=10, sticky="w")
        category_var = tk.StringVar()
        combo_category = ttk.Combobox(form, textvariable=category_var, values=["económico", "compacto", "tamanho médio", "suv", "luxo"], state="readonly", width=33)
        combo_category.grid(row=4, column=1, pady=10)
        tk.Label(form, text="Tipo de Combustível:", bg="#F4F6FA", font=("Arial", 12)).grid(row=5, column=0, pady=10, sticky="w")
        fuel_type_var = tk.StringVar()
        combo_fuel_type = ttk.Combobox(form, textvariable=fuel_type_var, values=["gasolina", "diesel", "elétrico", "híbrido"], state="readonly", width=33)
        combo_fuel_type.grid(row=5, column=1, pady=10)
        tk.Label(form, text="Seguro:", bg="#F4F6FA", font=("Arial", 12)).grid(row=6, column=0, pady=10, sticky="w")
        entry_insurance = tk.Entry(form, width=35)
        entry_insurance.grid(row=6, column=1, pady=10)
        tk.Label(form, text="Preço Diário:", bg="#F4F6FA", font=("Arial", 12)).grid(row=7, column=0, pady=10, sticky="w")
        entry_daily_rate = tk.Entry(form, width=35)
        entry_daily_rate.grid(row=7, column=1, pady=10)
        
        btn_save = tk.Button(self.fleet_content, text="Salvar Carro", bg="#2980b9", fg="white", width=20, 
                             command=lambda: self.handle_insert_car(entry_brand.get(), entry_model.get(), entry_year.get(), 
                                                                    entry_plate.get(), combo_category.get(), combo_fuel_type.get(), 
                                                                   entry_insurance.get(), entry_daily_rate.get()))
        btn_save.pack(pady=20)


# =========================================
# ALUGUER
# =========================================
    def show_rentals(self):
        pass

# =========================================
# FATURAS
# =========================================
    def show_invoices(self):
        pass

# =========================================
# UTILIZADORES
# =========================================
    def show_users(self):
        self.clear_main_content()

        # NAVBAR LATERAL
        sidebar = tk.Frame(self.main_content, bg="#34495e", width=220)
        sidebar.pack(side="left", fill="y")

        # ÁREA DE CONTEÚDO
        self.users_content = tk.Frame(self.main_content, bg="#F4F6FA")
        self.users_content.pack(side="right", fill="both", expand=True)

        # TÍTULO SIDEBAR
        lbl_users = tk.Label(sidebar, text="Utilizadores", bg="#34495e", fg="white", font=("Arial", 16, "bold"))
        lbl_users.pack(pady=20)

        # BOTÕES SIDEBAR
        btn_insert = tk.Button(sidebar, text="Inserir", bg="#34495e", fg="white", relief="groove", width=20, command=self.show_insert_user)
        btn_insert.pack(pady=5)
        btn_update = tk.Button(sidebar, text="Atualizar", bg="#34495e", fg="white", relief="groove", width=20, command=self.show_update_user)
        btn_update.pack(pady=5)
        btn_delete = tk.Button(sidebar, text="Apagar", bg="#34495e", fg="white", relief="groove", width=20)
        btn_delete.pack(pady=5)
        btn_list = tk.Button(sidebar, text="Listar", bg="#34495e", fg="white", relief="groove", width=20)
        btn_list.pack(pady=5)
       
        self.show_insert_user() # Mostrar a janela de inserção por padrão

    # LIMPAR ÁREA
    def clear_users_content(self):
        for widget in self.users_content.winfo_children():
            widget.destroy()

    # INSERIR UTILIZADOR
    def show_insert_user(self):
        self.clear_users_content()

        titulo = tk.Label(self.users_content, text="Inserir Utilizador", font=("Arial", 20, "bold"), bg="#F4F6FA")
        titulo.pack(pady=20)

        form = tk.Frame(self.users_content, bg="#F4F6FA")
        form.pack(pady=20)

        tk.Label(form, text="Nome:", bg="#F4F6FA", font=("Arial", 12)).grid(row=0, column=0, pady=10, sticky="w")
        entry_nome = tk.Entry(form, width=35)
        entry_nome.grid(row=0, column=1, pady=10)
        tk.Label(form,text="Login:",bg="#F4F6FA",font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="w")
        entry_login = tk.Entry(form, width=35)
        entry_login.grid(row=1, column=1, pady=10)
        tk.Label(form, text="Role:", bg="#F4F6FA", font=("Arial", 12)).grid(row=2, column=0, pady=10, sticky="w")
        role_var = tk.StringVar(value="normal")
        option_role = tk.OptionMenu(form, role_var, "administrador", "normal")
        option_role.config(width=30)
        option_role.grid(row=2, column=1, pady=10)
        btn_save = tk.Button(self.users_content, text="Salvar Utilizador", bg="#2980b9", fg="white", width=20, 
                             command=lambda: self.handle_insert_user(entry_nome.get(), entry_login.get(), role_var.get()))
        btn_save.pack(pady=20)

    # ATUALIZAR UTILIZADOR
    def show_update_user(self):
        self.clear_users_content()

        titulo = tk.Label(self.users_content,text="Atualizar Utilizador",font=("Arial", 20, "bold"),bg="#F4F6FA")
        titulo.pack(pady=20)

        form = tk.Frame(self.users_content, bg="white")
        form.pack(pady=20)

        tk.Label(form, text="ID:", bg="white", font=("Arial", 12)).grid(row=0, column=0, pady=10, sticky="w")
        entry_id = tk.Entry(form, width=35)
        entry_id.grid(row=0, column=1, pady=10)
        tk.Label(form, text="Novo Nome:", bg="white", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="w")
        entry_nome = tk.Entry(form, width=35)
        entry_nome.grid(row=1, column=1, pady=10)
        tk.Label(form, text="Novo Login:", bg="white", font=("Arial", 12)).grid(row=2, column=0, pady=10, sticky="w")
        entry_login = tk.Entry(form, width=35)
        entry_login.grid(row=2, column=1, pady=10)
        tk.Label(form, text="Novo Role:", bg="white", font=("Arial", 12)).grid(row=3, column=0, pady=10, sticky="w")
        role_var = tk.StringVar(value="normal")
        option_role = tk.OptionMenu(form, role_var, "administrador", "normal")
        option_role.config(width=30)
        option_role.grid(row=3, column=1, pady=10)
        
        btn_update = tk.Button(self.users_content, text="Atualizar Utilizador", bg="#2980b9", fg="white", width=20)
        btn_update.pack(pady=20)


    def logout(self):
        if messagebox.askyesno("Terminar Sessão", "Deseja sair da aplicação?"):
            self.destroy()

if __name__ == "__main__":
    MainWindow()