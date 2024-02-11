import tkinter as tk
import pickle
import os

class State:
    def __init__(self):
        self.email = None
        self.password = None
        self.selected_empresa = None
        self.save_login_info = False

    def get_selected_empresa(self):
        return self.selected_empresa
    
    def save_state(self, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(self.__dict__, file)
    
    def load_state(self, file_path):
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
            self.__dict__.update(data)

    def clear_state(self):
        self.email = None
        self.password = None
        self.selected_empresa = None
        self.save_login_info = False

class LoginPage(tk.Tk):
    def __init__(self, state):
        super().__init__()

        self.state = state
        self.email = None
        self.password = None

        self.geometry("400x300")
        self.title("Login")

        self.label_email = tk.Label(self, text="Email:")
        self.label_email.pack(pady=10)
        self.entry_email = tk.Entry(self)
        self.entry_email.pack(pady=10)

        self.label_password = tk.Label(self, text="Password:")
        self.label_password.pack(pady=10)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=10)

        self.save_login_var = tk.BooleanVar()
        self.chk_save_login = tk.Checkbutton(self, text="Salvar informações de login", variable=self.save_login_var)
        self.chk_save_login.pack(pady=10)


        self.btn_login = tk.Button(self, text="Login", command=self.login)
        self.btn_login.pack(pady=10)

        self.is_closed = False

    def login(self):
        self.state.email = self.entry_email.get()
        self.state.password = self.entry_password.get()
        self.state.save_login_info = self.save_login_var.get()

        if self.state.email and self.state.password:
            if self.state.save_login_info: 
                self.state.save_state("login_state.pkl")
            else:
                self.check_and_remove_login_state_file()
            self.is_closed = True
            self.destroy()   # Fecha a janela de login
    
    def is_closed_correctly(self):
        return self.is_closed
    
    def check_and_remove_login_state_file(self):
        login_state_file = "login_state.pkl"

        if os.path.exists(login_state_file):
            os.remove(login_state_file)
            print(f"Arquivo {login_state_file} removido.")
    
    def load_state(self):
        try:
            self.state.load_state("login_state.pkl")
            self.entry_email.insert(0, self.state.email)
            self.entry_password.insert(0, self.state.password)
            self.save_login_var.set(self.state.save_login_info)
        except FileNotFoundError:
            pass  # O arquivo não existe ainda    

class EmpresaPage(tk.Toplevel):
    def __init__(self, state, empresas):
        super().__init__()

        self.state = state

        self.geometry("400x300")
        self.title("Escolha a Empresa")

        self.label_empresa = tk.Label(self, text="Escolha a Empresa:")
        self.label_empresa.pack(pady=10)

        self.opcoes_empresas = [empresa.text_content() for empresa in empresas]

        self.entry_empresa = tk.StringVar(self)
        self.entry_empresa.set(self.opcoes_empresas[0])  # Valor padrão  
        self.dropdown_empresa = tk.OptionMenu(self, self.entry_empresa, *self.opcoes_empresas)
        self.dropdown_empresa.pack(pady=10)

        self.btn_confirmar = tk.Button(self, text="Confirmar", command=self.confirm)
        self.btn_confirmar.pack(pady=10)

        self.choice = None

    def confirm(self):
        self.state.selected_empresa = self.entry_empresa.get()
        if self.state.selected_empresa:
            self.choice = self.opcoes_empresas.index(self.state.selected_empresa)
            self.destroy()  # Fecha a janela de escolha de empresa

    def get_choice(self):
        return self.choice

    def show(self):
        self.wait_window()
        choice = self.get_choice()
        self.confirm()

    def get_name_empresa(self):
        return self.state.selected_empresa
    
class RepeatOperationPage(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.geometry("300x150")
        self.title("Repetir Operação")

        self.label_prompt = tk.Label(self, text="Deseja repetir a operação?")
        self.label_prompt.pack(pady=10)

        self.btn_sim = tk.Button(self, text="Sim", command=self.confirmar_repeticao)
        self.btn_sim.pack(pady=10)

        self.btn_nao = tk.Button(self, text="Não", command=self.finalizar_repeticao)
        self.btn_nao.pack(pady=10)

        self.repeat_operation = False
        self.is_closed = False


    def confirmar_repeticao(self):
        self.repeat_operation = True
        self.destroy()
        self.is_closed = True

    def finalizar_repeticao(self):
        self.repeat_operation = False
        self.destroy()
        self.is_closed = True



