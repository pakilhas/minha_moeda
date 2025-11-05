import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta

class DividasPessoaisView:
    def __init__(self, parent, controller, dividas_pessoais_controller):
        self.parent = parent
        self.controller = controller
        self.dividas_pessoais_controller = dividas_pessoais_controller
        
        self.criar_widgets()
        self.atualizar_dashboard()
    
    def criar_widgets(self):
        """Cria os widgets para a aba de dívidas pessoais"""
        main_frame = ttk.Frame(self.parent, padding="15")
        main_frame.pack(fill='both', expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="💳 Minhas Dívidas", 
                          font=('Arial', 18, 'bold'))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de entrada de dados
        frame_entrada = ttk.LabelFrame(main_frame, text="➕ Nova Dívida Pessoal", padding="15")
        frame_entrada.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Configurar grid do frame de entrada
        for i in range(6):
            frame_entrada.columnconfigure(i, weight=1)
        
        # Linha 1 - Data e Credor
        ttk.Label(frame_entrada, text="Data Compra:", font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.data_compra_entry = DateEntry(frame_entrada, width=15, background='darkblue',
                                           foreground='white', borderwidth=2, 
                                           date_pattern='dd/mm/yyyy', font=('Arial', 10))
        self.data_compra_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 15))
        
        ttk.Label(frame_entrada, text="Credor *:", font=('Arial', 10)).grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.credor_entry = ttk.Entry(frame_entrada, width=25, font=('Arial', 10))
        self.credor_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(0, 15), columnspan=3)
        
        # Linha 2 - Telefone e Email
        ttk.Label(frame_entrada, text="Telefone:", font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.telefone_entry = ttk.Entry(frame_entrada, width=20, font=('Arial', 10))
        self.telefone_entry.grid(row=1, column=1, sticky=tk.W, padx=(0, 15))
        
        ttk.Label(frame_entrada, text="E-mail:", font=('Arial', 10)).grid(row=1, column=2, sticky=tk.W, padx=(0, 5))
        self.email_entry = ttk.Entry(frame_entrada, width=25, font=('Arial', 10))
        self.email_entry.grid(row=1, column=3, sticky=(tk.W, tk.E), padx=(0, 15), columnspan=3)
        
        # Linha 3 - Valor e Data Vencimento
        ttk.Label(frame_entrada, text="Valor R$ *:", font=('Arial', 10)).grid(row=2, column=0, sticky=tk.W, padx=(0, 5))
        self.valor_divida_entry = ttk.Entry(frame_entrada, width=15, font=('Arial', 10, 'bold'))
        self.valor_divida_entry.grid(row=2, column=1, sticky=tk.W, padx=(0, 15))
        
        ttk.Label(frame_entrada, text="Data Vencimento:", font=('Arial', 10)).grid(row=2, column=2, sticky=tk.W, padx=(0, 5))
        self.data_vencimento_entry = DateEntry(frame_entrada, width=15, background='darkblue',
                                               foreground='white', borderwidth=2, 
                                               date_pattern='dd/mm/yyyy', font=('Arial', 10))
        self.data_vencimento_entry.grid(row=2, column=3, sticky=tk.W, padx=(0, 15))
        
        # Linha 4 - Descrição
        ttk.Label(frame_entrada, text="Descrição:", font=('Arial', 10)).grid(row=3, column=0, sticky=tk.W, padx=(0, 5))
        self.descricao_divida_entry = ttk.Entry(frame_entrada, width=50, font=('Arial', 10))
        self.descricao_divida_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(0, 15), columnspan=5)
        
        # Linha 5 - Botões
        frame_botoes_entrada = ttk.Frame(frame_entrada)
        frame_botoes_entrada.grid(row=4, column=0, columnspan=6, pady=(15, 0))
        
        btn_adicionar = ttk.Button(frame_botoes_entrada, text="✅ Adicionar Dívida", 
                                  command=self.adicionar_divida)
        btn_adicionar.pack(side=tk.LEFT, padx=5)
        
        btn_limpar = ttk.Button(frame_botoes_entrada, text="🗑️ Limpar Campos", 
                               command=self.limpar_campos)
        btn_limpar.pack(side=tk.LEFT, padx=5)
        
        # Frame do dashboard de dívidas pessoais
        frame_dashboard = ttk.LabelFrame(main_frame, text="📊 Resumo de Minhas Dívidas", padding="15")
        frame_dashboard.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Cards de métricas para dívidas pessoais
        self.total_pendente_var = tk.StringVar(value="R$ 0,00")
        self.total_pago_var = tk.StringVar(value="R$ 0,00")
        self.quantidade_pendentes_var = tk.StringVar(value="0")
        self.quantidade_vencidas_var = tk.StringVar(value="0")
        
        self.criar_card_dividas(frame_dashboard, "Total Pendente", self.total_pendente_var, 0, "#dc3545", "💰")
        self.criar_card_dividas(frame_dashboard, "Total Pago", self.total_pago_var, 1, "#28a745", "💳")
        self.criar_card_dividas(frame_dashboard, "Dívidas Pendentes", self.quantidade_pendentes_var, 2, "#ffc107", "📋")
        self.criar_card_dividas(frame_dashboard, "Dívidas Vencidas", self.quantidade_vencidas_var, 3, "#fd7e14", "⚠️")
        
        # Frame da tabela de dívidas pessoais
        frame_tabela = ttk.LabelFrame(main_frame, text="📋 Lista de Minhas Dívidas", padding="10")
        frame_tabela.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame_tabela.columnconfigure(0, weight=1)
        frame_tabela.rowconfigure(0, weight=1)
        
        main_frame.rowconfigure(3, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Tabela com scrollbar
        tree_frame = ttk.Frame(frame_tabela)
        tree_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        colunas = ('id', 'data_compra', 'credor', 'telefone', 'valor', 'data_vencimento', 'status')
        self.tree_dividas = ttk.Treeview(tree_frame, columns=colunas, show='headings', height=15)
        
        # Definir cabeçalhos
        cabecalhos = {
            'id': 'ID',
            'data_compra': 'Data Compra',
            'credor': 'Credor', 
            'telefone': 'Telefone',
            'valor': 'Valor (R$)',
            'data_vencimento': 'Vencimento',
            'status': 'Status'
        }
        
        for col, texto in cabecalhos.items():
            self.tree_dividas.heading(col, text=texto)
            if col in ['id', 'valor']:
                self.tree_dividas.column(col, width=80)
            elif col == 'data_compra' or col == 'data_vencimento':
                self.tree_dividas.column(col, width=100)
            elif col == 'telefone':
                self.tree_dividas.column(col, width=120)
            else:
                self.tree_dividas.column(col, width=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_dividas.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree_dividas.xview)
        self.tree_dividas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree_dividas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Frame de botões para dívidas pessoais
        frame_botoes_dividas = ttk.Frame(main_frame)
        frame_botoes_dividas.grid(row=4, column=0, columnspan=3, pady=15)
        
        botoes_dividas = [
            ("🔄 Atualizar", self.atualizar_dashboard),
            ("✅ Marcar como Paga", self.marcar_divida_paga),
            ("💸 Registrar como Saída", self.registrar_saida_divida),
            ("🗑️ Excluir Dívida", self.excluir_divida_selecionada),
            ("📊 Exportar Relatório", self.exportar_relatorio)
        ]
        
        for texto, comando in botoes_dividas:
            btn = ttk.Button(frame_botoes_dividas, text=texto, command=comando)
            btn.pack(side=tk.LEFT, padx=5)
    
    def criar_card_dividas(self, parent, titulo, variavel, coluna, cor, icone=""):
        card = ttk.Frame(parent, relief='solid', borderwidth=1, padding="10")
        card.grid(row=0, column=coluna, padx=5, sticky=(tk.W, tk.E))
        
        lbl_icone = ttk.Label(card, text=icone, font=('Arial', 12))
        lbl_icone.pack()
        
        lbl_titulo = ttk.Label(card, text=titulo, font=('Arial', 9))
        lbl_titulo.pack(pady=(5, 0))
        
        lbl_valor = ttk.Label(card, textvariable=variavel, font=('Arial', 12, 'bold'), 
                             foreground=cor)
        lbl_valor.pack(pady=(5, 0))
        
        parent.columnconfigure(coluna, weight=1)
    
    def adicionar_divida(self):
        try:
            data_compra = self.data_compra_entry.get_date()
            credor = self.credor_entry.get().strip()
            telefone = self.telefone_entry.get().strip()
            email = self.email_entry.get().strip()
            valor_str = self.valor_divida_entry.get().replace(',', '.').strip()
            data_vencimento = self.data_vencimento_entry.get_date()
            descricao = self.descricao_divida_entry.get().strip()
            
            # Validações
            if not credor:
                messagebox.showerror("Erro", "Por favor, preencha o nome do credor.")
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
            
            # Adicionar dívida
            sucesso = self.dividas_pessoais_controller.adicionar_divida(
                data_compra, credor, valor, data_vencimento, telefone, email, descricao
            )
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Dívida registrada com sucesso!")
                self.limpar_campos()
                self.atualizar_dashboard()
            else:
                messagebox.showerror("Erro", "Erro ao salvar dívida.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def limpar_campos(self):
        self.credor_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.valor_divida_entry.delete(0, tk.END)
        self.descricao_divida_entry.delete(0, tk.END)
        self.data_compra_entry.set_date(datetime.now())
        self.data_vencimento_entry.set_date(datetime.now() + timedelta(days=30))
    
    def atualizar_dashboard(self):
        try:
            # Atualizar métricas
            total_pendente = self.dividas_pessoais_controller.get_total_pendente()
            total_pago = self.dividas_pessoais_controller.get_total_pago()
            
            dividas_pendentes = [d for d in self.dividas_pessoais_controller.dividas if d.status == 'pendente']
            dividas_vencidas = self.dividas_pessoais_controller.get_dividas_vencidas()
            
            self.total_pendente_var.set(f"R$ {total_pendente:,.2f}")
            self.total_pago_var.set(f"R$ {total_pago:,.2f}")
            self.quantidade_pendentes_var.set(f"{len(dividas_pendentes)}")
            self.quantidade_vencidas_var.set(f"{len(dividas_vencidas)}")
            
            # Atualizar tabela de dívidas
            for item in self.tree_dividas.get_children():
                self.tree_dividas.delete(item)
            
            for divida in self.dividas_pessoais_controller.dividas:
                # Formatar valores
                valor_formatado = f"R$ {divida.valor:,.2f}"
                
                # Formatar datas de forma segura
                try:
                    if hasattr(divida.data_compra, 'strftime'):
                        data_compra_str = divida.data_compra.strftime('%d/%m/%Y')
                    else:
                        data_compra_str = str(divida.data_compra)[:10]
                except:
                    data_compra_str = str(divida.data_compra)
                
                data_vencimento_str = ""
                if divida.data_vencimento:
                    try:
                        if hasattr(divida.data_vencimento, 'strftime'):
                            data_vencimento_str = divida.data_vencimento.strftime('%d/%m/%Y')
                        else:
                            data_vencimento_str = str(divida.data_vencimento)[:10]
                    except:
                        data_vencimento_str = str(divida.data_vencimento)
                
                # Formatar status com emojis
                if divida.status == 'paga':
                    status_formatado = "✅ Paga"
                else:
                    # Verificar se está vencida
                    if divida.esta_vencida():
                        status_formatado = "⚠️ Vencida"
                    else:
                        status_formatado = "⏳ Pendente"
                
                # Inserir na tabela
                self.tree_dividas.insert('', tk.END, values=(
                    divida.id,
                    data_compra_str,
                    divida.credor,
                    divida.telefone,
                    valor_formatado,
                    data_vencimento_str,
                    status_formatado
                ))
                
        except Exception as e:
            print(f"Erro ao atualizar dashboard de dívidas pessoais: {e}")
            messagebox.showerror("Erro", f"Erro ao atualizar dashboard: {str(e)}")
    
    def marcar_divida_paga(self):
        """Marca a dívida selecionada como paga"""
        selected = self.tree_dividas.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Por favor, selecione uma dívida para marcar como paga.")
            return
        
        item = selected[0]
        valores = self.tree_dividas.item(item, 'values')
        divida_id = int(valores[0])
        
        # Verificar se já está paga
        if valores[6].startswith("✅"):
            messagebox.showinfo("Info", "Esta dívida já está marcada como paga.")
            return
        
        if messagebox.askyesno("Confirmar", 
                             f"Marcar esta dívida como paga?\n\n"
                             f"Credor: {valores[2]}\n"
                             f"Valor: {valores[4]}\n"
                             f"Data: {valores[1]}"):
            try:
                sucesso, mensagem = self.dividas_pessoais_controller.marcar_como_paga(divida_id)
                if sucesso:
                    messagebox.showinfo("Sucesso", mensagem)
                    self.atualizar_dashboard()
                else:
                    messagebox.showerror("Erro", mensagem)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao marcar dívida como paga: {str(e)}")
    
    def registrar_saida_divida(self):
        """Registra uma dívida paga como saída no controle financeiro"""
        selected = self.tree_dividas.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Por favor, selecione uma dívida para registrar como saída.")
            return
        
        item = selected[0]
        valores = self.tree_dividas.item(item, 'values')
        divida_id = int(valores[0])
        
        # Buscar dados completos da dívida
        divida = self.dividas_pessoais_controller.get_divida_por_id(divida_id)
        
        # Verificar se já está paga
        if divida.status != 'paga':
            messagebox.showwarning("Aviso", "Primeiro marque a dívida como paga antes de registrar como saída.")
            return
        
        # Registrar como saída no controle financeiro
        descricao = f"Pagamento: {divida.credor} - {divida.descricao}" if divida.descricao else f"Pagamento: {divida.credor}"
        data_pagamento = divida.data_pagamento if divida.data_pagamento else datetime.now().date()
        
        sucesso = self.controller.adicionar_transacao(
            data_pagamento, descricao, 'saida', divida.valor, 'Pagamento de Dívidas'
        )
        
        if sucesso:
            messagebox.showinfo("Sucesso", f"Saída registrada com sucesso!\n\n"
                                         f"Credor: {divida.credor}\n"
                                         f"Valor: R$ {divida.valor:,.2f}\n"
                                         f"Data: {data_pagamento.strftime('%d/%m/%Y')}")
            
            
            self.atualizar_dashboard()
        else:
            messagebox.showerror("Erro", "Erro ao registrar saída no controle financeiro.")    
    
    def excluir_divida_selecionada(self):
        """Exclui a dívida selecionada"""
        selected = self.tree_dividas.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Por favor, selecione uma dívida para excluir.")
            return
        
        item = selected[0]
        valores = self.tree_dividas.item(item, 'values')
        divida_id = int(valores[0])
        
        if messagebox.askyesno("Confirmar Exclusão", 
                             f"Tem certeza que deseja excluir esta dívida?\n\n"
                             f"ID: {divida_id}\n"
                             f"Credor: {valores[2]}\n"
                             f"Valor: {valores[4]}\n"
                             f"Data: {valores[1]}"):
            sucesso, mensagem = self.dividas_pessoais_controller.excluir_divida(divida_id)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.atualizar_dashboard()
            else:
                messagebox.showerror("Erro", mensagem)
    
    def exportar_relatorio(self):
        """Exporta relatório das dívidas pessoais"""
        try:
            hoje = datetime.now().strftime('%d/%m/%Y às %H:%M')
            total_pendente = self.dividas_pessoais_controller.get_total_pendente()
            total_pago = self.dividas_pessoais_controller.get_total_pago()
            dividas_pendentes = [d for d in self.dividas_pessoais_controller.dividas if d.status == 'pendente']
            dividas_vencidas = self.dividas_pessoais_controller.get_dividas_vencidas()
            
            relatorio = f"""
{'='*60}
RELATÓRIO DE DÍVIDAS PESSOAIS - {datetime.now().strftime('%d/%m/%Y')}
{'='*60}
Gerado em: {hoje}

RESUMO:
{'─'*40}
Total Pendente: R$ {total_pendente:>15,.2f}
Total Pago: R$ {total_pago:>18,.2f}
Dívidas Pendentes: {len(dividas_pendentes):>16}
Dívidas Vencidas: {len(dividas_vencidas):>17}

LISTA DE DÍVIDAS:
{'─'*40}
ID  | Data       | Credor              | Telefone       | Valor       | Vencimento  | Status
{'-'*90}
"""
            for divida in self.dividas_pessoais_controller.dividas:
                # Formatar datas
                try:
                    if hasattr(divida.data_compra, 'strftime'):
                        data_compra_str = divida.data_compra.strftime('%d/%m/%Y')
                    else:
                        data_compra_str = str(divida.data_compra)[:10]
                except:
                    data_compra_str = str(divida.data_compra)
                
                data_vencimento_str = ""
                if divida.data_vencimento:
                    try:
                        if hasattr(divida.data_vencimento, 'strftime'):
                            data_vencimento_str = divida.data_vencimento.strftime('%d/%m/%Y')
                        else:
                            data_vencimento_str = str(divida.data_vencimento)[:10]
                    except:
                        data_vencimento_str = str(divida.data_vencimento)
                
                status = "PAGA" if divida.status == 'paga' else "PENDENTE"
                
                relatorio += f"{divida.id:3} | {data_compra_str} | {divida.credor[:18]:18} | {divida.telefone[:13]:13} | R$ {divida.valor:9,.2f} | {data_vencimento_str:11} | {status:9}\n"

            # Salvar arquivo
            arquivo_relatorio = self.dividas_pessoais_controller.gerenciador.get_caminho_arquivo(
                f"relatorio_dividas_pessoais_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "reports"
            )
            
            with open(arquivo_relatorio, 'w', encoding='utf-8') as f:
                f.write(relatorio)
            
            messagebox.showinfo("Sucesso", f"Relatório de dívidas pessoais exportado:\n{arquivo_relatorio}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar relatório: {str(e)}")