from datetime import datetime
import pandas as pd

class Transacao:
    def __init__(self, id=None, data=None, descricao="", tipo="", valor=0.0, saldo=0.0, categoria=""):
        self.id = id
        self.data = data if data else datetime.now().date()  # Sempre usar date, não datetime
        self.descricao = descricao
        self.tipo = tipo
        self.valor = valor
        self.saldo = saldo
        self.categoria = categoria
    
    def to_dict(self):
        return {
            'id': self.id,
            'data': self.data,
            'descricao': self.descricao,
            'tipo': self.tipo,
            'valor': self.valor,
            'saldo': self.saldo,
            'categoria': self.categoria
        }
    
    @classmethod
    def from_dict(cls, data):
        # Garantir que data seja date, não string ou Timestamp
        data_value = data.get('data')
        if isinstance(data_value, str):
            data_value = datetime.strptime(data_value, '%Y-%m-%d').date()
        elif isinstance(data_value, pd.Timestamp):
            data_value = data_value.date()
        
        return cls(
            id=data.get('id'),
            data=data_value,
            descricao=data.get('descricao', ''),
            tipo=data.get('tipo', ''),
            valor=data.get('valor', 0.0),
            saldo=data.get('saldo', 0.0),
            categoria=data.get('categoria', '')
        )