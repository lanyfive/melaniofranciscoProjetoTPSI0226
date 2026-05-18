import tkinter as tk
from tkinter import ttk, messagebox
from database import init_db, get_connection, statistics
from login import LoginWindow
from service import CustomerService, CarService, RentalService, InvoiceService, UserService

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
        self.user_service = UserService()
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
    
    def handle_update_customer(self, customer_id, name):
        try:
            self.customer_service.update_customer(customer_id, name)
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso.")
            self.show_customers()
        except ValueError as e:
            messagebox.showerror("Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def handle_delete_customer(self, customer_id):
        try:
            self.customer_service.delete_customer(customer_id)
            messagebox.showinfo("Sucesso", "Cliente apagado com sucesso.")
            self.show_customers()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def handle_get_all_customers(self):
        
        for item in self.customers_table.get_children():
            self.customers_table.delete(item)
    
        search = self.search_var.get().strip().lower()
        customers = self.customer_service.get_all_customers()
        
        if search:
            customers = [
                customer for customer in customers
                if search in customer["name"].lower()
                or search in customer["nif"].lower()
            ]

        for customer in customers:
            self.customers_table.insert(
            "",
            "end",
            values=(
                customer["id"],
                customer["name"],
                customer["nif"]
            )
        )

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

    def handle_get_all_cars(self):
        
        for item in self.cars_table.get_children():
            self.cars_table.delete(item)
    
        search = self.search_var.get().strip().lower()
        cars = self.car_service.get_all_cars()
        
        if search:
            cars = [
                car for car in cars
                if search in car["brand"].lower()
                or search in car["model"].lower()
                or search in car["plate"].lower()
            ]

        for car in cars:
            self.cars_table.insert(
            "",
            "end",
            values=(
                car["id"],
                car["brand"],
                car["model"],
                car["year"],
                car["plate"]
            )
        )

# =========================================
# HANDLERS - RENTALS
# =========================================
    def handle_insert_rental(self, car_id, customer_id, start_date, end_date, total_cost):
        try:
            self.rental_service.create_rental(car_id, customer_id, start_date, end_date, total_cost)
            messagebox.showinfo("Sucesso", "Aluguer criado com sucesso.")
            self.show_rentals()
        except ValueError as e:
            messagebox.showerror("Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def handle_get_all_rentals(self):
        
        for item in self.rentals_table.get_children():
            self.rentals_table.delete(item)
    
        search = self.search_var.get().strip().lower()
        
        rentals = self.rental_service.get_all_rentals()

        if search:
            rentals = [
                rental for rental in rentals
                if (
                    search in rental["car"].lower()
                    or search in rental["customer"].lower()
                )
            ]

        for rental in rentals:
            self.rentals_table.insert(
                "",
                "end",
                values=(
                    rental["id"],
                    rental["car"],
                    rental["customer"],
                    rental["start_date"],
                    rental["end_date"],
                    rental["total_cost"]
                )
            )

# =========================================
# HANDLERS - INVOICES
# =========================================
    def handle_update_invoice(self):
        selected = self.invoices_table.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma fatura")
            return

        values = self.invoices_table.item(selected[0])["values"]
        invoice_id = values[0]

        confirm = messagebox.askyesno("Confirmar", "Deseja pagar a fatura?")
        if not confirm:
            return

        try:
            self.invoice_service.pay_invoice(invoice_id)
            messagebox.showinfo("Sucesso", "Fatura paga com sucesso.")
            self.show_invoices()
        except ValueError as e:
            messagebox.showerror("Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def handle_get_all_invoices(self):
        
        for item in self.invoices_table.get_children():
            self.invoices_table.delete(item)
    
        search = self.search_var.get().strip().lower()
        invoices = self.invoice_service.get_all_invoices()
        
        if search:
            invoices = [
                invoice for invoice in invoices
                if search in str(invoice["rental_id"])
            ]

        for invoice in invoices:
            self.invoices_table.insert(
                "",
                "end",
                values=(
                    invoice["id"],
                    invoice["rental_id"],
                    invoice["issue_date"],
                    invoice["amount"],
                    invoice["tax"],
                    invoice["total"],
                    invoice["status"]
                )
            )


# =========================================
# HANDLERS - USERS
# =========================================
    def handle_insert_user(self, nome, login, password, role):
        try:
            self.user_service.create_user(nome, login, password, role)
            messagebox.showinfo("Sucesso", "Utilizador criado com sucesso.")
            self.show_users()
        except ValueError as e:
            messagebox.showerror("Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def handle_get_all_users(self):
        for item in self.users_table.get_children():
            self.users_table.delete(item)
    
        search = self.search_var.get().strip().lower()
        users = self.user_service.get_all_users()
        
        if search:
            users = [
                user for user in users
                if search in user["name"].lower()
                or search in user["login"].lower()
                or search in user["role"].lower()
            ]

        for user in users:
            self.users_table.insert(
            "",
            "end",
            values=(
                user["id"],
                user["name"],
                user["login"],
                user["role"]
            )
        )


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

        self.top_frame = tk.Frame(self.main_content, bg="#F4F6FA", height=50)
        self.top_frame.pack(fill="x", padx=20)

        self.customers_content = tk.Frame(self.main_content, bg="#F4F6FA", width=780)
        self.customers_content.pack(side="right", fill="both", expand=True)

        title = tk.Label(self.top_frame, text="Clientes", font=("Arial", 22, "bold"), bg="#F4F6FA")
        title.pack(pady=10)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self.top_frame, textvariable=self.search_var, font=("Arial", 11))
        search_entry.pack(side="left", padx=(0, 10), ipady=5)
        btn_search = tk.Button(self.top_frame, text="Filtrar", bg="#2980b9", command=self.handle_get_all_customers, fg="white", padx=15)
        btn_search.pack(side="left")
        btn_delete = tk.Button(self.top_frame, text="Apagar", bg="#c0392b", command=self.show_delete_customer, fg="white")
        btn_delete.pack(side="right", padx=5)
        btn_update = tk.Button(self.top_frame, text="Atualizar", bg="#2980b9", command=self.show_update_customer, fg="white")
        btn_update.pack(side="right", padx=5)
        btn_insert = tk.Button(self.top_frame, text="Inserir", bg="#2980b9", command=self.show_insert_customer, fg="white")
        btn_insert.pack(side="right", padx=5)    

        table_frame = tk.Frame(self.customers_content, bg="#F4F6FA")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        columns = ("id", "name", "nif")

        self.customers_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.customers_table.heading("id", text="ID")
        self.customers_table.heading("name", text="Nome")
        self.customers_table.heading("nif", text="NIF")
        self.customers_table.column("id", width=5)
        self.customers_table.column("name", width=80)
        self.customers_table.column("nif", width=10)
        self.customers_table.pack(fill="both", expand=False)

        self.handle_get_all_customers()

    def show_insert_customer(self):
        win = tk.Toplevel(self)

        win.title("Inserir Cliente")
        win.geometry("400x750")
        win.configure(bg="#F4F6FA")

        tk.Label(win, text="Nome", bg="#F4F6FA", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(20, 5))
        ent_name = tk.Entry(win, font=("Arial", 11))
        ent_name.pack(fill="x", padx=30, ipady=5)
        tk.Label(win, text="NIF", bg="#F4F6FA", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(15, 5))
        ent_nif = tk.Entry(win, font=("Arial", 11))
        ent_nif.pack(fill="x", padx=30, ipady=5)
        tk.Label(win, text="Nº Doc. Identificação:", bg="#F4F6FA", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(15, 5))
        entry_idcard = tk.Entry(win, font=("Arial", 11))
        entry_idcard.pack(fill="x", padx=30, ipady=5)
        tk.Label(win, text="Data de Nascimento:", bg="#F4F6FA", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(15, 5))
        entry_birthdate = tk.Entry(win, font=("Arial", 11))
        entry_birthdate.pack(fill="x", padx=30, ipady=5)
        tk.Label(win, text="E-mail:", bg="#F4F6FA", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(15, 5))
        entry_email = tk.Entry(win, font=("Arial", 11))
        entry_email.pack(fill="x", padx=30, ipady=5)
        tk.Label(win, text="Telefone:", bg="#F4F6FA", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(15, 5))
        entry_phone = tk.Entry(win, font=("Arial", 11))
        entry_phone.pack(fill="x", padx=30, ipady=5)
        tk.Label(win, text="Morada:", bg="#F4F6FA", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(15, 5))
        entry_address = tk.Entry(win, font=("Arial", 11))
        entry_address.pack(fill="x", padx=30, ipady=5)
        tk.Label(win, text="Carta de Condução:", bg="#F4F6FA", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(15, 5))
        entry_drivinglicense = tk.Entry(win, font=("Arial", 11))
        entry_drivinglicense.pack(fill="x", padx=30, ipady=5)

        def save_customer():
            name = ent_name.get()
            nif = ent_nif.get()
            idcard = entry_idcard.get()
            birthdate = entry_birthdate.get()
            email = entry_email.get()
            phone = entry_phone.get()
            address = entry_address.get()
            drivinglicense = entry_drivinglicense.get()           

            if not name or not nif:
                messagebox.showwarning("Aviso", "Preencha todos os campos")
                return

            self.handle_insert_customer(name, nif, idcard, birthdate, email, phone, address, drivinglicense)
            win.destroy()

        tk.Button(win, text="Salvar", bg="#27ae60", fg="white", command=save_customer).pack(pady=25)

    def show_update_customer(self):
        selected = self.customers_table.selection()

        if not selected:
            messagebox.showwarning("Aviso", "Selecione um cliente")
            return
        
        values = self.customers_table.item(selected[0])["values"]
        customer_id = values[0]
        customer_name = values[1]

        win = tk.Toplevel(self)

        win.title("Atualizar Cliente")
        win.geometry("400x250")
        win.configure(bg="#F4F6FA")

        tk.Label(win, text="Nome", bg="#F4F6FA", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(20, 5))

        ent_name = tk.Entry(win, font=("Arial", 11))
        ent_name.insert(0, customer_name)
        ent_name.pack(fill="x", padx=30, ipady=5)

        def save_update():
            name = ent_name.get()
            self.customer_service.update_customer(customer_id, name)
            win.destroy()

        tk.Button(win, text="Atualizar",bg="#2980b9", fg="white", command=save_update).pack(pady=25)

    def show_delete_customer(self):

        selected = self.customers_table.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um cliente")
            return

        values = self.customers_table.item(selected[0])["values"]
        customer_id = values[0]

        confirm = messagebox.askyesno("Confirmar", "Deseja apagar o cliente?")
        if not confirm:
            return

        self.handle_delete_customer(customer_id)


# =========================================
# FROTA
# =========================================
    def show_fleet(self):
        self.clear_main_content()

        # NAVBAR LATERAL
        sidebar = tk.Frame(self.main_content, bg="#34495e", width=220)
        sidebar.pack(side="left", fill="y")

        self.top_frame = tk.Frame(self.main_content, bg="#F4F6FA", height=50)
        self.top_frame.pack(fill="x", padx=20)

        self.fleet_content = tk.Frame(self.main_content, bg="#F4F6FA", width=780)
        self.fleet_content.pack(side="right", fill="both", expand=True)

        title = tk.Label(self.top_frame, text="Frota", font=("Arial", 22, "bold"), bg="#F4F6FA")
        title.pack(pady=10)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self.top_frame, textvariable=self.search_var, font=("Arial", 11))
        search_entry.pack(side="left", padx=(0, 10), ipady=5)
        btn_search = tk.Button(self.top_frame, text="Filtrar", bg="#2980b9", command=self.handle_get_all_cars, fg="white", padx=15)
        btn_search.pack(side="left")
        btn_delete = tk.Button(self.top_frame, text="Apagar", bg="#c0392b", fg="white")
        btn_delete.pack(side="right", padx=5)
        btn_update = tk.Button(self.top_frame, text="Atualizar", bg="#2980b9", fg="white")
        btn_update.pack(side="right", padx=5)
        btn_insert = tk.Button(self.top_frame, text="Inserir", bg="#2980b9", fg="white")
        btn_insert.pack(side="right", padx=5)    

        table_frame = tk.Frame(self.fleet_content, bg="#F4F6FA")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        columns = ("id", "brand", "model", "year", "plate")

        self.cars_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.cars_table.heading("id", text="ID")
        self.cars_table.heading("brand", text="Marca")
        self.cars_table.heading("model", text="Modelo")
        self.cars_table.heading("year", text="Ano")
        self.cars_table.heading("plate", text="Matrícula")
        self.cars_table.column("id", width=5)
        self.cars_table.column("brand", width=80)
        self.cars_table.column("model", width=10)
        self.cars_table.column("year", width=10)
        self.cars_table.column("plate", width=10)
        self.cars_table.pack(fill="both", expand=False)

        self.handle_get_all_cars()


# =========================================
# ALUGUER
# =========================================
    def show_rentals(self):
        self.clear_main_content()

        # NAVBAR LATERAL
        sidebar = tk.Frame(self.main_content, bg="#34495e", width=220)
        sidebar.pack(side="left", fill="y")

        self.top_frame = tk.Frame(self.main_content, bg="#F4F6FA", height=50)
        self.top_frame.pack(fill="x", padx=20)

        self.rentals_content = tk.Frame(self.main_content, bg="#F4F6FA", width=780)
        self.rentals_content.pack(side="right", fill="both", expand=True)

        title = tk.Label(self.top_frame, text="Aluguer", font=("Arial", 22, "bold"), bg="#F4F6FA")
        title.pack(pady=10)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self.top_frame, textvariable=self.search_var, font=("Arial", 11))
        search_entry.pack(side="left", padx=(0, 10), ipady=5)
        btn_search = tk.Button(self.top_frame, text="Filtrar", bg="#2980b9", command=self.handle_get_all_rentals, fg="white", padx=15)
        btn_search.pack(side="left")
        btn_update = tk.Button(self.top_frame, text="Atualizar", bg="#2980b9", fg="white")
        btn_update.pack(side="right", padx=5)
        btn_insert = tk.Button(self.top_frame, text="Inserir", bg="#2980b9", command=self.show_insert_rental, fg="white")
        btn_insert.pack(side="right", padx=5)    

        table_frame = tk.Frame(self.rentals_content, bg="#F4F6FA")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        columns = ("id", "car", "customer", "start_date", "end_date", "total_cost")

        self.rentals_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.rentals_table.heading("id", text="ID")
        self.rentals_table.heading("car", text="Carro")
        self.rentals_table.heading("customer", text="Cliente")
        self.rentals_table.heading("start_date", text="Data de Início")
        self.rentals_table.heading("end_date", text="Data de Fim")
        self.rentals_table.heading("total_cost", text="Custo Total")
        self.rentals_table.column("id", width=5)
        self.rentals_table.column("car", width=80)
        self.rentals_table.column("customer", width=10)
        self.rentals_table.column("start_date", width=10)
        self.rentals_table.column("end_date", width=10)
        self.rentals_table.column("total_cost", width=10)
        self.rentals_table.pack(fill="both", expand=False)

        self.handle_get_all_rentals()

    def show_insert_rental(self):
        win = tk.Toplevel(self)

        win.title("Alugar Carro")
        win.geometry("400x500")
        win.configure(bg="#F4F6FA")

        cars = self.car_service.get_all_cars()
        customers = self.customer_service.get_all_customers()

        car_map = {}
        for car in cars:
            label = f"{car['brand']} {car['model']} ({car['plate']})"
            car_map[label] = car["id"]

        customer_map = {}
        for customer in customers:
            label = f"{customer['name']} ({customer['nif']})"
            customer_map[label] = customer["id"]

        tk.Label(win, text="Carro", bg="#F4F6FA", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(20, 5))
        role_car = tk.StringVar()
        combo_car = ttk.Combobox(win, textvariable=role_car, values=list(car_map.keys()), state="readonly", width=33)
        combo_car.pack(fill="x", padx=30, ipady=5)
        tk.Label(win, text="Cliente", bg="#F4F6FA", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(20, 5))
        role_customer = tk.StringVar()
        combo_customer = ttk.Combobox(win, textvariable=role_customer, values=list(customer_map.keys()), state="readonly", width=33)
        combo_customer.pack(fill="x", padx=30, ipady=5)
        tk.Label(win, text="Data de Início:", bg="#F4F6FA", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(20, 5))
        ent_start_date = tk.Entry(win, font=("Arial", 11))
        ent_start_date.pack(fill="x", padx=30, ipady=5)      
        tk.Label(win, text="Data de Fim:", bg="#F4F6FA", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(15, 5))
        ent_end_date = tk.Entry(win, font=("Arial", 11))
        ent_end_date.pack(fill="x", padx=30, ipady=5)
        tk.Label(win, text="Custo Total:", bg="#F4F6FA", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(15, 5))
        ent_total_cost = tk.Entry(win, font=("Arial", 11))
        ent_total_cost.pack(fill="x", padx=30, ipady=5)

        def save_rental():
            car_label = combo_car.get()
            customer_label = combo_customer.get()
            start_date = ent_start_date.get().strip()
            end_date = ent_end_date.get().strip()
            total_cost = ent_total_cost.get().strip()

            if not car_label or not customer_label or not start_date or not end_date or not total_cost:
                messagebox.showwarning("Aviso", "Preencha todos os campos")
                return

            car_id = car_map[car_label]
            customer_id = customer_map[customer_label]
            self.handle_insert_rental(car_id, customer_id, start_date, end_date, float(total_cost))
            win.destroy()

        tk.Button(win, text="Salvar", bg="#27ae60", fg="white", command=save_rental).pack(pady=25)

# =========================================
# FATURAS
# =========================================
    def show_invoices(self):
        self.clear_main_content()

        # NAVBAR LATERAL
        sidebar = tk.Frame(self.main_content, bg="#34495e", width=220)
        sidebar.pack(side="left", fill="y")

        self.top_frame = tk.Frame(self.main_content, bg="#F4F6FA", height=50)
        self.top_frame.pack(fill="x", padx=20)

        self.invoices_content = tk.Frame(self.main_content, bg="#F4F6FA", width=780)
        self.invoices_content.pack(side="right", fill="both", expand=True)

        title = tk.Label(self.top_frame, text="Faturas", font=("Arial", 22, "bold"), bg="#F4F6FA")
        title.pack(pady=10)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self.top_frame, textvariable=self.search_var, font=("Arial", 11))
        search_entry.pack(side="left", padx=(0, 10), ipady=5)
        btn_search = tk.Button(self.top_frame, text="Filtrar", bg="#2980b9", command=self.handle_get_all_invoices, fg="white", padx=15)
        btn_search.pack(side="left")
        btn_update = tk.Button(self.top_frame, text="Exportar", bg="#2980b9", fg="white")
        btn_update.pack(side="right", padx=5)
        btn_insert = tk.Button(self.top_frame, text="Pagar Fatura", bg="#2980b9", command=self.show_invoice_payment, fg="white")
        btn_insert.pack(side="right", padx=5)

        table_frame = tk.Frame(self.invoices_content, bg="#F4F6FA")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        columns = ("id", "rental_id", "issue_date", "amount", "tax", "total", "status")

        self.invoices_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.invoices_table.heading("id", text="ID")
        self.invoices_table.heading("rental_id", text="Aluguel")
        self.invoices_table.heading("issue_date", text="Data de Emissão")
        self.invoices_table.heading("amount", text="Valor")
        self.invoices_table.heading("tax", text="Imposto")
        self.invoices_table.heading("total", text="Total")
        self.invoices_table.heading("status", text="Estado")
        self.invoices_table.column("id", width=5)
        self.invoices_table.column("rental_id", width=80)
        self.invoices_table.column("issue_date", width=10)
        self.invoices_table.column("amount", width=10)
        self.invoices_table.column("tax", width=10)
        self.invoices_table.column("total", width=10)
        self.invoices_table.column("status", width=10)
        self.invoices_table.pack(fill="both", expand=False)

        self.handle_get_all_invoices()

    def show_invoice_payment(self):
        selected = self.invoices_table.selection()

        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma fatura")
            return
       
        values = self.invoices_table.item(selected[0])["values"]
        invoice_id = values[0]
        current_status = values[6]
       
        if current_status == "pago":
            messagebox.showinfo("Informação", "A fatura já está paga")
            return
       
        confirm = messagebox.askyesno("Confirmar", "Deseja pagar esta fatura?")

        if not confirm:
            return
        
        try:
            self.invoice_service.pay_invoice(invoice_id)
            messagebox.showinfo("Sucesso", "Fatura paga com sucesso")
            self.handle_get_all_invoices()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

