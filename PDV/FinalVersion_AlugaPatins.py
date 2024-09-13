# Importando as bibliotecas necessárias
import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QComboBox, QHBoxLayout, QFormLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


# Classe representando um Patins
class Patins:
    def __init__(self, numero, disponivel=True):
        self.numero = numero
        self.disponivel = disponivel

    def alugar(self):
        self.disponivel = False

    def devolver(self):
        self.disponivel = True

# Classe representando um Cliente
class Cliente:
    def __init__(self, cpf):
        self.cpf = cpf

# Classe representando um Aluguel
class Aluguel:
    def __init__(self, cliente, patins, preco):
        self.cliente = cliente
        self.patins = patins
        self.preco = preco
        self.hora_inicio = datetime.now()
        self.hora_fim = None
        self.dano = False
        self.valor_dano = 0.0
        self.forma_pagamento = None

    def finalizar_aluguel(self, dano=False, valor_dano=0.0):
        self.hora_fim = datetime.now()
        self.dano = dano
        self.valor_dano = valor_dano

    def registrar_pagamento(self, forma_pagamento):
        self.forma_pagamento = forma_pagamento

    def calcular_total(self):
        return self.preco + self.valor_dano

# Classe representando o sistema de PDV
class PDV:
    def __init__(self):
        self.patins = []
        self.alugueis = []

    def cadastrar_patins(self, numero):
        patins = Patins(numero)
        self.patins.append(patins)

    def verificar_disponibilidade(self, numero):
        for patins in self.patins:
            if patins.numero == numero and patins.disponivel:
                return patins
        return None

    def registrar_aluguel(self, cpf, numero, preco):
        cliente = Cliente(cpf)
        patins = self.verificar_disponibilidade(numero)
        if patins:
            patins.alugar()
            aluguel = Aluguel(cliente, patins, preco)
            self.alugueis.append(aluguel)
            return aluguel
        else:
            return None

    def finalizar_aluguel(self, cpf, numero, dano=False, valor_dano=0.0, forma_pagamento="Dinheiro"):
        for aluguel in self.alugueis:
            if aluguel.cliente.cpf == cpf and aluguel.patins.numero == numero and not aluguel.hora_fim:
                aluguel.finalizar_aluguel(dano, valor_dano)
                aluguel.registrar_pagamento(forma_pagamento)
                aluguel.patins.devolver()
                return aluguel.calcular_total()
        return None

    def fechamento_caixa(self):
        if any(aluguel.hora_fim is None for aluguel in self.alugueis):
            return None, None, True  # Retorna um sinal de erro se houver aluguel aberto
        total_dinheiro = sum(a.calcular_total() for a in self.alugueis if a.forma_pagamento == "Dinheiro")
        total_cartao = sum(a.calcular_total() for a in self.alugueis if a.forma_pagamento == "Cartão")
        return total_dinheiro, total_cartao, False

