import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta

class DividasView:
    def __init__(self, root, controller, financeiro_controller):
        self.root = root
        self.controller = controller
        self.financeiro_controller = financeiro_controller
        self.criar_widgets()

    def criar_widgets(self):
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill='both', expand=True)

        # Título
        titulo = ttk.Label(main_frame, text="📋 Controle de Quem me Deve", 
                          font=('Arial', 18, 'bold'))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Frame de entrada de dados
        frame_entrada = ttk.LabelFrame(main_frame, text="➕ Nova Dívida", padding="15")
        frame_entrada.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))

        # Configurar grid do frame de entrada
        for i in range(6):
            frame_entrada.columnconfigure(i, weight=1)

        # Linha 1 - Data e Nome
        ttk.Label(frame_entrada, text="Data Empréstimo:", font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.data_emprestimo_entry = DateEntry(frame_entrada, width=15, background='darkblue',
                                              foreground='white', borderwidth=2, 
                                              date_pattern='dd/mm/yyyy', font=('Arial', 10))
        self.data_emprestimo_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 15))

        ttk.Label(frame_entrada, text="Nome *:", font=('Arial', 10)).grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.nome_entry = ttk.Entry(frame_entrada, width=25, font=('Arial', 10))
        self.nome_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(0, 15), columnspan=3)

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
                               command=self.limpar_campos_divida)
        btn_limpar.pack(side=tk.LEFT, padx=5)

        # Frame do dashboard de dívidas
        frame_dashboard = ttk.LabelFrame(main_frame, text="📊 Resumo de Dívidas", padding="15")
        frame_dashboard.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))

        # Cards de métricas para dívidas
        self.total_pendente_var = tk.StringVar(value="R$ 0,00")
        self.total_recebido_var = tk.StringVar(value="R$ 0,00")
        self.quantidade_pendentes_var = tk.StringVar(value="0")
        self.quantidade_vencidas_var = tk.StringVar(value="0")

        self.criar_card_dividas(frame_dashboard, "Total Pendente", self.total_pendente_var, 0, "#dc3545", "💰")
        self.criar_card_dividas(frame_dashboard, "Total Recebido", self.total_recebido_var, 1, "#28a745", "💳")
        self.criar_card_dividas(frame_dashboard, "Dívidas Pendentes", self.quantidade_pendentes_var, 2, "#ffc107", "📋")
        self.criar_card_dividas(frame_dashboard, "Dívidas Vencidas", self.quantidade_vencidas_var, 3, "#fd7e14", "⚠️")

        # Frame da tabela de dívidas
        frame_tabela = ttk.LabelFrame(main_frame, text="📋 Lista de Dívidas", padding="10")
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

        colunas = ('id', 'data_emprestimo', 'nome', 'telefone', 'valor', 'data_vencimento', 'status')
        self.tree_dividas = ttk.Treeview(tree_frame, columns=colunas, show='headings', height=15)

        # Definir cabeçalhos
        cabecalhos = {
            'id': 'ID',
            'data_emprestimo': 'Data Empréstimo',
            'nome': 'Nome', 
            'telefone': 'Telefone',
            'valor': 'Valor (R$)',
            'data_vencimento': 'Vencimento',
            'status': 'Status'
        }

        for col, texto in cabecalhos.items():
            self.tree_dividas.heading(col, text=texto)
            if col in ['id', 'valor']:
                self.tree_dividas.column(col, width=80)
            elif col == 'data_emprestimo' or col == 'data_vencimento':
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

        # Frame de botões para dívidas
        frame_botoes_dividas = ttk.Frame(main_frame)
        frame_botoes_dividas.grid(row=4, column=0, columnspan=3, pady=15)

        botoes_dividas = [
            ("🔄 Atualizar", self.atualizar_dashboard_dividas),
            ("✅ Marcar como Paga", self.marcar_divida_paga),
            ("➕ Registrar como Entrada", self.registrar_entrada_divida),
            ("📧 Enviar Lembrete", self.enviar_lembrete),
            ("🗑️ Excluir Dívida", self.excluir_divida_selecionada),
            ("📊 Exportar Relatório", self.exportar_relatorio_dividas)
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
            data_emprestimo = self.data_emprestimo_entry.get_date()
            nome = self.nome_entry.get().strip()
            telefone = self.telefone_entry.get().strip()
            email = self.email_entry.get().strip()
            valor_str = self.valor_divida_entry.get().replace(',', '.').strip()
            data_vencimento = self.data_vencimento_entry.get_date()
            descricao = self.descricao_divida_entry.get().strip()

            # Validações
            if not nome:
                messagebox.showerror("Erro", "Por favor, preencha o nome do devedor.")
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
            sucesso = self.controller.adicionar_divida(
                data_emprestimo, nome, valor, data_vencimento, telefone, email, descricao
            )

            if sucesso:
                messagebox.showinfo("Sucesso", "Dívida registrada com sucesso!")
                self.limpar_campos_divida()
                self.atualizar_dashboard_dividas()
            else:
                messagebox.showerror("Erro", "Erro ao salvar dívida.")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")

    def limpar_campos_divida(self):
        self.nome_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.valor_divida_entry.delete(0, tk.END)
        self.descricao_divida_entry.delete(0, tk.END)
        self.data_emprestimo_entry.set_date(datetime.now())
        self.data_vencimento_entry.set_date(datetime.now() + timedelta(days=30))

    def atualizar_dashboard_dividas(self):
        try:
            # Atualizar métricas
            total_pendente = self.controller.get_total_pendente()
            total_recebido = self.controller.get_total_recebido()

            dividas_pendentes = [d for d in self.controller.dividas if d.status == 'pendente']
            dividas_vencidas = self.controller.get_dividas_vencidas()

            self.total_pendente_var.set(f"R$ {total_pendente:,.2f}")
            self.total_recebido_var.set(f"R$ {total_recebido:,.2f}")
            self.quantidade_pendentes_var.set(f"{len(dividas_pendentes)}")
            self.quantidade_vencidas_var.set(f"{len(dividas_vencidas)}")

            # Atualizar tabela de dívidas
            for item in self.tree_dividas.get_children():
                self.tree_dividas.delete(item)

            for divida in self.controller.dividas:
                # Formatar valores
                valor_formatado = f"R$ {divida.valor:,.2f}"

                # Formatar datas de forma segura
                try:
                    if hasattr(divida.data_emprestimo, 'strftime'):
                        data_emprestimo_str = divida.data_emprestimo.strftime('%d/%m/%Y')
                    else:
                        data_emprestimo_str = str(divida.data_emprestimo)[:10]
                except:
                    data_emprestimo_str = str(divida.data_emprestimo)

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
                    data_emprestimo_str,
                    divida.nome,
                    divida.telefone,
                    valor_formatado,
                    data_vencimento_str,
                    status_formatado
                ))

        except Exception as e:
            print(f"Erro ao atualizar dashboard de dívidas: {e}")
            messagebox.showerror("Erro", f"Erro ao atualizar dashboard de dívidas: {str(e)}")

    def marcar_divida_paga(self):
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
                             f"Devedor: {valores[2]}\n"
                             f"Valor: {valores[4]}\n"
                             f"Data: {valores[1]}"):
            try:
                sucesso, mensagem = self.controller.marcar_como_paga(divida_id)
                if sucesso:
                    messagebox.showinfo("Sucesso", mensagem)
                    self.atualizar_dashboard_dividas()
                else:
                    messagebox.showerror("Erro", mensagem)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao marcar dívida como paga: {str(e)}")

    def registrar_entrada_divida(self):
        """Registra uma dívida paga como entrada no controle financeiro"""
        selected = self.tree_dividas.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Por favor, selecione uma dívida para registrar como entrada.")
            return
        
        item = selected[0]
        valores = self.tree_dividas.item(item, 'values')
        divida_id = int(valores[0])
        
        # Buscar dados completos da dívida
        divida = self.dividas_controller.get_divida_por_id(divida_id)
        
        # Verificar se já está paga
        if divida.status != 'paga':
            messagebox.showwarning("Aviso", "Primeiro marque a dívida como paga antes de registrar como entrada.")
            return
        
        # Registrar como entrada no controle financeiro
        descricao = f"Recebimento: {divida.nome} - {divida.descricao}" if divida.descricao else f"Recebimento: {divida.nome}"
        data_pagamento = divida.data_pagamento if divida.data_pagamento else datetime.now().date()
        
        sucesso = self.controller.adicionar_transacao(
            data_pagamento, descricao, 'entrada', divida.valor, 'Recebimentos'
        )
        
        if sucesso:
            messagebox.showinfo("Sucesso", f"Entrada registrada com sucesso!\n\n"
                                         f"Devedor: {divida.nome}\n"
                                         f"Valor: R$ {divida.valor:,.2f}\n"
                                         f"Data: {data_pagamento.strftime('%d/%m/%Y')}")
            
            
            self.atualizar_dashboard_dividas()
        else:
            messagebox.showerror("Erro", "Erro ao registrar entrada no controle financeiro.")
    def enviar_lembrete(self):
        selected = self.tree_dividas.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Por favor, selecione uma dívida para enviar lembrete.")
            return

        item = selected[0]
        valores = self.tree_dividas.item(item, 'values')
        divida_id = int(valores[0])

        # Buscar dados completos da dívida
        divida = self.controller.get_divida_por_id(divida_id)

        if divida.status == 'paga':
            messagebox.showinfo("Info", "Esta dívida já está paga.")
            return

        # Simular envio de lembrete
        mensagem = f"""
📧 LEMBRETE DE DÍVIDA

Prezado(a) {divida.nome},

Gostaríamos de lembrá-lo(a) sobre o valor de R$ {divida.valor:,.2f} 
que foi emprestado em {divida.data_emprestimo.strftime('%d/%m/%Y')}.

"""

        if divida.data_vencimento:
            if divida.esta_vencida():
                mensagem += f"⚠️ ATENÇÃO: Esta dívida está VENCIDA desde {divida.data_vencimento.strftime('%d/%m/%Y')}!\n\n"
            else:
                dias_para_vencer = (divida.data_vencimento - datetime.now().date()).days
                mensagem += f"📅 Vencimento: {divida.data_vencimento.strftime('%d/%m/%Y')} ({dias_para_vencer} dias)\n\n"

        if divida.descricao:
            mensagem += f"Descrição: {divida.descricao}\n\n"

        mensagem += "Agradecemos pela atenção.\nAtenciosamente."

        # Mostrar preview da mensagem
        messagebox.showinfo("Lembrete Pronto", 
                          f"📋 Preview do Lembrete:\n\n{mensagem}\n\n"
                          f"📞 Telefone: {divida.telefone or 'Não informado'}\n"
                          f"📧 E-mail: {divida.email or 'Não informado'}\n\n"
                          f"⚠️  Esta é uma simulação. Para implementar o envio real,\n"
                          f"integre com APIs de e-mail ou WhatsApp.")

    def excluir_divida_selecionada(self):
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
                             f"Devedor: {valores[2]}\n"
                             f"Valor: {valores[4]}\n"
                             f"Data: {valores[1]}"):
            sucesso, mensagem = self.controller.excluir_divida(divida_id)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.atualizar_dashboard_dividas()
            else:
                messagebox.showerror("Erro", mensagem)

    def exportar_relatorio_dividas(self):
        # Implementar exportação de relatório de dívidas
        pass