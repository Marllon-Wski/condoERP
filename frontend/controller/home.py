from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMessageBox
from condoERP.frontend.model.home import HomeModel


class HomeController(QMainWindow):
    def __init__(self, tacesso):
        super().__init__()

        loader = QUiLoader()
        ui_file = QFile("view/home.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.model = HomeModel()
        self.ui.stackedWidget.setCurrentIndex(0)

        # conecta todos os botões de navegação (feito uma vez)
        self.conectar_botoes()
        self.acessVerify(tacesso)

    # MÉTODOS DE CONEXÃO DE BOTÕES

    def conectar_botoes(self):
        # lista de (attr_name, handler)
        pares = [
            ("pushEncomendas", self.carregaEncomendas),
            ("pushNotificacoes", self.carregaNotificacoes),
            ("pushVeiculos", self.carregaVeiculos),
            ("pushVisitantes", self.carregaVisitantes),
            ("pushOcorrencias", self.carregaOcorrencias),

            ("pushEncomendas_2", self.carregaEncomendas),
            ("pushNotificacoes_2", self.carregaNotificacoes),
            ("pushVeiculos_2", self.carregaVeiculos),
            ("pushVisitantes_2", self.carregaVisitantes),
            ("pushOcorrencias_2", self.carregaOcorrencias),
            ("pushHome_2", self.carregaHome),

            ("pushEncomendas_3", self.carregaEncomendas),
            ("pushNotificacoes_3", self.carregaNotificacoes),
            ("pushVeiculos_3", self.carregaVeiculos),
            ("pushVisitantes_3", self.carregaVisitantes),
            ("pushOcorrencias_3", self.carregaOcorrencias),
            ("pushHome_3", self.carregaHome),

            ("pushEncomendas_4", self.carregaEncomendas),
            ("pushNotificacoes_4", self.carregaNotificacoes),
            ("pushVeiculos_4", self.carregaVeiculos),
            ("pushVisitantes_4", self.carregaVisitantes),
            ("pushOcorrencias_4", self.carregaOcorrencias),
            ("pushHome_4", self.carregaHome),

            ("pushEncomendas_5", self.carregaEncomendas),
            ("pushNotificacoes_5", self.carregaNotificacoes),
            ("pushVeiculos_5", self.carregaVeiculos),
            ("pushVisitantes_5", self.carregaVisitantes),
            ("pushOcorrencias_5", self.carregaOcorrencias),
            ("pushHome_5", self.carregaHome),

            ("pushEncomendas_6", self.carregaEncomendas),
            ("pushNotificacoes_6", self.carregaNotificacoes),
            ("pushVeiculos_6", self.carregaVeiculos),
            ("pushVisitantes_6", self.carregaVisitantes),
            ("pushOcorrencias_6", self.carregaOcorrencias),
            ("pushHome_6", self.carregaHome),

            ("pushAlterarEncomenda", self.alterarEncomenda),
            ("pushExcluirEncomenda", self.excluirEncomenda),
            ("pushNovaEncomenda", self.addEncomenda),

            ("pushAlterarNotificacao", self.alterarNotificacao),
            ("pushExcluirNotificacao", self.excluirNotificacao),
            ("pushNovaNotificacao", self.addNotificacao),

            ("pushAlterarVeiculo", self.alterarVeiculo),
            ("pushExcluirVeiculo", self.excluirVeiculo),
            ("pushNovoVeiculo", self.addVeiculo),

            ("pushAlterarVisitante", self.alterarVisitante),
            ("pushExcluirVisitante", self.excluirVisitante),
            ("pushNovoVisitante", self.addVisitante),

            ("pushAlterarOcorrencia", self.alterarOcorrencia),
            ("pushExcluirOcorrencia", self.excluirOcorrencia),
            ("pushNovaOcorrencia", self.addOcorrencia)
        ]

        for nome, handler in pares:
            widget = getattr(self.ui, nome, None)
            if widget is not None:
                try:
                    widget.clicked.connect(handler)
                except Exception:
                    # caso o widget não tenha sinal clicked, ignora
                    pass

    # MÉTODOS DE ACESSO E RESTRIÇÃO

    def acessVerify(self, tacesso):
        self.ui.pushAlterarEncomenda.setVisible(True)
        self.ui.pushExcluirEncomenda.setVisible(True)
        self.ui.pushNovaEncomenda.setVisible(True)
        self.ui.pushAlterarNotificacao.setVisible(True)
        self.ui.pushExcluirNotificacao.setVisible(True)
        self.ui.pushNovaNotificacao.setVisible(True)
        self.ui.pushAlterarVeiculo.setVisible(True)
        self.ui.pushExcluirVeiculo.setVisible(True)
        self.ui.pushNovoVeiculo.setVisible(True)
        self.ui.pushAlterarVisitante.setVisible(True)
        self.ui.pushExcluirVisitante.setVisible(True)
        self.ui.pushNovoVisitante.setVisible(True)
        self.ui.pushAlterarOcorrencia.setVisible(True)
        self.ui.pushExcluirOcorrencia.setVisible(True)
        self.ui.pushNovaOcorrencia.setVisible(True)

        # 2. Restringindo os acessos baseado no tipo (Forçado para lowercase por segurança)
        tipo = tacesso.lower()

        if tipo == "visitante":
            # Visitante não vê encomendas nem notificações
            self.ui.pushAlterarEncomenda.setVisible(False)
            self.ui.pushExcluirEncomenda.setVisible(False)
            self.ui.pushNovaEncomenda.setVisible(False)
            self.ui.pushAlterarNotificacao.setVisible(False)
            self.ui.pushExcluirNotificacao.setVisible(False)
            self.ui.pushNovaNotificacao.setVisible(False)
            # Visitante não altera veículo nem ocorrências, só vê/adiciona visitante/vaga
            self.ui.pushAlterarVeiculo.setVisible(False)
            self.ui.pushExcluirVeiculo.setVisible(False)
            self.ui.pushNovoVeiculo.setVisible(False)
            self.ui.pushAlterarOcorrencia.setVisible(False)
            self.ui.pushExcluirOcorrencia.setVisible(False)
            self.ui.pushNovaOcorrencia.setVisible(False)

        elif tipo == "morador":
            # Morador faz quase tudo, mas não pode EXCLUIR ou ALTERAR coisas críticas do condomínio
            self.ui.pushExcluirEncomenda.setVisible(False)
            self.ui.pushExcluirNotificacao.setVisible(False)
            self.ui.pushAlterarNotificacao.setVisible(False)
            self.ui.pushNovaNotificacao.setVisible(
                False)  # Quem cria notificação é o Admin
            self.ui.pushExcluirVisitante.setVisible(
                False)  # Portaria quem gerencia saída

        elif tipo == "admin":
            # Admin tem acesso total, não alteramos nada (continua tudo True)
            pass

    # MÉTODOS DE CARREGAMENTO DE TELAS

    def carregaEncomendas(self):
        # funções dos botões da página 2
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.pushEncomendas.blockSignals(True)
        self.ui.pushEncomendas.setEnabled(False)
        self.ui.pushEncomendas_2.blockSignals(True)
        self.ui.pushEncomendas_2.setEnabled(False)
        # self.ui.pushEncomendas_2.clicked.connect(self.carregaEncomendas)

        # a API retorna uma lista de dicionários, ex:
        # {"id": 1, "id_usuario": 3, "descricao": "...",
        #  "data_entrega": "2026-06-10", "data_coleta": None,
        #  "nome_usuario": "João da Silva"}
        dados = self.model.selectEncomendas()

        tabela_sql = QStandardItemModel(len(dados), 5)
        tabela_sql.setHorizontalHeaderLabels(
            ['ID', 'Morador', 'Descrição', 'Data Entrega', 'Data Coleta'])

        for linha_index, linha in enumerate(dados):
            # se não tiver data_entrega, preenche com
            dt_entrega = linha.get("data_entrega") or "---"
            # mesma coisa, com "Aguardando Retirada"
            dt_coleta = linha.get("data_coleta") or "Aguardando Retirada"

            tabela_sql.setItem(linha_index, 0, QStandardItem(
                str(linha.get("id", ""))))            # ID
            tabela_sql.setItem(linha_index, 1, QStandardItem(
                str(linha.get("nome_usuario", ""))))  # Morador
            tabela_sql.setItem(linha_index, 2, QStandardItem(
                str(linha.get("descricao", ""))))     # Descrição
            tabela_sql.setItem(linha_index, 3, QStandardItem(
                str(dt_entrega)))                     # Data Entrega
            tabela_sql.setItem(linha_index, 4, QStandardItem(
                str(dt_coleta)))                      # Data Coleta

        self.ui.tableView.setModel(tabela_sql)

        self.ui.tableView.setColumnWidth(0, 50)   # ID
        self.ui.tableView.setColumnWidth(1, 150)  # Morador
        self.ui.tableView.setColumnWidth(2, 250)  # Descrição bem larga
        self.ui.tableView.setColumnWidth(3, 140)  # Data Entrega

        self.ui.pushEncomendas.blockSignals(False)
        self.ui.pushEncomendas.setEnabled(True)
        self.ui.pushEncomendas_2.blockSignals(False)
        self.ui.pushEncomendas_2.setEnabled(True)

        self.ui.tableView.horizontalHeader().setStretchLastSection(True)

    def carregaNotificacoes(self):

        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.pushNotificacoes.blockSignals(True)
        self.ui.pushNotificacoes.setEnabled(False)
        self.ui.pushNotificacoes_3.blockSignals(True)
        self.ui.pushNotificacoes_3.setEnabled(False)

        # {"id": 1, "id_usuario": 3, "descricao": "...", "nome_usuario": "João da Silva"}
        dados = self.model.buscarNotificacoes()

        tabela_sql = QStandardItemModel(len(dados), 3)
        tabela_sql.setHorizontalHeaderLabels(['ID', 'Usuário', 'Notificação'])

        for linha_index, linha in enumerate(dados):
            tabela_sql.setItem(linha_index, 0, QStandardItem(
                str(linha.get("id", ""))))            # ID
            tabela_sql.setItem(linha_index, 1, QStandardItem(
                str(linha.get("nome_usuario", ""))))  # Usuário
            tabela_sql.setItem(linha_index, 2, QStandardItem(
                str(linha.get("descricao", ""))))     # Notificação

        self.ui.tableView_2.setModel(tabela_sql)

        self.ui.tableView_2.setColumnWidth(0, 50)   # ID curtinho
        self.ui.tableView_2.setColumnWidth(1, 150)  # Usuário

        self.ui.pushNotificacoes.blockSignals(False)
        self.ui.pushNotificacoes.setEnabled(True)
        self.ui.pushNotificacoes_3.blockSignals(False)
        self.ui.pushNotificacoes_3.setEnabled(True)

        self.ui.tableView_2.horizontalHeader().setStretchLastSection(True)

    def carregaVeiculos(self):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.pushVeiculos.blockSignals(True)
        self.ui.pushVeiculos.setEnabled(False)
        self.ui.pushVeiculos_4.blockSignals(True)
        self.ui.pushVeiculos_4.setEnabled(False)

        # {"id": 1, "id_usuario": 3, "placa": "ABC1234", "descricao": "...",
        #  "documento": "...", "nome_usuario": "João da Silva"}
        dados = self.model.buscarVeiculos()

        tabela_sql = QStandardItemModel(len(dados), 5)
        tabela_sql.setHorizontalHeaderLabels(
            ['ID', 'Proprietário', 'Placa', 'Veículo/Descrição', 'Documento'])

        for linha_index, linha in enumerate(dados):
            tabela_sql.setItem(linha_index, 0, QStandardItem(
                str(linha.get("id", ""))))            # ID
            tabela_sql.setItem(linha_index, 1, QStandardItem(
                str(linha.get("nome_usuario", ""))))  # Proprietário
            tabela_sql.setItem(linha_index, 2, QStandardItem(
                str(linha.get("placa", ""))))         # Placa
            tabela_sql.setItem(linha_index, 3, QStandardItem(
                str(linha.get("descricao", ""))))     # Descrição
            tabela_sql.setItem(linha_index, 4, QStandardItem(
                str(linha.get("documento", ""))))     # Documento

        self.ui.tableView_3.setModel(tabela_sql)

        self.ui.tableView_3.setColumnWidth(0, 50)   # ID
        self.ui.tableView_3.setColumnWidth(1, 150)  # Proprietário
        self.ui.tableView_3.setColumnWidth(2, 100)  # Placa
        self.ui.tableView_3.setColumnWidth(3, 200)  # Descricao
        self.ui.tableView_3.setColumnWidth(4, 200)  # Documento

        self.ui.pushVeiculos.blockSignals(False)
        self.ui.pushVeiculos.setEnabled(True)
        self.ui.pushVeiculos_4.blockSignals(False)
        self.ui.pushVeiculos_4.setEnabled(True)

        self.ui.tableView_3.horizontalHeader().setStretchLastSection(True)

    def carregaVisitantes(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        self.ui.pushVisitantes.blockSignals(True)
        self.ui.pushVisitantes.setEnabled(False)
        self.ui.pushVisitantes_5.blockSignals(True)
        self.ui.pushVisitantes_5.setEnabled(False)

        # {"id": 1, "id_user": 2, "id_veiculo": 5, "id_vaga": 3, "id_morador": 1,
        #  "nome": "Maria", "cpf": "...", "telefone": "...", "nome_morador": "João da Silva"}
        dados = self.model.buscarVisitantes()

        tabela_sql = QStandardItemModel(len(dados), 6)
        tabela_sql.setHorizontalHeaderLabels([
            'ID', 'Nome do Visitante', 'Telefone', 'ID Veículo', 'Vaga', 'Morador Visitado'
        ])

        for linha_index, linha in enumerate(dados):
            id_veiculo = str(linha.get("id_veiculo")) if linha.get(
                "id_veiculo") else "A pé"
            vaga = str(linha.get("id_vaga")) if linha.get(
                "id_vaga") else "Sem Vaga"

            tabela_sql.setItem(linha_index, 0, QStandardItem(
                str(linha.get("id", ""))))             # ID Visitante
            tabela_sql.setItem(linha_index, 1, QStandardItem(
                str(linha.get("nome", ""))))           # Nome Visitante
            tabela_sql.setItem(linha_index, 2, QStandardItem(
                str(linha.get("telefone", ""))))       # Telefone
            tabela_sql.setItem(linha_index, 3, QStandardItem(
                id_veiculo))                            # Veículo
            tabela_sql.setItem(linha_index, 4, QStandardItem(
                vaga))                                  # Vaga
            tabela_sql.setItem(linha_index, 5, QStandardItem(
                str(linha.get("nome_morador", ""))))   # Nome Morador

        self.ui.tableView_4.setModel(tabela_sql)

        self.ui.tableView_4.setColumnWidth(0, 40)   # ID
        self.ui.tableView_4.setColumnWidth(1, 180)  # Nome Visitante
        self.ui.tableView_4.setColumnWidth(2, 110)  # Telefone
        self.ui.tableView_4.setColumnWidth(3, 70)   # Veículo
        self.ui.tableView_4.setColumnWidth(4, 100)  # Vaga

        self.ui.pushVisitantes.blockSignals(False)
        self.ui.pushVisitantes.setEnabled(True)
        self.ui.pushVisitantes_5.blockSignals(False)
        self.ui.pushVisitantes_5.setEnabled(True)

        self.ui.tableView_4.horizontalHeader().setStretchLastSection(True)

    def carregaOcorrencias(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        self.ui.pushOcorrencias.blockSignals(True)
        self.ui.pushOcorrencias.setEnabled(False)
        self.ui.pushOcorrencias_6.blockSignals(True)
        self.ui.pushOcorrencias_6.setEnabled(False)

        # {"id": 1, "id_usuario": 3, "descricao": "...", "nome_usuario": "João da Silva"}
        dados = self.model.buscarOcorrencias()

        tabela_sql = QStandardItemModel(len(dados), 3)
        tabela_sql.setHorizontalHeaderLabels(
            ['ID', 'Registrado por', 'Descrição da Ocorrência'])

        for linha_index, linha in enumerate(dados):
            tabela_sql.setItem(linha_index, 0, QStandardItem(
                str(linha.get("id", ""))))            # ID Ocorrência
            tabela_sql.setItem(linha_index, 1, QStandardItem(
                str(linha.get("nome_usuario", ""))))  # Nome do Usuário
            tabela_sql.setItem(linha_index, 2, QStandardItem(
                str(linha.get("descricao", ""))))     # Descrição

        self.ui.tableView_5.setModel(tabela_sql)

        self.ui.tableView_5.setColumnWidth(0, 50)   # ID
        self.ui.tableView_5.setColumnWidth(1, 150)  # Nome de quem reclamou

        self.ui.pushOcorrencias.blockSignals(False)
        self.ui.pushOcorrencias.setEnabled(True)
        self.ui.pushOcorrencias_6.blockSignals(False)
        self.ui.pushOcorrencias_6.setEnabled(True)

        self.ui.tableView_5.horizontalHeader().setStretchLastSection(True)

    def carregaHome(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    # MÉTODOS DE GERENCIAMENTO (ENCOMENDAS)

    def addEncomenda(self):
        loader = QUiLoader()
        ui_file = QFile("view/addEncomenda.ui")
        ui_file.open(QFile.ReadOnly)

        self.dialog_encomenda = loader.load(ui_file, self)
        ui_file.close()

        self.dialog_encomenda.btnSalvar.clicked.connect(
            self.salvar_nova_encomenda)
        self.dialog_encomenda.btnCancelar.clicked.connect(
            self.dialog_encomenda.reject)

        self.dialog_encomenda.exec()

    def salvar_nova_encomenda(self):
        id = self.dialog_encomenda.lineEdit.text().strip()
        descricao = self.dialog_encomenda.lineEdit_2.text().strip()
        data = self.dialog_encomenda.dateEdit.date().toString("yyyy-MM-dd")

        if not descricao:
            QMessageBox.warning(self.dialog_encomenda, "Erro",
                                "O campo descrição é obrigatório.")
            return

        sucesso = self.model.inserirEncomendas(id, descricao, data)

        if sucesso:
            print(f"Salvando no banco: {descricao}")
            self.dialog_encomenda.accept()
            self.carregaEncomendas()
        else:
            print(f"Erro na inclusão do banco de dados.")
            self.carregaEncomendas()
            return

    def excluirEncomenda(self):
        from PySide6.QtWidgets import QMessageBox
        index = self.ui.tableView.currentIndex()
        if not index.isValid():
            QMessageBox.warning(
                self, "Aviso", "Selecione uma linha na tabela para excluir.")
            return

        id_selecionado = self.ui.tableView.model().item(index.row(), 0).text()

        botao = QMessageBox.question(
            self, "Confirmar Exclusão",
            f"Deseja realmente excluir a encomenda ID {id_selecionado}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if botao == QMessageBox.Yes:
            self.model.deletarEncomenda(id_selecionado)
            print(f"Encomenda {id_selecionado} excluída com sucesso.")
            self.carregaEncomendas()  # Recarrega a tabela

    def alterarEncomenda(self):
        from PySide6.QtWidgets import QMessageBox
        index = self.ui.tableView.currentIndex()
        if not index.isValid():
            QMessageBox.warning(
                self, "Aviso", "Selecione uma linha para alterar.")
            return

        # Habilita a edição inline diretamente na linha selecionada da tabela
        self.ui.tableView.edit(index)
        print("Modo de edição inline ativado para Encomendas.")

    # MÉTODOS DE GERENCIAMENTO (NOTIFICAÇÕES)

    def addNotificacao(self):
        loader = QUiLoader()
        ui_file = QFile("view/addNotificacao.ui")
        ui_file.open(QFile.ReadOnly)

        self.dialog_notificacao = loader.load(ui_file, self)
        ui_file.close()

        self.dialog_notificacao.btnSalvar.clicked.connect(
            self.salvar_nova_notificacao)
        self.dialog_notificacao.btnCancelar.clicked.connect(
            self.dialog_notificacao.reject)
        self.dialog_notificacao.exec()

    def salvar_nova_notificacao(self):
        id = self.dialog_notificacao.lineEdit.text().strip()
        descricao = self.dialog_notificacao.lineEdit_2.text()

        if not descricao:
            QMessageBox.warning(self.dialog_notificacao,
                                "Erro", "O campo descrição é obrigatório.")
            return

        sucesso = self.model.inserirNotificacao(id, descricao)

        if sucesso:
            print(f"Salvando no banco: {descricao}")
            self.dialog_notificacao.accept()
            self.carregaNotificacoes()
        else:
            print(f"Erro na inclusão do banco de dados.")
            self.carregaNotificacoes()
            return

    def excluirNotificacao(self):
        index = self.ui.tableView_2.currentIndex()
        if not index.isValid():
            QMessageBox.warning(
                self, "Aviso", "Selecione uma linha na tabela para excluir.")
            return

        id_selecionado = self.ui.tableView_2.model().item(index.row(), 0).text()

        botao = QMessageBox.question(
            self, "Confirmar Exclusão",
            f"Deseja realmente excluir a notificação ID {id_selecionado}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if botao == QMessageBox.Yes:
            self.model.deletarNotificacao(id_selecionado)
            print(f"Notificação {id_selecionado} excluída.")
            self.carregaNotificacoes()

    def alterarNotificacao(self):
        index = self.ui.tableView_2.currentIndex()
        if not index.isValid():
            QMessageBox.warning(
                self, "Aviso", "Selecione uma linha para alterar.")
            return
        self.ui.tableView_2.edit(index)

    # MÉTODOS DE GERENCIAMENTO (VEÍCULOS)

    def addVeiculo(self):
        loader = QUiLoader()
        ui_file = QFile("view/addVeiculo.ui")
        ui_file.open(QFile.ReadOnly)
        self.dialog_veiculo = loader.load(ui_file, self)
        ui_file.close()

        self.dialog_veiculo.btnSalvar.clicked.connect(self.salvar_novo_veiculo)
        self.dialog_veiculo.btnCancelar.clicked.connect(
            self.dialog_veiculo.reject)
        self.dialog_veiculo.exec()

    def salvar_novo_veiculo(self):
        id_user = self.dialog_veiculo.lineEdit.text().strip()
        # Força letras maiúsculas na placa
        placa = self.dialog_veiculo.lineEdit_2.text().strip().upper()
        descricao = self.dialog_veiculo.lineEdit_3.text()
        documento = self.dialog_veiculo.lineEdit_4.text()

        if not placa or not descricao:
            QMessageBox.warning(self.dialog_veiculo, "Erro",
                                "Placa e Descrição são obrigatórios.")
            return

        sucesso = self.model.inserirVeiculos(
            id_user, placa, descricao, documento)
        if sucesso:
            print(f"Veículo salvo: {placa}")
            self.dialog_veiculo.accept()
            self.carregaVeiculos()
        else:
            print("Erro na inclusão do veículo.")
            self.carregaVeiculos()

    def excluirVeiculo(self):
        from PySide6.QtWidgets import QMessageBox
        index = self.ui.tableView_3.currentIndex()
        if not index.isValid():
            QMessageBox.warning(
                self, "Aviso", "Selecione uma linha na tabela para excluir.")
            return

        id_selecionado = self.ui.tableView_3.model().item(index.row(), 0).text()
        botao = QMessageBox.question(
            self, "Confirmar Exclusão",
            f"Deseja realmente excluir o veículo ID {id_selecionado}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if botao == QMessageBox.Yes:
            self.model.deletarVeiculo(id_selecionado)
            print(f"Veículo {id_selecionado} excluído.")
            self.carregaVeiculos()

    def alterarVeiculo(self):
        index = self.ui.tableView_3.currentIndex()
        if not index.isValid():
            QMessageBox.warning(
                self, "Aviso", "Selecione uma linha para alterar.")
            return
        self.ui.tableView_3.edit(index)

    # MÉTODOS DE GERENCIAMENTO (VISITANTES)

    def addVisitante(self):
        loader = QUiLoader()
        ui_file = QFile("view/addVisitante.ui")
        ui_file.open(QFile.ReadOnly)
        self.dialog_visitante = loader.load(ui_file, self)
        ui_file.close()

        self.dialog_visitante.btnSalvar.clicked.connect(
            self.salvar_novo_visitante)
        self.dialog_visitante.btnCancelar.clicked.connect(
            self.dialog_visitante.reject)
        self.dialog_visitante.exec()

    def salvar_novo_visitante(self):
        id_user = self.dialog_visitante.lineEdit.text().strip()
        id_veiculo = self.dialog_visitante.lineEdit_2.text().strip() or None
        id_vaga = self.dialog_visitante.lineEdit_3.text().strip() or None
        id_morador = self.dialog_visitante.lineEdit_4.text().strip()

        if not id_user or not id_morador:
            QMessageBox.warning(self.dialog_visitante, "Erro",
                                "Campos Usuário e Morador são obrigatórios.")
            return

        sucesso = self.model.inserirVisitantes(
            id_user, id_veiculo, id_vaga, id_morador)
        if sucesso:
            print("Visitante incluído com sucesso.")
            self.dialog_visitante.accept()
            self.carregaVisitantes()
        else:
            print("Erro na inclusão do visitante.")
            self.carregaVisitantes()

    def excluirVisitante(self):
        from PySide6.QtWidgets import QMessageBox
        index = self.ui.tableView_4.currentIndex()
        if not index.isValid():
            QMessageBox.warning(
                self, "Aviso", "Selecione uma linha na tabela para excluir.")
            return

        id_selecionado = self.ui.tableView_4.model().item(index.row(), 0).text()
        botao = QMessageBox.question(
            self, "Confirmar Remoção",
            f"Deseja realmente remover o registro do visitante ID {id_selecionado}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if botao == QMessageBox.Yes:
            self.model.deletarVisitante(id_selecionado)
            print(f"Visitante {id_selecionado} removido.")
            self.carregaVisitantes()

    def alterarVisitante(self):
        index = self.ui.tableView_4.currentIndex()
        if not index.isValid():
            QMessageBox.warning(
                self, "Aviso", "Selecione uma linha para alterar.")
            return
        self.ui.tableView_4.edit(index)

    # MÉTODOS DE GERENCIAMENTO (OCORRÊNCIAS)

    def addOcorrencia(self):
        loader = QUiLoader()
        ui_file = QFile("view/addOcorrencia.ui")
        ui_file.open(QFile.ReadOnly)
        self.dialog_ocorrencia = loader.load(ui_file, self)
        ui_file.close()

        self.dialog_ocorrencia.btnSalvar.clicked.connect(
            self.salvar_nova_ocorrencia)
        self.dialog_ocorrencia.btnCancelar.clicked.connect(
            self.dialog_ocorrencia.reject)
        self.dialog_ocorrencia.exec()

    def salvar_nova_ocorrencia(self):
        id_user = self.dialog_ocorrencia.lineEdit.text().strip()
        descricao = self.dialog_ocorrencia.lineEdit_2.text()

        if not descricao:
            QMessageBox.warning(self.dialog_ocorrencia,
                                "Erro", "O campo descrição é obrigatório.")
            return

        sucesso = self.model.inserirOcorrencias(id_user, descricao)
        if sucesso:
            print(f"Ocorrência salva: {descricao}")
            self.dialog_ocorrencia.accept()
            self.carregaOcorrencias()
        else:
            print("Erro na inclusão da ocorrência.")
            self.carregaOcorrencias()

    def excluirOcorrencia(self):
        from PySide6.QtWidgets import QMessageBox
        index = self.ui.tableView_5.currentIndex()
        if not index.isValid():
            QMessageBox.warning(
                self, "Aviso", "Selecione uma linha na tabela para excluir.")
            return

        id_selecionado = self.ui.tableView_5.model().item(index.row(), 0).text()
        botao = QMessageBox.question(
            self, "Confirmar Exclusão",
            f"Deseja realmente excluir a ocorrência ID {id_selecionado}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if botao == QMessageBox.Yes:
            self.model.deletarOcorrencia(id_selecionado)
            print(f"Ocorrência {id_selecionado} excluída.")
            self.carregaOcorrencias()

    def alterarOcorrencia(self):
        index = self.ui.tableView_5.currentIndex()
        if not index.isValid():
            QMessageBox.warning(
                self, "Aviso", "Selecione uma linha para alterar.")
            return
        self.ui.tableView_5.edit(index)

    # MÉTODOS DE EXIBIÇÃO

    def show(self):
        self.ui.show()