# Classe principal da janela do sistema
class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LocaPatins - Aluguel de Patins")
        self.setGeometry(100, 100, 1080, 1080)
        self.pdv = PDV()
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Sessão para cadastrar Patins
        secao_patins = self.criar_secao_patins()
        main_layout.addWidget(secao_patins)

        # Espaçamento entre seções
        main_layout.addSpacing(10)

        # Sessão de registro de aluguel
        secao_aluguel = self.criar_secao_aluguel()
        main_layout.addWidget(secao_aluguel)

        # Espaçamento entre seções
        main_layout.addSpacing(20)

        # Sessão de devolução de aluguel
        secao_devolucao = self.criar_secao_devolucao()
        main_layout.addWidget(secao_devolucao)

        # Espaçamento entre seções
        main_layout.addSpacing(20)

        # Botões juntos na parte inferior
        botoes_layout = QHBoxLayout()
        main_layout.addLayout(botoes_layout)

        # Botão para cadastrar patins
        self.botao_cadastrar_patins = QPushButton("Cadastrar Patins")
        self.botao_cadastrar_patins.setFixedSize(150, 50)
        self.botao_cadastrar_patins.setStyleSheet("font-weight: bold;")
        self.botao_cadastrar_patins.clicked.connect(self.cadastrar_patins)
        botoes_layout.addWidget(self.botao_cadastrar_patins)

        # Botão para registrar aluguel
        self.botao_registrar_aluguel = QPushButton("Registrar Aluguel")
        self.botao_registrar_aluguel.setFixedSize(150, 50)
        self.botao_registrar_aluguel.setStyleSheet("font-weight: bold;")
        self.botao_registrar_aluguel.clicked.connect(self.registrar_aluguel)
        botoes_layout.addWidget(self.botao_registrar_aluguel)

        # Botão para finalizar aluguel
        self.botao_finalizar_aluguel = QPushButton("Finalizar Aluguel")
        self.botao_finalizar_aluguel.setFixedSize(150, 50)
        self.botao_finalizar_aluguel.setStyleSheet("font-weight: bold;")
        self.botao_finalizar_aluguel.clicked.connect(self.finalizar_aluguel)
        botoes_layout.addWidget(self.botao_finalizar_aluguel)

        # Botão para fechar caixa
        self.botao_fechar_caixa = QPushButton("Fechar Caixa")
        self.botao_fechar_caixa.setFixedSize(150, 50)
        self.botao_fechar_caixa.setStyleSheet("font-weight: bold;")
        self.botao_fechar_caixa.clicked.connect(self.fechar_caixa)
        botoes_layout.addWidget(self.botao_fechar_caixa)

        # Espaçamento inferior
        botoes_layout.addStretch()

    def criar_secao_patins(self):
        patins_group = QWidget()
        layout = QVBoxLayout(patins_group)
        
        titulo = QLabel("Cadastrar Patins:")
        titulo.setStyleSheet("font-weight: bold;")
        layout.addWidget(titulo)

        form_layout = QFormLayout()
        self.input_numero_patins = QLineEdit()
        self.input_numero_patins.setPlaceholderText("Número do Patins")
        form_layout.addRow("Número do Patins:", self.input_numero_patins)

        self.patins_register_button = QPushButton("Cadastrar Patins")
        self.patins_register_button.setFixedHeight(40)
        self.patins_register_button.clicked.connect(self.cadastrar_patins)

        layout.addLayout(form_layout)
        # layout.addWidget(self.patins_register_button)
        
        return patins_group

    def criar_secao_aluguel(self):
        aluguel_group = QWidget()
        layout = QVBoxLayout(aluguel_group)
        
        titulo = QLabel("Registro de Aluguel:")
        titulo.setStyleSheet("font-weight: bold;")
        layout.addWidget(titulo)

        form_layout = QFormLayout()
        self.input_cpf = QLineEdit()
        self.input_cpf.setPlaceholderText("CPF do Cliente")
        self.input_numero_patins_alugar = QLineEdit()
        self.input_numero_patins_alugar.setPlaceholderText("Número do Patins para Alugar")
        self.input_preco = QLineEdit()
        self.input_preco.setPlaceholderText("Preço do Aluguel")

        form_layout.addRow("CPF do Cliente:", self.input_cpf)
        form_layout.addRow("Número do Patins:", self.input_numero_patins_alugar)
        form_layout.addRow("Preço do Aluguel:", self.input_preco)

        layout.addLayout(form_layout)
        
        return aluguel_group

    def criar_secao_devolucao(self):
        devolucao_group = QWidget()
        layout = QVBoxLayout(devolucao_group)
        
        titulo = QLabel("Devolução de Aluguel:")
        titulo.setStyleSheet("font-weight: bold;")
        layout.addWidget(titulo)

        form_layout = QFormLayout()
        self.input_cpf_devolucao = QLineEdit()
        self.input_cpf_devolucao.setPlaceholderText("CPF do Cliente (Devolução)")
        self.input_numero_patins_devolucao = QLineEdit()
        self.input_numero_patins_devolucao.setPlaceholderText("Número do Patins (Devolução)")
        self.input_dano = QComboBox()
        self.input_dano.addItems(["Sem Danos", "Com Danos"])
        self.input_valor_dano = QLineEdit()
        self.input_valor_dano.setPlaceholderText("Valor do Dano (se houver)")
        self.input_forma_pagamento = QComboBox()
        self.input_forma_pagamento.addItems(["Dinheiro", "Cartão"])

        form_layout.addRow("CPF do Cliente:", self.input_cpf_devolucao)
        form_layout.addRow("Número do Patins:", self.input_numero_patins_devolucao)
        form_layout.addRow("Estado do Patins:", self.input_dano)
        form_layout.addRow("Valor do Dano:", self.input_valor_dano)
        form_layout.addRow("Forma de Pagamento:", self.input_forma_pagamento)

        layout.addLayout(form_layout)
        
        return devolucao_group

    def cadastrar_patins(self):
        numero = self.input_numero_patins.text()
        if numero:
            self.pdv.cadastrar_patins(numero)
            QMessageBox.information(self, "Sucesso", f"Patins de número {numero} cadastrado com sucesso.")
            self.input_numero_patins.clear()
        else:
            QMessageBox.warning(self, "Erro", "Número do patins não pode ser vazio.")

    def registrar_aluguel(self):
        cpf = self.input_cpf.text()
        numero = self.input_numero_patins_alugar.text()
        preco = self.input_preco.text()
        if cpf and numero and preco:
            try:
                preco = float(preco)
                aluguel = self.pdv.registrar_aluguel(cpf, numero, preco)
                if aluguel:
                    QMessageBox.information(self, "Sucesso", f"Aluguel registrado para o cliente {cpf}.")
                else:
                    QMessageBox.warning(self, "Erro", "Patins não disponível ou inválido.")
            except ValueError:
                QMessageBox.warning(self, "Erro", "Preço do aluguel deve ser um número.")
            self.input_cpf.clear()
            self.input_numero_patins_alugar.clear()
            self.input_preco.clear()
        else:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")

    def finalizar_aluguel(self):
        cpf = self.input_cpf_devolucao.text()
        numero = self.input_numero_patins_devolucao.text()
        dano = self.input_dano.currentText() == "Com Danos"
        try:
            valor_dano = float(self.input_valor_dano.text()) if dano else 0.0
        except ValueError:
            QMessageBox.warning(self, "Erro", "Valor do dano deve ser um número.")
            return
        forma_pagamento = self.input_forma_pagamento.currentText()

        if cpf and numero:
            total = self.pdv.finalizar_aluguel(cpf, numero, dano, valor_dano, forma_pagamento)
            if total is not None:
                QMessageBox.information(self, "Sucesso", f"Aluguel finalizado. Total a pagar: R${total:.2f}.")
                self.input_cpf_devolucao.clear()
                self.input_numero_patins_devolucao.clear()
                self.input_valor_dano.clear()
            else:
                QMessageBox.warning(self, "Erro", "Aluguel não encontrado ou já finalizado.")
        else:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")

    def fechar_caixa(self):
        total_dinheiro, total_cartao, erro = self.pdv.fechamento_caixa()
        if erro:
            QMessageBox.warning(self, "Erro", "Existem aluguéis em aberto. Não é possível fechar o caixa.")
        else:
            QMessageBox.information(self, "Fechamento de Caixa", 
                                    f"Fechamento de Caixa realizado com sucesso.\n"
                                    f"Total em Dinheiro: R${total_dinheiro:.2f}\n"
                                    f"Total em Cartão: R${total_cartao:.2f}")
            exit()

def main():
    app = QApplication(sys.argv)
    window = JanelaPrincipal()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
