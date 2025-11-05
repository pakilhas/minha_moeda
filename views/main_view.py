import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

class MainView:
    def __init__(self, parent, controller, dividas_controller):
        self.parent = parent
        self.controller = controller
        self.dividas_controller = dividas_controller
        
        self.criar_widgets()
        self.atualizar_dashboard()
    
    def criar_widgets(self):
        """Cria os widgets para a aba principal"""
        main_frame = ttk.Frame(self.parent, padding="15")
        main_frame.pack(fill='both', expand=True)
        
        # Configurar grid
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="💼 Controle Financeiro Minha Moeda v2.0", 
                          font=('Arial', 18, 'bold'))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de entrada de dados
        frame_entrada = ttk.LabelFrame(main_frame, text="➕ Nova Transação", padding="15")
        frame_entrada.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        frame_entrada.columnconfigure(1, weight=1)
        
        # Linha 1 - Data e Descrição
        ttk.Label(frame_entrada, text="Data:", font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.data_entry = DateEntry(frame_entrada, width=15, background='darkblue',
                                   foreground='white', borderwidth=2, 
                                   date_pattern='dd/mm/yyyy', font=('Arial', 10))
        self.data_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 15))
        
        ttk.Label(frame_entrada, text="Descrição:", font=('Arial', 10)).grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.descricao_entry = ttk.Entry(frame_entrada, width=25, font=('Arial', 10))
        self.descricao_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(0, 15))
        frame_entrada.columnconfigure(3, weight=1)
        
        # Linha 2 - Tipo, Categoria e Valor
        ttk.Label(frame_entrada, text="Tipo:", font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        
        self.tipo_var = tk.StringVar(value="entrada")
        frame_tipo = ttk.Frame(frame_entrada)
        frame_tipo.grid(row=1, column=1, sticky=tk.W)
        ttk.Radiobutton(frame_tipo, text="💰 Entrada", variable=self.tipo_var, 
                       value="entrada", command=self.atualizar_cor_valor).pack(side=tk.LEFT)
        ttk.Radiobutton(frame_tipo, text="💸 Saída", variable=self.tipo_var, 
                       value="saida", command=self.atualizar_cor_valor).pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Label(frame_entrada, text="Categoria:", font=('Arial', 10)).grid(row=1, column=2, sticky=tk.W, padx=(0, 5))
        self.categoria_var = tk.StringVar()
        categorias = ["Salário", "Investimentos", "Alimentação", "Moradia", "Transporte", 
                     "Lazer", "Saúde", "Educação", "Compras", "Serviços", "Outros"]
        self.categoria_combo = ttk.Combobox(frame_entrada, textvariable=self.categoria_var, 
                                           values=categorias, width=15, font=('Arial', 10))
        self.categoria_combo.grid(row=1, column=3, sticky=tk.W, padx=(0, 15))
        self.categoria_combo.set("Outros")
        
        ttk.Label(frame_entrada, text="Valor R$:", font=('Arial', 10)).grid(row=1, column=4, sticky=tk.W, padx=(0, 5))
        self.valor_entry = ttk.Entry(frame_entrada, width=15, font=('Arial', 10, 'bold'))
        self.valor_entry.grid(row=1, column=5, sticky=tk.W)
        
        # Linha 3 - Botões
        frame_botoes_entrada = ttk.Frame(frame_entrada)
        frame_botoes_entrada.grid(row=2, column=0, columnspan=6, pady=(15, 0))
        
        btn_adicionar = ttk.Button(frame_botoes_entrada, text="✅ Adicionar Transação", 
                                  command=self.adicionar_transacao)
        btn_adicionar.pack(side=tk.LEFT, padx=5)
        
        btn_limpar = ttk.Button(frame_botoes_entrada, text="🗑️ Limpar Campos", 
                               command=self.limpar_campos)
        btn_limpar.pack(side=tk.LEFT, padx=5)
        
        # Frame do dashboard
        frame_dashboard = ttk.LabelFrame(main_frame, text="📊 Dashboard Financeiro", padding="15")
        frame_dashboard.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Cards de métricas
        self.saldo_atual_var = tk.StringVar(value="R$ 0,00")
        self.entradas_var = tk.StringVar(value="R$ 0,00")
        self.saidas_var = tk.StringVar(value="R$ 0,00")
        self.saldo_previsto_var = tk.StringVar(value="R$ 0,00")
        
        self.criar_card(frame_dashboard, "Saldo Atual", self.saldo_atual_var, 0, "#28a745", "💳")
        self.criar_card(frame_dashboard, "Entradas Futuras", self.entradas_var, 1, "#17a2b8", "📈")
        self.criar_card(frame_dashboard, "Saídas Futuras", self.saidas_var, 2, "#dc3545", "📉")
        self.criar_card(frame_dashboard, "Saldo Previsto", self.saldo_previsto_var, 3, "#ffc107", "🔮")
        
        # Frame principal com tabela e resumo
        frame_principal = ttk.Frame(main_frame)
        frame_principal.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame_principal.columnconfigure(0, weight=2)
        frame_principal.columnconfigure(1, weight=1)
        frame_principal.rowconfigure(0, weight=1)
        
        # Frame da tabela
        frame_tabela = ttk.LabelFrame(frame_principal, text="📋 Extrato Completo", padding="10")
        frame_tabela.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        frame_tabela.columnconfigure(0, weight=1)
        frame_tabela.rowconfigure(0, weight=1)
        
        # Tabela com scrollbar
        tree_frame = ttk.Frame(frame_tabela)
        tree_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        colunas = ('id', 'data', 'descricao', 'tipo', 'categoria', 'valor', 'saldo')
        self.tree = ttk.Treeview(tree_frame, columns=colunas, show='headings', height=15)
        
        # Definir cabeçalhos
        cabecalhos = {
            'id': 'ID',
            'data': 'Data',
            'descricao': 'Descrição', 
            'tipo': 'Tipo',
            'categoria': 'Categoria',
            'valor': 'Valor (R$)',
            'saldo': 'Saldo (R$)'
        }
        
        for col, texto in cabecalhos.items():
            self.tree.heading(col, text=texto)
            if col == 'id':
                self.tree.column(col, width=50)
            elif col == 'descricao':
                self.tree.column(col, width=200)
            else:
                self.tree.column(col, width=100)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Frame do resumo
        frame_resumo = ttk.LabelFrame(frame_principal, text="📈 Resumo por Categoria", padding="10")
        frame_resumo.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame_resumo.columnconfigure(0, weight=1)
        frame_resumo.rowconfigure(0, weight=1)
        
        # Tabela de resumo
        colunas_resumo = ('categoria', 'total', 'quantidade')
        self.tree_resumo = ttk.Treeview(frame_resumo, columns=colunas_resumo, show='headings', height=15)
        
        self.tree_resumo.heading('categoria', text='Categoria')
        self.tree_resumo.heading('total', text='Total Gasto')
        self.tree_resumo.heading('quantidade', text='Qtd')
        
        self.tree_resumo.column('categoria', width=120)
        self.tree_resumo.column('total', width=100)
        self.tree_resumo.column('quantidade', width=60)
        
        self.tree_resumo.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame de botões inferiores
        frame_botoes = ttk.Frame(main_frame)
        frame_botoes.grid(row=4, column=0, columnspan=3, pady=15)
        
        botoes = [
            ("🔄 Atualizar", self.atualizar_dashboard),
            ("🗑️ Excluir Selecionada", self.excluir_transacao_selecionada),
            ("📊 Exportar Relatório", self.exportar_relatorio),
            ("💾 Backup", self.fazer_backup),
            ("🔄 Recalcular Saldos", self.recalcular_saldos),
            ("🧹 Limpar Tudo", self.limpar_tudo),
            ("❌ Sair", self.fechar_aplicacao)
        ]
        
        for texto, comando in botoes:
            btn = ttk.Button(frame_botoes, text=texto, command=comando)
            btn.pack(side=tk.LEFT, padx=5)
    
    def criar_card(self, parent, titulo, variavel, coluna, cor, icone=""):
        card = ttk.Frame(parent, relief='solid', borderwidth=1, padding="10")
        card.grid(row=0, column=coluna, padx=5, sticky=(tk.W, tk.E))
        
        lbl_icone = ttk.Label(card, text=icone, font=('Arial', 14))
        lbl_icone.pack()
        
        lbl_titulo = ttk.Label(card, text=titulo, font=('Arial', 10))
        lbl_titulo.pack(pady=(5, 0))
        
        lbl_valor = ttk.Label(card, textvariable=variavel, font=('Arial', 14, 'bold'), 
                             foreground=cor)
        lbl_valor.pack(pady=(5, 0))
        
        parent.columnconfigure(coluna, weight=1)
    
    def atualizar_cor_valor(self):
        if self.tipo_var.get() == 'entrada':
            self.valor_entry.configure(foreground='green')
        else:
            self.valor_entry.configure(foreground='red')
    
    def adicionar_transacao(self):
        try:
            data = self.data_entry.get_date()
            descricao = self.descricao_entry.get().strip()
            tipo = self.tipo_var.get()
            categoria = self.categoria_combo.get()
            valor_str = self.valor_entry.get().replace(',', '.').strip()
            
            if not descricao:
                messagebox.showerror("Erro", "Por favor, preencha a descrição.")
                return
            
            if not valor_str:
                messagebox.showerror("Erro", "Por favor, preencha o valor.")
                return
            
            try:
                valor = float(valor_str)
                if valor <= 0:
                    messagebox.showerror("Erro", "O valor deve ser maior que zero.")
                    return
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido. Use números (ex: 150.50).")
                return
            
            sucesso = self.controller.adicionar_transacao(data, descricao, tipo, valor, categoria)
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Transação adicionada com sucesso!")
                self.limpar_campos()
                self.atualizar_dashboard()
            else:
                messagebox.showerror("Erro", "Erro ao salvar transação.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def excluir_transacao_selecionada(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Por favor, selecione uma transação para excluir.")
            return
        
        item = selected[0]
        valores = self.tree.item(item, 'values')
        transacao_id = int(valores[0])
        
        if messagebox.askyesno("Confirmar Exclusão", 
                             f"Tem certeza que deseja excluir esta transação?\n\n"
                             f"ID: {transacao_id}\n"
                             f"Descrição: {valores[2]}\n"
                             f"Data: {valores[1]}\n"
                             f"Valor: {valores[5]}"):
            sucesso, mensagem = self.controller.excluir_transacao(transacao_id)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.atualizar_dashboard()
            else:
                messagebox.showerror("Erro", mensagem)
    
    def limpar_campos(self):
        self.descricao_entry.delete(0, tk.END)
        self.valor_entry.delete(0, tk.END)
        self.categoria_combo.set("Outros")
        self.tipo_var.set("entrada")
        self.data_entry.set_date(datetime.now())
        self.atualizar_cor_valor()
    
    def atualizar_dashboard(self):
        try:
            previsao = self.controller.previsao_final_mes()
            
            self.saldo_atual_var.set(f"R$ {previsao['saldo_atual']:,.2f}")
            self.entradas_var.set(f"R$ {previsao['entradas_futuras']:,.2f}")
            self.saidas_var.set(f"R$ {previsao['saidas_futuras']:,.2f}")
            self.saldo_previsto_var.set(f"R$ {previsao['saldo_final_previsto']:,.2f}")
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            df = self.controller.get_dataframe()
            if df is not None and len(df) > 0:
                for _, row in df.iterrows():
                    valor_absoluto = abs(row['valor'])
                    valor_formatado = f"R$ {valor_absoluto:,.2f}"
                    saldo_formatado = f"R$ {row['saldo']:,.2f}"
                    
                    try:
                        if hasattr(row['data'], 'strftime'):
                            data_str = row['data'].strftime('%d/%m/%Y')
                        else:
                            data_str = str(row['data'])[:10]
                    except:
                        data_str = str(row['data'])

                    if row['tipo'] == 'entrada':
                        tipo_formatado = "💰 Entrada"
                        valor_exibicao = f"+ {valor_formatado}"
                    elif row['tipo'] == 'saida':
                        tipo_formatado = "💸 Saída" 
                        valor_exibicao = f"- {valor_formatado}"
                    else:
                        tipo_formatado = "⚡ Inicial"
                        valor_exibicao = valor_formatado
                    
                    self.tree.insert('', tk.END, values=(
                        row['id'],
                        data_str,
                        row['descricao'],
                        tipo_formatado,
                        row['categoria'],
                        valor_exibicao,
                        saldo_formatado
                    ))
            
            for item in self.tree_resumo.get_children():
                self.tree_resumo.delete(item)
            
            resumo = self.controller.get_resumo_por_categoria()
            for _, row in resumo.iterrows():
                self.tree_resumo.insert('', tk.END, values=(
                    row['Categoria'],
                    f"R$ {row['Total Gasto']:,.2f}",
                    row['Quantidade']
                ))
                
        except Exception as e:
            print(f"Erro ao atualizar dashboard: {e}")
            messagebox.showerror("Erro", f"Erro ao atualizar dashboard: {str(e)}")
    
    def exportar_relatorio(self):
        try:
            previsao = self.controller.previsao_final_mes()
            hoje = datetime.now().strftime('%d/%m/%Y às %H:%M')
            
            relatorio = f"""
{'='*60}
RELATÓRIO FINANCEIRO - {datetime.now().strftime('%d/%m/%Y')}
{'='*60}
Gerado em: {hoje}

RESUMO FINANCEIRO:
{'─'*40}
Saldo Atual: R$ {previsao['saldo_atual']:>15,.2f}
Entradas Futuras: R$ {previsao['entradas_futuras']:>11,.2f}
Saídas Futuras: R$ {previsao['saidas_futuras']:>12,.2f}
Saldo Previsto: R$ {previsao['saldo_final_previsto']:>12,.2f}

EXTRATO COMPLETO:
{'─'*40}
ID  | Data       | Descrição           | Tipo    | Categoria  | Valor       | Saldo
{'-'*80}
"""
            df = self.controller.get_dataframe()
            if df is not None and len(df) > 0:
                for _, row in df.iterrows():
                    tipo = "Entrada" if row['tipo'] == 'entrada' else "Saída" if row['tipo'] == 'saida' else "Inicial"
                    sinal = "+" if row['valor'] > 0 else "-" if row['valor'] < 0 else " "
                    
                    try:
                        if hasattr(row['data'], 'strftime'):
                            data_str = row['data'].strftime('%d/%m/%Y')
                        else:
                            data_str = str(row['data'])[:10]
                    except:
                        data_str = str(row['data'])
                    
                    relatorio += f"{row['id']:3} | {data_str} | {row['descricao'][:18]:18} | {tipo:7} | {row['categoria'][:10]:10} | {sinal} R$ {abs(row['valor']):9,.2f} | R$ {row['saldo']:9,.2f}\n"

            relatorio += f"\nRESUMO POR CATEGORIA:\n{'─'*40}\n"
            resumo = self.controller.get_resumo_por_categoria()
            for _, row in resumo.iterrows():
                relatorio += f"{row['Categoria'][:15]:15} | R$ {row['Total Gasto']:>10,.2f} | {row['Quantidade']:3} transações\n"

            arquivo_relatorio = self.controller.gerenciador.get_caminho_arquivo(
                f"relatorio_financeiro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "reports"
            )
            
            with open(arquivo_relatorio, 'w', encoding='utf-8') as f:
                f.write(relatorio)
            
            messagebox.showinfo("Sucesso", f"Relatório exportado:\n{arquivo_relatorio}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar relatório: {str(e)}")
    
    def fazer_backup(self):
        try:
            sucesso = self.controller.gerenciador.criar_backup("controle_financeiro.csv")
            if sucesso:
                messagebox.showinfo("Sucesso", "Backup criado com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao criar backup.")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar backup: {str(e)}")
    
    def recalcular_saldos(self):
        try:
            self.controller.recalcular_saldos()
            self.controller.salvar_dados()
            self.atualizar_dashboard()
            messagebox.showinfo("Sucesso", "Saldos recalculados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao recalcular saldos: {str(e)}")
    
    def limpar_tudo(self):
        if messagebox.askyesno("Confirmar", 
                             "Tem certeza que deseja limpar TODOS os dados?\n\n"
                             "⚠️  ATENÇÃO: Esta ação não pode ser desfeita!\n"
                             "Todos os registros serão apagados e apenas o saldo inicial permanecerá."):
            try:
                sucesso = self.controller.limpar_todos_dados()
                if sucesso:
                    self.atualizar_dashboard()
                    messagebox.showinfo("Sucesso", "Todos os dados foram limpos!\nApenas o saldo inicial permanece.")
                else:
                    messagebox.showerror("Erro", "Erro ao limpar dados.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao limpar dados: {str(e)}")
    
    def fechar_aplicacao(self):
        """Fecha a aplicação de forma segura"""
        if messagebox.askokcancel("Sair", "Deseja realmente sair do aplicativo?"):
            self.controller.salvar_dados()
            self.parent.quit()