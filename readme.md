# Controle Financeiro Minha Moeda

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)

Aplicativo desktop em **Python** para gerenciamento financeiro pessoal com interface moderna e módulos integrados de controle de finanças, dívidas e empréstimos.

---

## Visão Geral

O **Minha Moeda** organiza suas finanças em três módulos principais:

* **Controle Financeiro** – Registro de entradas e saídas
* **Quem me Deve** – Gestão de empréstimos e cobranças
* **Minhas Dívidas** – Monitoramento de obrigações e pagamentos

Tudo integrado, com dashboards, relatórios, backups automáticos e previsões financeiras.

---

## Funcionalidades

### Controle Financeiro

* Registro de transações e cálculo automático de saldo
* Dashboard com métricas e previsões
* Filtros, categorias e relatórios por tipo

### Quem me Deve

* Cadastro de devedores e controle de vencimentos
* Marcação de status (pendente/pago)
* Integração com o módulo financeiro

### Minhas Dívidas

* Cadastro de credores e lembretes de vencimento
* Registro automático de saídas
* Relatório de dívidas pessoais

---

## Instalação

### Requisitos

* Python 3.8+
* pip

### Passos

```bash
git clone https://github.com/seu-usuario/minha_moeda.git
cd minha_moeda
pip install pandas tkcalendar
python main.py
```

---

## Como Usar

* Na primeira execução, o aplicativo cria automaticamente as pastas `data/`, `reports/` e `backups/`.
* Adicione uma entrada chamada “Saldo Inicial”.
* Registre entradas e saídas diárias, empréstimos e dívidas.
* Gere relatórios e consulte seu saldo previsto no dashboard.

---

## Tecnologias

* **Python 3.12+**
* **Tkinter (ttk)** – Interface gráfica
* **Pandas** – Manipulação de dados
* **tkcalendar** – Seleção de datas
* **CSV** – Persistência local

---

## Estrutura do Projeto

```
meu_controle_financeiro/
├── controllers/        # Lógica de negócio
├── views/              # Interface do usuário
├── models/             # Estruturas de dados
├── utils/              # Funções auxiliares
├── data/               # Dados locais
├── reports/            # Relatórios gerados
├── backups/            # Backups automáticos
└── main.py             # Ponto de entrada
```

