# melaniofranciscoProjetoTPSI0226
# AutoMSF - Sistema de Gestão de Aluguer de Carros

Aplicação desktop desenvolvido em Python para gestão de aluguer de carros, clientes, utilizadores e faturação automática.

---

# Funcionalidades

## Perfil Administrador

O utilizador com perfil de administrador pode:

- Efetuar login na aplicação
- Gerir utilizadores
  - Inserir
  - Atualizar
  - Apagar
  - Listar
- Gerir carros
  - Inserir
  - Atualizar
  - Apagar
  - Listar

---

## Perfil Normal

O utilizador com perfil normal pode:

- Efetuar login na aplicação
- Gerir clientes
- Registar alugueres
- Registar devoluções
- Registar pagamentos de faturas

---

# Faturação Automática

Após o registo de um aluguer, o sistema gera automaticamente a respetiva fatura.

---

# Tecnologias Utilizadas

- Python 3
- Tkinter
- SQLite
- ttk

---

# Estrutura do Projeto

```text
project/
│
├── main.py
├── database.py
├── login.py
├── services/
├── models/
├── views/
├── rentacar.db
└── README.md
```

---

# Requisitos

Antes de executar o sistema, instalar:

- Python 3.10+
- pip

---

# Instalação Local

## 1. Clonar o projeto

```bash
git clone https://github.com/lanyfive/melaniofranciscoProjetoTPSI0226.git
```

---

## 2. Entrar na pasta do projeto

```bash
cd project
```

---

# Executar Aplicação

```bash
python main.py
```

---

# Base de Dados

O sistema utiliza SQLite.

O ficheiro da base de dados será criado automaticamente:

```text
rentacar.db
```

---

# Utilizador Administrador Inicial

Exemplo:

| Utilizador | Senha |
|---|---|
| admin | admin123 |

---

# Funcionalidades Técnicas

- Login autenticado
- Controlo de permissões por perfil
- CRUD de utilizadores
- CRUD de carros
- CRUD de clientes
- Gestão de alugueres
- Registo de devoluções
- Geração automática de faturas
- Interface gráfica com Tkinter

---


# Autor

Projeto desenvolvido para gestão de aluguer de carros em ambiente desktop utilizando Python + Tkinter + SQLite.
