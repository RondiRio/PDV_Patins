# importando as libs

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
import os

class CadastraProduto(QDialog):
    def __init__(self, barcode=None):
        super().__init__()
        self.setWindowTitle("PDV - Cadastro Produto")
        self.setGeometry(100, 100, 600, 600)

        tela = QVBoxLayout()

        self.NomeProduto = QLineEdit(self)
        self.NomeProduto.setPlaceholderText("Nome - inclua nome e sobrenome")
        tela.addWidget(self.NomeProduto)
        
        self.NomeProduto = QLineEdit(self)
        self.NomeProduto.setPlaceholderText("Nome")
        tela.addWidget(self.NomeProduto)

        self.PrecoProduto = QLineEdit(self)
        self.PrecoProduto.setPlaceholderText("Numero patins")
        tela.addWidget(self.PrecoProduto)

        hora_atual =  datetime.datetime.now().strftime("%H:%M:%S")
        self.UnidadeProduto = QLabel(hora_atual)
        tela.addWidget(self.UnidadeProduto)

        self.CodigoProduto = QLineEdit(self)
        self.CodigoProduto.setPlaceholderText("CPF - Cliente")

        if barcode:
            self.CodigoProduto.setText(barcode)
        tela.addWidget(self.CodigoProduto)

        Salvar = QPushButton("Salvar", self)
        Salvar.setStyleSheet("background: red; color: white; font-size: 3em;")
        Salvar.setFont(QFont('Arial', 15))
        Salvar.clicked.connect(self.RegistraProduto)
        tela.addWidget(Salvar)

        self.setLayout(tela)

    def RegistraProduto(self):
        nome = self.NomeProduto.text()
        unidade = self.UnidadeProduto
        preco = self.PrecoProduto.text()
        codigo = self.CodigoProduto.text()
        with open('itensRegistrados.txt', 'a') as file:
            file.write(f"{codigo},{nome},{unidade},{preco}\n")
        QMessageBox.information(self, "Sucesso", "Cliente Registrado.")
        self.accept()


