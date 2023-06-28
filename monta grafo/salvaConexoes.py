from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QComboBox, QDialog, QListWidget, QListWidgetItem, QCheckBox, QFileDialog, QMessageBox
from PyQt5.QtCore import QFile, QTextStream
import os

class ListarPessoasWindow(QDialog):
    def __init__(self, pessoas_file, preenchidos):
        super().__init__()
        self.pessoas_file = pessoas_file
        self.selected_persons_ids = []

        # Layout da lista de pessoas
        vbox = QVBoxLayout()

        # Adiciona o rótulo
        label = QLabel("Selecione as pessoas:")
        vbox.addWidget(label)

        # Adiciona o botão Limpar
        btn_limpar = QPushButton("Limpar")
        btn_limpar.clicked.connect(self.limpar_checkboxes)
        vbox.addWidget(btn_limpar)

        # Adiciona a lista
        self.list_widget = QListWidget()
        vbox.addWidget(self.list_widget)

        # Adiciona os checkboxes
        self.pessoas = []
        with open(pessoas_file, "r") as f:
            next(f)  # ignora a primeira linha
            for line in f:
                fields = line.strip().split('\t')
                if len(fields) >= 4:
                    nome, apelido, cidade = fields[1], fields[2], fields[3]
                    self.pessoas.append((fields[0], f"{fields[0]} - {nome}, {apelido}, {cidade}"))

        for id_, nome in self.pessoas:
            item_widget = QWidget(self.list_widget)
            item_layout = QHBoxLayout(item_widget)
            checkbox = QCheckBox(item_widget)
            label = QLabel(nome, item_widget)
            item_layout.addWidget(checkbox)
            item_layout.addWidget(label)
            item_layout.setContentsMargins(0, 0, 0, 0)  # Remove as margens internas
            item_layout.setStretch(1, 1)
            item_layout.setStretch(2, 9)
            checkbox.stateChanged.connect(lambda state, id=id_: self.checkbox_changed(state, id))
            if id_ in preenchidos.split(','):
                checkbox.setChecked(True)
            list_item = QListWidgetItem(self.list_widget)
            #list_item.setSizeHint(item_widget.sizeHint())  # Define o tamanho do item com base no widget interno
            self.list_widget.setItemWidget(list_item, item_widget)

        # Adiciona o botão OK
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.accept)
        vbox.addWidget(btn_ok)

        self.setLayout(vbox)
        self.resize(800, 600)
        

    def checkbox_changed(self, state, id):
        if state == 2:
            self.selected_persons_ids.append(id)
        else:
            self.selected_persons_ids.remove(id)


    def limpar_checkboxes(self):
        for checkbox in self.list_widget.findChildren(QCheckBox):
            checkbox.setChecked(False)
        self.selected_persons_ids = []


