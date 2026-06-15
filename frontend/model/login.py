from condoERP.frontend.controller.api import ApiClient


class LoginModel:
    def loginVerify(self, login, senha):
        resposta = ApiClient.post("/login/auth", {
            "ilogin": login,
            "senha": senha,
        })

        if not resposta.get("sucesso"):
            print("Erro ao verificar login:", resposta.get("erro"))
            return False

        dados = resposta.get("dados") or {}
        return dados.get("tipo_acesso", False)

    def newLogin(self, nome, email, tel, cpf, data, senha, tacesso):
        payload = {
            "nome": nome,
            "ilogin": email,
            "telefone": tel,
            "cpf": cpf,
            "data_nasc": data,
            "senha": senha,
            "tipo_acesso": tacesso,
        }

        resposta = ApiClient.post("/login", payload)
        if not resposta.get("sucesso"):
            print("Erro ao criar login:", resposta.get("erro"))
            return False

        return True
