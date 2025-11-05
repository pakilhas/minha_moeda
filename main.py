import tkinter as tk
from tkinter import ttk, messagebox
from utils.file_manager import GerenciadorArquivos
from controllers.financeiro_controller import FinanceiroController
from controllers.dividas_controller import DividasController
from controllers.dividas_pessoais_controller import DividasPessoaisController
from views.main_view import MainView
from views.dividas_view import DividasView
from views.dividas_pessoais_view import DividasPessoaisView

class ControleFinanceiroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Controle Financeiro Minha Moeda - v2.0")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f8f9fa')
        
        # Inicializar gerenciador de arquivos e controles
        self.gerenciador = GerenciadorArquivos()
        self.controle_financeiro = FinanceiroController(self.gerenciador)
        self.controle_dividas = DividasController(self.gerenciador)
        self.controle_dividas_pessoais = DividasPessoaisController(self.gerenciador)
        
        # Criar notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Criar as abas
        self.criar_aba_principal()
        self.criar_aba_dividas()
        self.criar_aba_dividas_pessoais()
        
        # Configurar fechamento seguro
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)
    
    def criar_aba_principal(self):
        """Cria a aba principal do controle financeiro"""
        self.aba_principal = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_principal, text="💰 Controle Financeiro")
        
        # CORREÇÃO: Passar o dividas_controller como terceiro parâmetro
        self.view_principal = MainView(self.aba_principal, self.controle_financeiro, self.controle_dividas)
    
    def criar_aba_dividas(self):
        """Cria a aba de controle de dívidas (quem me deve)"""
        self.aba_dividas = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_dividas, text="📋 Quem me Deve")
        
        self.view_dividas = DividasView(self.aba_dividas, self.controle_financeiro, self.controle_dividas)
    
    def criar_aba_dividas_pessoais(self):
        """Cria a aba de controle de dívidas pessoais (minhas dívidas)"""
        self.aba_dividas_pessoais = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_dividas_pessoais, text="💳 Minhas Dívidas")
        
        self.view_dividas_pessoais = DividasPessoaisView(self.aba_dividas_pessoais, self.controle_financeiro, self.controle_dividas_pessoais)
    
    def fechar_aplicacao(self):
        """Fecha a aplicação de forma segura"""
        if messagebox.askokcancel("Sair", "Deseja realmente sair do aplicativo?"):
            # Garantir que os dados estão salvos
            self.controle_financeiro.salvar_dados()
            self.controle_dividas.salvar_dados()
            self.controle_dividas_pessoais.salvar_dados()
            self.root.destroy()

def main():
    try:
        # Configurar estilo moderno
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    root = tk.Tk()
    app = ControleFinanceiroApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()