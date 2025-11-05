import pandas as pd
from datetime import datetime
from models.divida_pessoal import DividaPessoal
from utils.file_manager import GerenciadorArquivos

class DividasPessoaisController:
    def __init__(self, gerenciador_arquivos):
        self.gerenciador = gerenciador_arquivos
        self.arquivo = "controle_dividas_pessoais.csv"
        self.dividas = []
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega os dados do arquivo CSV"""
        colunas_esperadas = [
            'id', 'data_compra', 'data_vencimento', 'credor', 'telefone', 
            'email', 'valor', 'descricao', 'status', 'data_pagamento'
        ]
        
        df = self.gerenciador.carregar_dataframe(self.arquivo, colunas_esperadas)
        
        if df is not None:
            # Converter datas de forma segura
            colunas_data = ['data_compra', 'data_vencimento', 'data_pagamento']
            for coluna in colunas_data:
                if coluna in df.columns:
                    df[coluna] = pd.to_datetime(df[coluna], errors='coerce')
                    # Converter para datetime.date
                    df[coluna] = df[coluna].apply(lambda x: x.date() if pd.notna(x) else None)
            
            self.dividas = [DividaPessoal.from_dict(row) for _, row in df.iterrows()]
        else:
            self.dividas = []
    
    def salvar_dados(self):
        """Salva os dados no arquivo CSV"""
        try:
            df = pd.DataFrame([d.to_dict() for d in self.dividas])
            return self.gerenciador.salvar_dataframe(df, self.arquivo)
        except Exception as e:
            print(f"Erro ao salvar dados de dívidas pessoais: {e}")
            return False
    
    def get_proximo_id(self):
        """Retorna o próximo ID disponível"""
        if not self.dividas:
            return 1
        return max(d.id for d in self.dividas) + 1
    
    def adicionar_divida(self, data_compra, credor, valor, data_vencimento=None, 
                        telefone='', email='', descricao=''):
        """Adiciona uma nova dívida pessoal"""
        try:
            # Converter datas para datetime.date
            if isinstance(data_compra, (datetime, pd.Timestamp)):
                data_compra_dt = data_compra.date()
            elif hasattr(data_compra, 'strftime'):
                data_compra_dt = data_compra
            else:
                data_compra_dt = datetime.strptime(data_compra, '%d/%m/%Y').date()
            
            data_vencimento_dt = None
            if data_vencimento:
                if isinstance(data_vencimento, (datetime, pd.Timestamp)):
                    data_vencimento_dt = data_vencimento.date()
                elif hasattr(data_vencimento, 'strftime'):
                    data_vencimento_dt = data_vencimento
                else:
                    data_vencimento_dt = datetime.strptime(data_vencimento, '%d/%m/%Y').date()
            
            nova_divida = DividaPessoal(
                id=self.get_proximo_id(),
                data_compra=data_compra_dt,
                data_vencimento=data_vencimento_dt,
                credor=credor,
                telefone=telefone,
                email=email,
                valor=float(valor),
                descricao=descricao,
                status='pendente',
                data_pagamento=None
            )
            
            self.dividas.append(nova_divida)
            salvo = self.salvar_dados()
            
            return salvo
            
        except Exception as e:
            print(f"Erro ao adicionar dívida pessoal: {e}")
            return False
    
    def marcar_como_paga(self, divida_id, data_pagamento=None):
        """Marca uma dívida como paga"""
        try:
            divida = next((d for d in self.dividas if d.id == divida_id), None)
            if not divida:
                return False, "Dívida não encontrada"
            
            # Converter data_pagamento para datetime.date
            data_pagamento_dt = None
            if data_pagamento:
                if isinstance(data_pagamento, (datetime, pd.Timestamp)):
                    data_pagamento_dt = data_pagamento.date()
                elif hasattr(data_pagamento, 'strftime'):
                    data_pagamento_dt = data_pagamento
                else:
                    data_pagamento_dt = datetime.strptime(data_pagamento, '%d/%m/%Y').date()
            else:
                data_pagamento_dt = datetime.now().date()
            
            divida.status = 'paga'
            divida.data_pagamento = data_pagamento_dt
            
            salvo = self.salvar_dados()
            if salvo:
                return True, "Dívida marcada como paga com sucesso"
            else:
                return False, "Erro ao salvar dados"
            
        except Exception as e:
            return False, f"Erro ao marcar dívida como paga: {str(e)}"
    
    def excluir_divida(self, divida_id):
        """Exclui uma dívida pelo ID"""
        try:
            divida = next((d for d in self.dividas if d.id == divida_id), None)
            if not divida:
                return False, "Dívida não encontrada"
            
            self.dividas = [d for d in self.dividas if d.id != divida_id]
            salvo = self.salvar_dados()
            
            if salvo:
                return True, "Dívida excluída com sucesso"
            else:
                return False, "Erro ao salvar dados após exclusão"
            
        except Exception as e:
            return False, f"Erro ao excluir dívida: {str(e)}"
    
    def get_total_pendente(self):
        """Retorna o total de dívidas pendentes"""
        dividas_pendentes = [d for d in self.dividas if d.status == 'pendente']
        return sum(d.valor for d in dividas_pendentes)
    
    def get_total_pago(self):
        """Retorna o total de dívidas pagas"""
        dividas_pagas = [d for d in self.dividas if d.status == 'paga']
        return sum(d.valor for d in dividas_pagas)
    
    def get_dividas_vencidas(self):
        """Retorna dívidas vencidas"""
        return [d for d in self.dividas if d.esta_vencida()]
    
    def get_dataframe(self):
        """Retorna os dados como DataFrame para a view"""
        if not self.dividas:
            return pd.DataFrame(columns=[
                'id', 'data_compra', 'data_vencimento', 'credor', 'telefone', 
                'email', 'valor', 'descricao', 'status', 'data_pagamento'
            ])
        return pd.DataFrame([d.to_dict() for d in self.dividas])
    
    def get_divida_por_id(self, divida_id):
        """Retorna uma dívida específica pelo ID"""
        return next((d for d in self.dividas if d.id == divida_id), None)