# =========================================
# UTILIZADORES
# =========================================
    def show_users(self):
        self.clear_main_content()

        # NAVBAR LATERAL
        sidebar = tk.Frame(self.main_content, bg="#34495e", width=220)
        sidebar.pack(side="left", fill="y")

        self.top_frame = tk.Frame(self.main_content, bg="#F4F6FA", height=50)
        self.top_frame.pack(fill="x", padx=20)

        self.users_content = tk.Frame(self.main_content, bg="#F4F6FA", width=780)
        self.users_content.pack(side="right", fill="both", expand=True)

        title = tk.Label(self.top_frame, text="Utilizadores", font=("Arial", 22, "bold"), bg="#F4F6FA")
        title.pack(pady=10)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self.top_frame, textvariable=self.search_var, font=("Arial", 11))
        search_entry.pack(side="left", padx=(0, 10), ipady=5)
        btn_search = tk.Button(self.top_frame, text="Filtrar", bg="#2980b9", command=self.handle_get_all_users, fg="white", padx=15)
        btn_search.pack(side="left")
        btn_delete = tk.Button(self.top_frame, text="Apagar", bg="#c0392b", fg="white")
        btn_delete.pack(side="right", padx=5)
        btn_update = tk.Button(self.top_frame, text="Atualizar", bg="#2980b9", fg="white")
        btn_update.pack(side="right", padx=5)
        btn_insert = tk.Button(self.top_frame, text="Inserir", bg="#2980b9", command=self.show_insert_user, fg="white")
        btn_insert.pack(side="right", padx=5)    

        table_frame = tk.Frame(self.users_content, bg="#F4F6FA")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        columns = ("id", "name", "login", "role")

        self.users_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.users_table.heading("id", text="ID")
        self.users_table.heading("name", text="Nome")
        self.users_table.heading("login", text="Login")
        self.users_table.heading("role", text="Role")
        self.users_table.column("id", width=5)
        self.users_table.column("name", width=80)
        self.users_table.column("login", width=80)
        self.users_table.column("role", width=80)
        self.users_table.pack(fill="both", expand=False)

        self.handle_get_all_users()

    def show_insert_user(self):
        win = tk.Toplevel(self)

        win.title("Inserir Utilizador")
        win.geometry("400x500")
        win.configure(bg="#F4F6FA")

        tk.Label(win, text="Nome", bg="#F4F6FA", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(20, 5))
        ent_name = tk.Entry(win, font=("Arial", 11))
        ent_name.pack(fill="x", padx=30, ipady=5)
        tk.Label(win, text="Login", bg="#F4F6FA", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(15, 5))
        ent_login = tk.Entry(win, font=("Arial", 11))
        ent_login.pack(fill="x", padx=30, ipady=5)
        tk.Label(win, text="Senha", bg="#F4F6FA", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(15, 5))
        entry_password = tk.Entry(win, font=("Arial", 11), show="*")
        entry_password.pack(fill="x", padx=30, ipady=5)
        tk.Label(win, text="Role:", bg="#F4F6FA", font=("Arial", 12)).pack(anchor="w", padx=30, pady=(15, 5))
        role_var = tk.StringVar()
        combo_role = ttk.Combobox(win, textvariable=role_var, values=["admin", "normal"], state="readonly", width=33)
        combo_role.pack(fill="x", padx=30, ipady=5)

        def save_user():
            name = ent_name.get()
            login = ent_login.get()
            password = entry_password.get()
            role = combo_role.get()

            if not name or not login or not password or not role:
                messagebox.showwarning("Aviso", "Preencha todos os campos")
                return

            self.handle_insert_user(name, login, password, role)
            win.destroy()

        tk.Button(win, text="Salvar", bg="#27ae60", fg="white", command=save_user).pack(pady=25)


    def logout(self):
        if messagebox.askyesno("Terminar Sessão", "Deseja sair da aplicação?"):
            self.destroy()

if __name__ == "__main__":
    MainWindow()
