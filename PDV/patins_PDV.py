import datetime
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QDialog, QMessageBox, QComboBox, QHBoxLayout
)
from PyQt5.QtGui import * 
from PyQt5.QtCore import *

class CadastraAluguel(QDialog):
    def __init__(self, numero=None):
        super().__init__()
        self.setWindowTitle("Aluguel de Patins")
        self.setGeometry(100, 100, 600, 600)

        tela = QVBoxLayout()

        self.NomeCliente = QLineEdit(self)
        self.NomeCliente.setPlaceholderText("Nome do Cliente")
        tela.addWidget(self.NomeCliente)

        self.NumeroPatins = QLineEdit(self)
        self.NumeroPatins.setPlaceholderText("Número do Patins")
        tela.addWidget(self.NumeroPatins)

        hora_atual = datetime.datetime.now().strftime("%H:%M:%S")
        self.HoraAluguel = QLabel(f"Hora do Aluguel: {hora_atual}")
        tela.addWidget(self.HoraAluguel)

        self.CPFCliente = QLineEdit(self)
        self.CPFCliente.setPlaceholderText("CPF do Cliente")
        tela.addWidget(self.CPFCliente)

        if numero:
            self.NumeroPatins.setText(numero)

        tela.addWidget(self.NumeroPatins)

        Salvar = QPushButton("Salvar", self)
        Salvar.setStyleSheet("background: red; color: white; font-size: 2em;")
        Salvar.setFont(QFont('Arial', 15))
        Salvar.clicked.connect(self.RegistraAluguel)
        tela.addWidget(Salvar)

        self.setLayout(tela)

    def RegistraAluguel(self):
        nome = self.NomeCliente.text()
        numero = self.NumeroPatins.text()
        cpf = self.CPFCliente.text()
        hora = datetime.datetime.now().strftime("%H:%M:%S")

        with open('alugueis.txt', 'a') as file:
            file.write(f"{cpf},{nome},{numero},{hora}\n")

        QMessageBox.information(self, "Sucesso", "Aluguel Registrado.")
        self.accept()

class MetodoPagamento(QDialog):
    def __init__(self, total):
        super().__init__()
        self.setWindowTitle("Formas de Pagamento")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.total_label = QLabel(f"Total do Aluguel: R$ {total:.2f}", self)
        layout.addWidget(self.total_label)

        instruction_label = QLabel("Escolha a Forma de Pagamento:", self)
        layout.addWidget(instruction_label)

        self.payment_combobox = QComboBox(self)
        self.payment_combobox.addItems(["Cartão de Crédito", "Boleto", "Pix", "Transferência Bancária"])
        layout.addWidget(self.payment_combobox)

        self.payment_combobox.currentIndexChanged.connect(self.display_selected_payment)

        self.message_label = QLabel("", self)
        layout.addWidget(self.message_label)

        self.botaoFimVenda = QPushButton("Pagar", self)
        self.botaoFimVenda.setStyleSheet("background: green; color: white; font-size: 2em;")
        self.botaoFimVenda.setFont(QFont('Arial', 15))
        self.botaoFimVenda.clicked.connect(self.finalizar_pagamento)
        layout.addWidget(self.botaoFimVenda)

        self.setLayout(layout)

    def display_selected_payment(self):
        payment_method = self.payment_combobox.currentText()
        self.message_label.setText(f"Você selecionou: {payment_method}")

    def finalizar_pagamento(self):
        QMessageBox.information(self, "Pagamento", "Pagamento realizado com sucesso!")
        self.accept()