class AddConnections(QWidget):
    def __init__(self):
        super().__init__()

        # Label e campo de texto para arquivo de pessoas
        label_pessoas = QLabel("Arquivo pessoas:")
        self.text_pessoas = QLineEdit()
        hbox_pessoas = QHBoxLayout()
        hbox_pessoas.addWidget(label_pessoas)
        hbox_pessoas.addWidget(self.text_pessoas)

        # Label e campo de texto para arquivo de conexões
        label_conexoes = QLabel("Arquivo conexões:")
        self.text_conexoes = QLineEdit()
        hbox_conexoes = QHBoxLayout()
        hbox_conexoes.addWidget(label_conexoes)
        hbox_conexoes.addWidget(self.text_conexoes)

        # Declaração dos campos de origem
        label_origem = QLabel("Origem(ns):")
        self.text_origem = QLineEdit()
        self.text_origem.setReadOnly(True)

         # Botão para trocar origem e destino
        btn_troca = QPushButton("<->")
        btn_troca.clicked.connect(self.troca_origem_destino)

        # Declaração dos campos de destino
        label_destino = QLabel("Destino(s):")
        self.text_destino = QLineEdit()
        self.text_destino.setReadOnly(True)

        # Botões de adicionar origens e destino
        btn_add_origem = QPushButton("+")
        btn_add_origem.clicked.connect(lambda: self.abrir_janela_pessoas("origem", self.text_origem.text()))
        btn_add_destino = QPushButton("+")
        btn_add_destino.clicked.connect(lambda: self.abrir_janela_pessoas("destino", self.text_destino.text()))


        # Layout dos campos de origem
        hbox_origem = QHBoxLayout()
        hbox_origem.addWidget(label_origem)
        hbox_origem.addWidget(btn_add_origem)

        vbox_origem = QVBoxLayout()
        vbox_origem.addLayout(hbox_origem)
        vbox_origem.addWidget(self.text_origem)

        # Layout dos campos de origem
        hbox_destino = QHBoxLayout()
        hbox_destino.addWidget(label_destino)
        hbox_destino.addWidget(btn_add_destino)

        vbox_destino = QVBoxLayout()
        vbox_destino.addLayout(hbox_destino)
        vbox_destino.addWidget(self.text_destino)

        # Layout dos campos de origem destino e troca
        superhbox = QHBoxLayout()
        superhbox.addLayout(vbox_origem)
        superhbox.addWidget(btn_troca)
        superhbox.addLayout(vbox_destino)

        # Lista de opções para tipo de conexão
        self.combo_conexao = QComboBox()
        self.carregar_opcoes_conexao()

        # Botão para salvar conexões
        btn_salvar = QPushButton("Salvar conexão(ões)")
        btn_salvar.clicked.connect(self.salvar_conexao)

        # Layout principal
        vbox = QVBoxLayout()
        vbox.addLayout(hbox_pessoas)
        vbox.addLayout(hbox_conexoes)
        vbox.addLayout(superhbox)
        vbox.addWidget(self.combo_conexao)
        vbox.addWidget(btn_salvar)

        self.setLayout(vbox)


    def carregar_opcoes_conexao(self):
        file = QFile("relacoes.rel")
        if not file.open(QFile.ReadOnly | QFile.Text):
            return

        opcoes = []
        stream = QTextStream(file)
        while not stream.atEnd():
            opcao = stream.readLine().strip()
            opcoes.append(opcao)

        file.close()

        self.combo_conexao.clear()
        self.combo_conexao.addItems(opcoes)


    def troca_origem_destino(self):
        origem = self.text_origem.text()
        destino = self.text_destino.text()
        self.text_origem.setText(destino)
        self.text_destino.setText(origem)


    def abrir_janela_pessoas(self, local, preenchidos):
        if not self.text_pessoas.text():
            QMessageBox.critical(self, "Erro", "Nome de arquivo vazio.")
            return

        try:
            with open(self.text_pessoas.text(), "r") as f:
                header = f.readline()
                texto = f.read().strip()
        except FileNotFoundError:
            QMessageBox.critical(self, "Erro", "Arquivo não encontrado.")
            return
        
        listar_pessoas = ListarPessoasWindow(self.text_pessoas.text(), preenchidos)
        if listar_pessoas.exec_() == QDialog.Accepted:
            pessoas = ''
            for id in listar_pessoas.selected_persons_ids:
                pessoas += id + ','
            if local == 'origem':
                self.text_origem.setText(pessoas[0:len(pessoas)-1])
            elif local == 'destino':
                self.text_destino.setText(pessoas[0:len(pessoas)-1])


    def salvar_conexao(self):
        # Obter os valores dos campos
        origem = self.text_origem.text().strip()
        destino = self.text_destino.text().strip()
        conexao = self.combo_conexao.currentText().strip().split('-')[0]

        # Verificar se os campos foram preenchidos corretamente
        if not origem:
            QMessageBox.warning(self, 'Atenção', 'Preencha o campo Origem.')
            return
        if not destino:
            QMessageBox.warning(self, 'Atenção', 'Preencha o campo Destino.')
            return
        if not conexao:
            QMessageBox.warning(self, 'Atenção', 'Preencha o campo Conexao.')
            return
        
        # Criar a lista de conexões
        conexoes = []
        for o in origem.split(','):
            for d in destino.split(','):
                if o != d:
                    conexoes.append(f'{o} {d}')

        # Verificar se já existe um arquivo de conexões
        if os.path.exists(self.text_conexoes.text()):
            modo = 'a'
        else:
            modo = 'w'

        # Escrever as conexões no arquivo
        with open(self.text_conexoes.text(), modo) as f:
            for c in conexoes:
                f.write(f'{c} {conexao}\n')

        QMessageBox.information(self, 'Sucesso', 'Conexão(ões) salva com sucesso.')


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = AddConnections()
    window.show()
    sys.exit(app.exec_())

