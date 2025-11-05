import pandas as pd
from datetime import datetime
from models.transacao import Transacao
from utils.file_manager import GerenciadorArquivos

class FinanceiroController:
    def __init__(self, gerenciador_arquivos):
        self.gerenciador = gerenciador_arquivos
        self.arquivo = "controle_financeiro.csv"
        self.transacoes = []
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega os dados do arquivo CSV"""
        colunas_esperadas = ['id', 'data', 'descricao', 'tipo', 'valor', 'saldo', 'categoria']
        
        df = self.gerenciador.carregar_dataframe(self.arquivo, colunas_esperadas)
        
        if df is not None:
            # Converter datas de forma segura
            if 'data' in df.columns:
                df['data'] = pd.to_datetime(df['data'], errors='coerce')
                # Converter para datetime.date (não Timestamp)
                df['data'] = df['data'].apply(lambda x: x.date() if pd.notna(x) else datetime.now().date())
            
            self.transacoes = [Transacao.from_dict(row) for _, row in df.iterrows()]
        else:
            self.criar_estrutura_inicial()
    
    def criar_estrutura_inicial(self):
        """Cria a estrutura inicial com saldo inicial"""
        transacao_inicial = Transacao(
            id=1,
            data=datetime.now().date(),
            descricao="Saldo Inicial",
            tipo="saldo_inicial",
            valor=0.0,
            saldo=0.0,
            categoria="Inicial"
        )
        self.transacoes = [transacao_inicial]
        self.salvar_dados()
    
    def salvar_dados(self):
        """Salva os dados no arquivo CSV"""
        try:
            df = pd.DataFrame([t.to_dict() for t in self.transacoes])
            return self.gerenciador.salvar_dataframe(df, self.arquivo)
        except Exception as e:
            print(f"Erro ao salvar dados financeiros: {e}")
            return False
    
    def get_proximo_id(self):
        """Retorna o próximo ID disponível"""
        if not self.transacoes:
            return 1
        return max(t.id for t in self.transacoes) + 1
    
    def adicionar_transacao(self, data, descricao, tipo, valor, categoria):
        """Adiciona uma nova transação"""
        try:
            # Converter data para formato consistente - SEMPRE para datetime.date
            if isinstance(data, (datetime, pd.Timestamp)):
                data_dt = data.date()
            elif hasattr(data, 'strftime'):
                # Se tem método strftime, é date ou datetime
                data_dt = data
            else:
                # Se é string, converter
                data_dt = datetime.strptime(data, '%d/%m/%Y').date()
            
            # Calcular novo saldo
            saldo_anterior = self.transacoes[-1].saldo if self.transacoes else 0.0
            
            if tipo == 'entrada':
                valor_transacao = abs(valor)
                novo_saldo = saldo_anterior + valor_transacao
            else:  # saida
                valor_transacao = -abs(valor)
                novo_saldo = saldo_anterior - abs(valor)
            
            nova_transacao = Transacao(
                id=self.get_proximo_id(),
                data=data_dt,
                descricao=descricao,
                tipo=tipo,
                valor=valor_transacao,
                saldo=novo_saldo,
                categoria=categoria
            )
            
            self.transacoes.append(nova_transacao)
            self.recalcular_saldos()
            
            salvo = self.salvar_dados()
            if salvo:
                print(f"Transação adicionada: {descricao} - R$ {valor}")
            return salvo
            
        except Exception as e:
            print(f"Erro ao adicionar transação: {e}")
            return False

    def excluir_transacao(self, transacao_id):
        """Exclui uma transação pelo ID"""
        try:
            if transacao_id == 1:  # Não permitir excluir saldo inicial
                return False, "Não é possível excluir o saldo inicial"
            
            transacao_original = next((t for t in self.transacoes if t.id == transacao_id), None)
            if not transacao_original:
                return False, "Transação não encontrada"
            
            self.transacoes = [t for t in self.transacoes if t.id != transacao_id]
            self.recalcular_saldos()
            
            salvo = self.salvar_dados()
            if salvo:
                return True, "Transação excluída com sucesso"
            else:
                return False, "Erro ao salvar dados após exclusão"
            
        except Exception as e:
            return False, f"Erro ao excluir transação: {str(e)}"
    
    def recalcular_saldos(self):
        """Recalcula todos os saldos com base nas transações"""
        if not self.transacoes:
            return
        
        # Ordenar por data e ID
        self.transacoes.sort(key=lambda x: (x.data, x.id))
        
        saldo = 0.0
        for transacao in self.transacoes:
            if transacao.tipo == 'saldo_inicial':
                saldo = transacao.valor
            else:
                saldo += transacao.valor
            transacao.saldo = saldo
    
    def get_dataframe(self):
        """Retorna os dados como DataFrame para a view"""
        if not self.transacoes:
            return pd.DataFrame(columns=['id', 'data', 'descricao', 'tipo', 'valor', 'saldo', 'categoria'])
        return pd.DataFrame([t.to_dict() for t in self.transacoes])
    
    def previsao_final_mes(self):
        """Calcula previsão financeira até o final do mês"""
        try:
            hoje = datetime.now().date()
            
            if not self.transacoes:
                return self._retorno_previsao_padrao()
            
            saldo_atual = self.transacoes[-1].saldo
            
            df = self.get_dataframe()
            if len(df) == 0:
                return self._retorno_previsao_padrao()
            
            # Garantir que a coluna data é datetime
            if 'data' in df.columns:
                df['data'] = pd.to_datetime(df['data'], errors='coerce')
            
            # Converter hoje para Timestamp para comparação
            hoje_ts = pd.Timestamp(hoje)
            
            transacoes_futuras = df[df['data'] > hoje_ts]
            
            entradas_futuras = transacoes_futuras[
                transacoes_futuras['tipo'] == 'entrada'
            ]['valor'].sum()
            
            saidas_futuras = abs(transacoes_futuras[
                transacoes_futuras['tipo'] == 'saida'
            ]['valor'].sum())
            
            saldo_final_previsto = saldo_atual + entradas_futuras - saidas_futuras
            
            return {
                'saldo_atual': saldo_atual,
                'entradas_futuras': entradas_futuras,
                'saidas_futuras': saidas_futuras,
                'saldo_final_previsto': saldo_final_previsto
            }
            
        except Exception as e:
            print(f"Erro no cálculo de previsão: {e}")
            return self._retorno_previsao_padrao()
    
    def get_resumo_por_categoria(self):
        """Retorna resumo de gastos por categoria"""
        try:
            df = self.get_dataframe()
            if len(df) == 0:
                return pd.DataFrame(columns=['Categoria', 'Total Gasto', 'Quantidade'])
            
            saidas = df[df['tipo'] == 'saida']
            if len(saidas) == 0:
                return pd.DataFrame(columns=['Categoria', 'Total Gasto', 'Quantidade'])
            
            resumo = saidas.groupby('categoria')['valor'].agg(['sum', 'count']).reset_index()
            resumo.columns = ['Categoria', 'Total Gasto', 'Quantidade']
            resumo['Total Gasto'] = resumo['Total Gasto'].abs()
            return resumo.sort_values('Total Gasto', ascending=False)
        except Exception as e:
            print(f"Erro no resumo por categoria: {e}")
            return pd.DataFrame(columns=['Categoria', 'Total Gasto', 'Quantidade'])
    
    def limpar_todos_dados(self):
        """Limpa todos os dados e reinicia com saldo inicial"""
        try:
            self.criar_estrutura_inicial()
            return True
        except Exception as e:
            print(f"Erro ao limpar dados: {e}")
            return False
    
    def _retorno_previsao_padrao(self):
        return {
            'saldo_atual': 0.0,
            'entradas_futuras': 0.0,
            'saidas_futuras': 0.0,
            'saldo_final_previsto': 0.0
        }