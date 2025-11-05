import pandas as pd
from pathlib import Path
from datetime import datetime
import shutil

class GerenciadorArquivos:
    def __init__(self, base_dir="."):
        self.base_dir = Path(base_dir)
        self.criar_estrutura_pastas()
    
    def criar_estrutura_pastas(self):
        """Cria a estrutura de pastas necessária"""
        pastas = ['data', 'reports', 'backups']
        for pasta in pastas:
            (self.base_dir / pasta).mkdir(exist_ok=True)
    
    def get_caminho_arquivo(self, nome_arquivo, tipo="data"):
        """Retorna o caminho completo do arquivo"""
        if tipo == "data":
            return self.base_dir / 'data' / nome_arquivo
        elif tipo == "reports":
            return self.base_dir / 'reports' / nome_arquivo
        elif tipo == "backups":
            return self.base_dir / 'backups' / nome_arquivo
        return self.base_dir / nome_arquivo
    
    def carregar_dataframe(self, nome_arquivo, colunas_esperadas=None):
        """Carrega um DataFrame do arquivo CSV com tratamento de erros"""
        try:
            caminho = self.get_caminho_arquivo(nome_arquivo)
            if not caminho.exists():
                print(f"Arquivo {nome_arquivo} não encontrado. Criando novo.")
                return None
            
            # Verificar se o arquivo está vazio
            if caminho.stat().st_size == 0:
                print(f"Arquivo {nome_arquivo} está vazio. Criando novo.")
                return None
            
            # Tentar ler o CSV
            try:
                df = pd.read_csv(caminho)
            except pd.errors.EmptyDataError:
                print(f"Arquivo {nome_arquivo} está vazio (EmptyDataError). Criando novo.")
                return None
            except pd.errors.ParserError as e:
                print(f"Erro ao parsear {nome_arquivo}: {e}. Criando novo.")
                return None
            
            # Verificar se o DataFrame está vazio
            if df.empty:
                print(f"Arquivo {nome_arquivo} está vazio. Criando novo.")
                return None
            
            # Adicionar colunas faltantes se especificado
            if colunas_esperadas:
                for coluna in colunas_esperadas:
                    if coluna not in df.columns:
                        df[coluna] = self._get_valor_padrao_coluna(coluna, len(df))
            
            return df
            
        except Exception as e:
            print(f"Erro ao carregar {nome_arquivo}: {e}")
            return None
            
    def salvar_dataframe(self, df, nome_arquivo):
        """Salva um DataFrame no arquivo CSV com tratamento de erros"""
        try:
            caminho = self.get_caminho_arquivo(nome_arquivo)
            df.to_csv(caminho, index=False)
            print(f"Arquivo {nome_arquivo} salvo com sucesso.")
            return True
        except Exception as e:
            print(f"Erro ao salvar {nome_arquivo}: {e}")
            return False
    
    def criar_backup(self, nome_arquivo):
        """Cria um backup do arquivo"""
        try:
            origem = self.get_caminho_arquivo(nome_arquivo)
            if not origem.exists():
                return False
                
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            destino = self.get_caminho_arquivo(
                f"{nome_arquivo.split('.')[0]}_backup_{timestamp}.csv", 
                "backups"
            )
            
            shutil.copy2(origem, destino)
            return True
        except Exception as e:
            print(f"Erro ao criar backup: {e}")
            return False
    
    def _get_valor_padrao_coluna(self, coluna, num_linhas):
        """Retorna valores padrão para colunas faltantes"""
        padroes = {
            'id': range(1, num_linhas + 1),
            'status': 'pendente',
            'saldo': 0.0,
            'valor': 0.0,
            'tipo': 'entrada',
            'categoria': 'Outros'
        }
        return padroes.get(coluna, '')
    
    def criar_arquivo_vazio(self, nome_arquivo, colunas):
        """Cria um arquivo CSV vazio com as colunas especificadas"""
        try:
            caminho = self.get_caminho_arquivo(nome_arquivo)
            df = pd.DataFrame(columns=colunas)
            df.to_csv(caminho, index=False)
            print(f"Arquivo {nome_arquivo} criado com colunas: {colunas}")
            return True
        except Exception as e:
            print(f"Erro ao criar arquivo {nome_arquivo}: {e}")
            return False