from datetime import datetime
import pandas as pd

class Divida:
    def __init__(self, id=None, data_emprestimo=None, data_vencimento=None, nome="", 
                 telefone="", email="", valor=0.0, descricao="", status="pendente", data_pagamento=None):
        self.id = id
        self.data_emprestimo = data_emprestimo if data_emprestimo else datetime.now().date()
        self.data_vencimento = data_vencimento
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.valor = valor
        self.descricao = descricao
        self.status = status
        self.data_pagamento = data_pagamento
    
    def to_dict(self):
        return {
            'id': self.id,
            'data_emprestimo': self.data_emprestimo,
            'data_vencimento': self.data_vencimento,
            'nome': self.nome,
            'telefone': self.telefone,
            'email': self.email,
            'valor': self.valor,
            'descricao': self.descricao,
            'status': self.status,
            'data_pagamento': self.data_pagamento
        }
    
    @classmethod
    def from_dict(cls, data):
        # Converter datas para date
        def safe_date_conversion(date_value):
            if date_value is None:
                return None
            if isinstance(date_value, str):
                return datetime.strptime(date_value, '%Y-%m-%d').date()
            elif isinstance(date_value, pd.Timestamp):
                return date_value.date()
            return date_value
        
        return cls(
            id=data.get('id'),
            data_emprestimo=safe_date_conversion(data.get('data_emprestimo')),
            data_vencimento=safe_date_conversion(data.get('data_vencimento')),
            nome=data.get('nome', ''),
            telefone=data.get('telefone', ''),
            email=data.get('email', ''),
            valor=data.get('valor', 0.0),
            descricao=data.get('descricao', ''),
            status=data.get('status', 'pendente'),
            data_pagamento=safe_date_conversion(data.get('data_pagamento'))
        )
    
    def esta_vencida(self):
        if self.status == 'paga' or not self.data_vencimento:
            return False
        return self.data_vencimento < datetime.now().date()