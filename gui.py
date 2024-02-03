import tkinter as tk
from tkinter import filedialog

class State:
    def __init__(self):
        self.email = None
        self.password = None
        self.selected_empresa = None

    def get_selected_empresa(self):
        return self.selected_empresa

class LoginPage(tk.Tk):
    def __init__(self, state):
        super().__init__()

        self.state = state
        self.email = None
        self.password = None

        self.geometry("300x200")
        self.title("Login")

        self.label_email = tk.Label(self, text="Email:")
        self.label_email.pack(pady=10)
        self.entry_email = tk.Entry(self)
        self.entry_email.pack(pady=10)

        self.label_password = tk.Label(self, text="Password:")
        self.label_password.pack(pady=10)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=10)

        self.btn_login = tk.Button(self, text="Login", command=self.login)
        self.btn_login.pack(pady=10)

        self.is_closed = False

    def login(self):
        self.state.email = self.entry_email.get()
        self.state.password = self.entry_password.get()

        if self.state.email and self.state.password:
            self.is_closed = True
            self.destroy()   # Fecha a janela de login
    
    def is_closed_correctly(self):
        return self.is_closed
    

class EmpresaPage(tk.Toplevel):
    def __init__(self, state, empresas):
        super().__init__()

        self.state = state

        self.geometry("300x200")
        self.title("Escolha a Empresa")

        self.label_empresa = tk.Label(self, text="Escolha a Empresa:")
        self.label_empresa.pack(pady=10)

        self.opcoes_empresas = [empresa.text_content() for empresa in empresas]

        self.entry_empresa = tk.StringVar(self)
        self.entry_empresa.set(self.opcoes_empresas[0])  # Valor padrão  
        self.dropdown_empresa = tk.OptionMenu(self, self.entry_empresa, *self.opcoes_empresas)
        self.dropdown_empresa.pack(pady=10)

        self.btn_confirmar = tk.Button(self, text="Confirmar", command=self.confirmar)
        self.btn_confirmar.pack(pady=10)

        self.choice = None

    def confirmar(self):
        self.state.selected_empresa = self.entry_empresa.get()
        if self.state.selected_empresa:
            self.choice = self.opcoes_empresas.index(self.state.selected_empresa)
            self.destroy()  # Fecha a janela de escolha de empresa

    def get_choice(self):
        return self.choice

    def show(self):
        self.wait_window()
        choice = self.get_choice()
        self.confirmar()

    def get_name_empresa(self):
        return self.state.selected_empresa
    
def choose_download_directory():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Selecione o diretório de downloads")
    return folder_selected