class AluguelPatins(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Aluguel de Patins")
        self.setGeometry(100, 100, 900, 900)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        
        botaoIniciarAluguel = QPushButton("Iniciar Aluguel", self)
        botaoIniciarAluguel.setStyleSheet("background: blue; color: white; font-size: 2em;")
        botaoIniciarAluguel.setFixedSize(200, 50)
        botaoIniciarAluguel.setFont(QFont('Arial', 15))
        botaoIniciarAluguel.setFixedSize(150, 30)
        botaoIniciarAluguel.setFont(QFont('Arial', 15))
        botaoIniciarAluguel.clicked.connect(self.iniciar_aluguel)
        main_layout.addWidget(botaoIniciarAluguel)
        
        self.entradaNumeroPatins = QLineEdit()
        self.entradaNumeroPatins.setPlaceholderText("Digite o número do patins")
        self.entradaNumeroPatins.setFixedSize(150, 30)
        self.entradaNumeroPatins.returnPressed.connect(self.iniciar_aluguel)
        main_layout.addWidget(self.entradaNumeroPatins)
        
        self.cpf = QLineEdit()
        self.cpf.setPlaceholderText("Digite o CPF do cliente")
        self.cpf.setFixedSize(150, 30)
        self.cpf.returnPressed.connect(self.iniciar_aluguel)
        main_layout.addWidget(self.cpf)
        
        self.item_tabela = QTableWidget(self)
        self.item_tabela.setColumnCount(4)
        self.item_tabela.setHorizontalHeaderLabels(["CPF", "Nome", "Número Patins", "Hora Início"])
        main_layout.addWidget(self.item_tabela)

        botaoFinalizarAluguel = QPushButton("Finalizar Aluguel", self)
        botaoFinalizarAluguel.setStyleSheet("background: green; color: white; font-size: 2em;")
        botaoFinalizarAluguel.setFixedSize(200, 50)
        botaoFinalizarAluguel.setFont(QFont('Arial', 15))
        botaoFinalizarAluguel.clicked.connect(self.finalizar_aluguel)
        main_layout.addWidget(botaoFinalizarAluguel)

        botaoCancelarAluguel = QPushButton("Cancelar Aluguel", self)
        botaoCancelarAluguel.setStyleSheet("background: red; color: white; font-size: 2em;")
        botaoCancelarAluguel.setFixedSize(200, 50)
        botaoCancelarAluguel.setFont(QFont('Arial', 15))
        botaoCancelarAluguel.clicked.connect(self.cancelar_aluguel)
        main_layout.addWidget(botaoCancelarAluguel)

        self.carregar_dados()

    def iniciar_aluguel(self):
        numeroPatins = self.entradaNumeroPatins.text()
        if not numeroPatins and self.cpf:
            QMessageBox.warning(self, "Erro", "Informe o número do patins e o numero do CPF")
            return
        
        dialog = CadastraAluguel(numeroPatins)
        dialog.exec_()
        self.carregar_dados()

    def carregar_dados(self):
        self.item_tabela.setRowCount(0)
        if os.path.exists("alugueis.txt"):
            with open('alugueis.txt', "r") as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 4:
                        cpf, nome, numero, hora = parts
                        rowPosition = self.item_tabela.rowCount()
                        self.item_tabela.insertRow(rowPosition)
                        self.item_tabela.setItem(rowPosition, 0, QTableWidgetItem(cpf))
                        self.item_tabela.setItem(rowPosition, 1, QTableWidgetItem(nome))
                        self.item_tabela.setItem(rowPosition, 2, QTableWidgetItem(numero))
                        self.item_tabela.setItem(rowPosition, 3, QTableWidgetItem(hora))

    def finalizar_aluguel(self):
        if self.item_tabela.rowCount() == 0:
            QMessageBox.warning(self, "Erro", "Nenhum aluguel registrado.")
            return

        row = self.item_tabela.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Erro", "Selecione um aluguel para finalizar.")
            return

        hora_inicio = self.item_tabela.item(row, 3).text()
        hora_fim = datetime.datetime.now().strftime("%H:%M:%S")

        fmt = '%H:%M:%S'
        hora_inicio = datetime.datetime.strptime(hora_inicio, fmt)
        hora_fim = datetime.datetime.strptime(hora_fim, fmt)

        duracao = (hora_fim - hora_inicio).total_seconds() / 3600
        total = duracao * 10  # R$ 10 por hora de aluguel

        dialog = MetodoPagamento(total)
        dialog.exec_()

        self.item_tabela.removeRow(row)

    def cancelar_aluguel(self):
        row = self.item_tabela.currentRow()
        if row != -1:
            self.item_tabela.removeRow(row)
        else:
            QMessageBox.warning(self, "Erro", "Selecione um aluguel para cancelar.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AluguelPatins()
    window.show()
    sys.exit(app.exec_())