class IndexPDV(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDV - Chessman")
        self.setGeometry(100, 100, 900, 900)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        self.entrarCodigoBarra = QLineEdit()
        self.entrarCodigoBarra.setPlaceholderText("Digite o nome do cliente.")
        self.entrarCodigoBarra.setFixedSize(150, 30)
        self.entrarCodigoBarra.returnPressed.connect(self.adiciona_item)
        main_layout.addWidget(self.entrarCodigoBarra)

        botaoAdicionar = QPushButton("Adicionar Produto", self)
        botaoAdicionar.setStyleSheet("background: blue; color: white; font-size: 3em;")
        botaoAdicionar.setFixedSize(150, 30)
        botaoAdicionar.setFont(QFont('Arial', 15))
        botaoAdicionar.clicked.connect(self.adiciona_item)
        main_layout.addWidget(botaoAdicionar)

        self.botaoBuscarByNome = QLineEdit(self)
        self.botaoBuscarByNome.setPlaceholderText("Buscar pelo nome")
        self.botaoBuscarByNome.returnPressed.connect(self.procurar_produto)
        main_layout.addWidget(self.botaoBuscarByNome)

        self.item_tabela = QTableWidget(self)
        self.item_tabela.setColumnCount(6)
        self.item_tabela.setHorizontalHeaderLabels(["Código", "Nome", "Tamanho", "CPF", "Preço", "Hora"])
        main_layout.addWidget(self.item_tabela)

        self.total_label = QLabel("Total: R$ 0.00", self)
        font = QFont('Arial', 20)
        self.total_label.setFont(font)
        main_layout.addWidget(self.total_label)

        botaoCancelarItem = QPushButton("Cancelar item", self)
        botaoCancelarItem.setStyleSheet("background: red; color: white; font-size: 3em;")
        botaoCancelarItem.setFixedSize(150, 30)
        botaoCancelarItem.setFont(QFont('Arial', 15))
        botaoCancelarItem.clicked.connect(self.cancelar_item)
        # main_layout.addWidget(botaoCancelarItem)
        
        main_layout.addWidget(botaoCancelarItem)
        
        button_layoutCancelaItem = QHBoxLayout()
        button_layoutCancelaItem.addStretch()  # Adiciona um espaço flexível antes do botão
        button_layoutCancelaItem.addWidget(botaoCancelarItem)
        
        # Adicionar o layout do botão ao layout principal
        main_layout.addLayout(button_layoutCancelaItem)

        botaoCancelarVenda = QPushButton("Cancelar venda", self)
        botaoCancelarVenda.setStyleSheet("background: red; color: white; font-size: 3em;")
        botaoCancelarVenda.setFixedSize(150, 30)
        botaoCancelarVenda.setFont(QFont('Arial', 15))
        botaoCancelarVenda.clicked.connect(self.cancelar_venda)
        # main_layout.addWidget(botaoCancelarVenda)
        
        main_layout.addWidget(botaoCancelarVenda)
        
        button_layoutCancelaVenda = QHBoxLayout()
        button_layoutCancelaVenda.addStretch()  # Adiciona um espaço flexível antes do botão
        button_layoutCancelaVenda.addWidget(botaoCancelarVenda)
        
        # Adicionar o layout do botão ao layout principal
        main_layout.addLayout(button_layoutCancelaVenda)

        botaoFinalizarVenda = QPushButton("Finalizar venda", self)
        botaoFinalizarVenda.setStyleSheet("background: green; color: white; font-size: 3em;")
        botaoFinalizarVenda.setFixedSize(150, 30)
        botaoFinalizarVenda.setFont(QFont('Arial', 15))
        botaoFinalizarVenda.clicked.connect(self.pagamento)
        
        # main_layout.addWidget(botaoFinalizarVenda)
        button_layoutbotaoFinalizarVenda = QHBoxLayout()
        button_layoutbotaoFinalizarVenda.addStretch()  # Adiciona um espaço flexível antes do botão
        button_layoutbotaoFinalizarVenda.addWidget(botaoFinalizarVenda)
        
        # Adicionar o layout do botão ao layout principal
        main_layout.addLayout(button_layoutbotaoFinalizarVenda)
        
        self.setLayout(main_layout)

        self.itens = []
        self.total = 0.0

    def adiciona_item(self):
        codigoBarras = self.entrarCodigoBarra.text()
        produtoEncontrado = False

        if os.path.exists("ClientesRegistrados.txt"):
            with open('itensRegistrados.txt', "r") as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) != 4:
                        continue
                    codigo, nome, unidade, preco = parts
                    if codigo == codigoBarras:
                        produtoEncontrado = True
                        item = {"codigo": codigo, "nome": nome, "Tamanho": unidade, "quantidade": 1, "preco": float(preco)}
                        self.itens.append(item)
                        self.atualiza_tabela()
                        self.atualiza_total()
                        break
        if not produtoEncontrado:
            self.abrirCadastroProduto(codigoBarras)

        self.entrarCodigoBarra.clear()

    def atualiza_tabela(self):
        self.item_tabela.setRowCount(len(self.itens))
        for row, item in enumerate(self.itens):
            self.item_tabela.setItem(row, 0, QTableWidgetItem(item["codigo"]))
            self.item_tabela.setItem(row, 1, QTableWidgetItem(item["nome"]))
            self.item_tabela.setItem(row, 2, QTableWidgetItem(item["tamanho"]))
            self.item_tabela.setItem(row, 3, QTableWidgetItem(str(item["quantidade"])))
            self.item_tabela.setItem(row, 4, QTableWidgetItem(f'R$ {item["preco"]:.2f}'))
            self.item_tabela.setItem(row, 5, QTableWidgetItem(f'R$ {item["quantidade"] * item["preco"]:.2f}'))

    def atualiza_total(self):
        self.total = sum(item["quantidade"] * item["preco"] for item in self.itens)
        self.total_label.setText(f"Total: R$ {self.total:,.2f}".rjust(20))

    def procurar_produto(self):
        nome_produto = self.botaoBuscarByNome.text().strip().lower()
        produtoEncontrado = False

        if os.path.exists('itensRegistrados.txt'):
            with open('itensRegistrados.txt', 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) != 4:
                        continue
                    codigo, nome, unidade, preco = parts

                    if nome.lower() == nome_produto:
                        produtoEncontrado = True
                        item = {"codigo": codigo, "nome": nome, "Tamanho": unidade, "quantidade": 1, "preco": float(preco)}

                        self.itens.append(item)
                        self.atualiza_tabela()
                        self.atualiza_total()
                        break
        if not produtoEncontrado:
            QMessageBox.warning(self, "Cliente não encontrado", "Nenhum cliente com esse nome.")

        self.botaoBuscarByNome.clear()

    def pagamento(self):
        dialog = Metodo_pagamento(total=self.total)
        dialog.exec_()

    def cancelar_item(self):
        if self.itens:
            self.itens.pop()
            self.atualiza_tabela()
            self.atualiza_total()

    def cancelar_venda(self):
        self.itens = []
        self.atualiza_tabela()
        self.atualiza_total()

    def fechar_venda(self):
        pass

    def abrirCadastroProduto(self, barcode=None):
        dialog = CadastraProduto(barcode)
        dialog.exec_()


class Metodo_pagamento(QDialog):
    def __init__(self, total):
        super().__init__()
        self.setWindowTitle("Formas de Pagamento")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.total_label = QLabel(f"Total da Compra: R$ {total:.2f}", self)
        layout.addWidget(self.total_label)

        instruction_label = QLabel("Escolha a Forma de Pagamento:", self)
        layout.addWidget(instruction_label)

        self.payment_combobox = QComboBox(self)
        self.payment_combobox.addItems(["Cartão de Crédito", "Boleto", "Pix", "Transferência Bancária"])
        layout.addWidget(self.payment_combobox)

        self.payment_combobox.currentIndexChanged.connect(self.display_selected_payment)

        self.message_label = QLabel("", self)
        layout.addWidget(self.message_label)

        self.setLayout(layout)

    def display_selected_payment(self):
        payment_method = self.payment_combobox.currentText()
        if payment_method:
            self.message_label.setText(f"Você selecionou: {payment_method}")
            botaoFimVenda = QPushButton("Pagar")
            botaoFimVenda.setStyleSheet("background: blue; color: white; font-size: 3em;")
            botaoFimVenda.setFont(QFont('Arial', 15))
            botaoFimVenda.clicked.connect(self.on_payment_button_clicked)
            
            
            botaoVoltar = QPushButton("Pagar")
            botaoVoltar.setStyleSheet("background: blue; color: white; font-size: 3em;")
            botaoVoltar.setFont(QFont('Arial', 15))
            botaoVoltar.clicked.connect(self.on_back_button_clicked)
            
            self.layout().addWidget(botaoFimVenda)
        else:
            self.message_label.setText("")
    def on_payment_button_clicked(self):
    
        print("Pagamento realizado!")
    def on_back_button_clicked(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IndexPDV()
    window.show()
    sys.exit(app.exec_())
