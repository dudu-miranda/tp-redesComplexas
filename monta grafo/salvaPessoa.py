from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QCheckBox
from PyQt5.QtCore import Qt

import os


class Janela(QWidget):
    def __init__(self):
        super().__init__()

        # Define o título da janela e seu tamanho
        self.setWindowTitle("Cadastro de Pessoa")
        self.setGeometry(100, 100, 400, 200)

        # Cria os componentes da janela
        arquivo_label = QLabel("Arquivo de nomes:")
        self.checkbox_arquivo = QCheckBox()
        self.arquivo_text = QLineEdit()
        nome_label = QLabel("Nome:")
        self.checkbox_nome = QCheckBox()
        self.nome_text = QLineEdit()
        apelido_label = QLabel("Apelido:")
        self.checkbox_apelido = QCheckBox()
        self.apelido_text = QLineEdit()
        cidade_label = QLabel("Cidade:")
        self.checkbox_cidade = QCheckBox()
        self.cidade_text = QLineEdit()
        salvar_button = QPushButton("Salvar Pessoa")

        self.checkbox_arquivo.setChecked(Qt.Checked)
        self.checkbox_nome.setChecked(Qt.Checked)
        self.checkbox_apelido.setChecked(Qt.Checked)
        self.checkbox_cidade.setChecked(Qt.Checked)


        # Conecta o sinal stateChanged de cada checkbox ao slot apropriado
        self.checkbox_arquivo.stateChanged.connect(self.habilitar_arquivo_text)
        self.checkbox_nome.stateChanged.connect(self.habilitar_nome_text)
        self.checkbox_apelido.stateChanged.connect(self.habilitar_apelido_text)
        self.checkbox_cidade.stateChanged.connect(self.habilitar_cidade_text)

        # Criando um layout horizontal para cada par de label e checkbox
        layout_arquivo = QHBoxLayout()
        layout_arquivo.addWidget(arquivo_label)
        layout_arquivo.addWidget(self.checkbox_arquivo)
        layout_nome = QHBoxLayout()
        layout_nome.addWidget(nome_label)
        layout_nome.addWidget(self.checkbox_nome)
        layout_apelido = QHBoxLayout()
        layout_apelido.addWidget(apelido_label)
        layout_apelido.addWidget(self.checkbox_apelido)
        layout_cidade = QHBoxLayout()
        layout_cidade.addWidget(cidade_label)
        layout_cidade.addWidget(self.checkbox_cidade)

        # Centraliza o botão na janela
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(salvar_button)
        button_layout.addStretch()
        salvar_button.clicked.connect(self.salvar_pessoa)

        # Organiza os componentes da janela em um layout vertical
        layout = QVBoxLayout()
        layout.addLayout(layout_arquivo)
        layout.addWidget(self.arquivo_text)
        layout.addLayout(layout_nome)
        layout.addWidget(self.nome_text)
        layout.addLayout(layout_apelido)
        layout.addWidget(self.apelido_text)
        layout.addLayout(layout_cidade)
        layout.addWidget(self.cidade_text)
        layout.addLayout(button_layout)

        # Organiza os componentes da janela em um layout vertical
        # layout = QVBoxLayout()
        # layout.addWidget(arquivo_label)
        # layout.addWidget(self.arquivo_text)
        # layout.addWidget(nome_label)
        # layout.addWidget(self.nome_text)
        # layout.addWidget(apelido_label)
        # layout.addWidget(self.apelido_text)
        # layout.addWidget(cidade_label)
        # layout.addWidget(self.cidade_text)
        # layout.addLayout(button_layout)

        # Define o layout da janela
        self.setLayout(layout)
        self.show()


    def salvar_pessoa(self):
        if not self.nome_text.text():
            QMessageBox.warning(self, "Atenção", "Por favor, preencha o campo Nome.")
            return
        if not self.arquivo_text.text():
            QMessageBox.warning(self, "Atenção", "Por favor, preencha o campo Arquivo de Nomes.")
            return

        # Verifica se o arquivo existe e cria se necessário
        if not os.path.exists(self.arquivo_text.text()):
            with open(self.arquivo_text.text(), "w") as f:
                f.write("ID\tNOME\tAPELIDO\tCIDADE\n")

        # 1. Abrir o arquivo para leitura e obter a lista de linhas já existentes
        with open(self.arquivo_text.text(), 'r') as f:
            linhas = f.readlines()

        # 2. Extrair o último ID salvo do arquivo ou definir como 0 caso seja a primeira inserção
        if len(linhas) > 1:
            ultimo_id = int(linhas[-1].split()[0])
        else:
            ultimo_id = 0

        # 3. Obter os dados fornecidos pelo usuário nos campos da interface gráfica
        nome = self.nome_text.text()
        apelido = self.apelido_text.text()
        cidade = self.cidade_text.text()

        # 4. Incrementar o último ID obtido para criar um novo ID único
        novo_id = ultimo_id + 1

        # 5. Escrever o novo registro no arquivo de nomes, com o novo ID, nome, apelido e cidade
        novo_registro = f"{novo_id}\t{{{nome}}}\t[{apelido}]\t({cidade})\n"
        with open(self.arquivo_text.text(), 'a') as f:
            f.write(novo_registro)

        # 6. Atualizar a interface gráfica com a mensagem de confirmação
        msg_box = QMessageBox()
        msg_box.setText(f"A pessoa {nome} foi salva com sucesso!")
        msg_box.exec_()

        # Verifica se o checkbox está marcado para cada campo antes de resetá-lo
        if self.checkbox_arquivo.isChecked():
            self.arquivo_text.setText("")
        if self.checkbox_nome.isChecked():
            self.nome_text.setText("")
        if self.checkbox_apelido.isChecked():
            self.apelido_text.setText("")
        if self.checkbox_cidade.isChecked():
            self.cidade_text.setText("")


    def habilitar_arquivo_text(self, state):
        self.arquivo_text.setEnabled(state == Qt.Checked)


    def habilitar_nome_text(self, state):
        self.nome_text.setEnabled(state == Qt.Checked)


    def habilitar_apelido_text(self, state):
        self.apelido_text.setEnabled(state == Qt.Checked)


    def habilitar_cidade_text(self, state):
        self.cidade_text.setEnabled(state == Qt.Checked)


if __name__ == '__main__':
    app = QApplication([])
    janela = Janela()
    app.exec_()