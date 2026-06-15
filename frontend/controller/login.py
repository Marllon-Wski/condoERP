from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from condoERP.frontend.model.login import LoginModel
from condoERP.frontend.controller.home import HomeController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_file = QFile("view/login.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.model = LoginModel()

        self.ui.stackedWidget.setCurrentIndex(0)
        self.conectar_botoes()

    def conectar_botoes(self):
        self.ui.pushButton.clicked.connect(self.login)
        self.ui.pushButton_2.clicked.connect(self.abrir_cadastro)

        self.ui.pushButton_3.clicked.connect(self.cadastrar)
        self.ui.pushButton_4.clicked.connect(self.abrir_login)

    def abrir_cadastro(self):
        # função que abre a aba de cadastro
        self.ui.stackedWidget.setCurrentIndex(1)

    def abrir_login(self):
        # função que abre a aba de login
        self.ui.stackedWidget.setCurrentIndex(0)

    def login(self):
        # função para verificar senha/usuário no banco e depois passar para a próxima tela
        # .strip() é apenas uma função para tirar espaços ou valores vazios.
        login = self.ui.lineEdit.text().strip()
        senha = self.ui.lineEdit_2.text().strip()

        if not login or not senha:
            QMessageBox.warning(self.ui, "Erro de Validação",
                                "Todos os campos devem ser preenchidos!")
            print("Cadastro barrado: Existem campos vazios.")
            return  # quebra da função

        v = self.model.loginVerify(login, senha)

        if v:
            # carrega a home
            self.home_window = HomeController(tacesso=v)
            self.home_window.show()
            self.ui.close()
        else:
            QMessageBox.critical(self.ui, "Erro de Login",
                                 "Usuário ou senha incorretos.")
            print("Erro no Login.")

        # fazer um verificador do fetchall onde se a consulta der vazio, barrar o login, se não, entrar.

    def cadastrar(self):
        nome = self.ui.lineEdit_3.text().strip()
        email = self.ui.lineEdit_4.text().strip()
        tel = self.ui.lineEdit_5.text().strip()
        cpf = self.ui.lineEdit_6.text().strip()
        data = self.ui.dateEdit.date().toString("yyyy-MM-dd")
        senha = self.ui.lineEdit_7.text().strip()
        csenha = self.ui.lineEdit_8.text().strip()
        opcao = self.ui.comboBox.currentText().strip()

        # verificação extensa de campos vazios
        if not nome or not email or not tel or not cpf or not data or not senha or not csenha:
            QMessageBox.warning(self.ui, "Erro de Validação",
                                "Todos os campos devem ser preenchidos!")
            print("Cadastro barrado: Existem campos vazios.")
            return  # quebra da função, barramento

        if senha != csenha:  # verificação para os campos de senha
            print("As senhas devem coinscindir.")
            return

        if "Morador" in opcao:
            tacesso = "morador"
        elif "Visitante" in opcao:
            tacesso = "visitante"

        v = self.model.newLogin(nome, email, tel, cpf, data, senha, tacesso)

        if v:  # verificação de inclusão de cadastro
            QMessageBox.information(
                self.ui, "Sucesso", "Cadastro realizado com sucesso!")
            print("Login novo!")
            self.abrir_login()
        else:
            QMessageBox.critical(
                self.ui, "Erro", "Não foi possível realizar o cadastro no banco de dados.")
            print("Login não deu certo :(")

        i = self.model.acessVerify(tacesso)

    def show(self):
        self.ui.show()
