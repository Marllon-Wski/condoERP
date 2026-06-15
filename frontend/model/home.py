from condoERP.frontend.controller.api import ApiClient


class HomeModel:

    # Encomendas

    def selectEncomendas(self):
        resposta = ApiClient.get("/encomendas")

        if not resposta.get("sucesso"):
            print("Erro ao buscar encomendas:", resposta.get("erro"))
            return []

        return resposta.get("dados") or []

    def inserirEncomendas(self, id_usuario, descricao, data_entrega):
        resposta = ApiClient.post("/encomendas", {
            "id_usuario": id_usuario,
            "descricao": descricao,
            "data_entrega": data_entrega,
        })

        if not resposta.get("sucesso"):
            print("Erro ao inserir encomenda:", resposta.get("erro"))
            return False

        return True

    def deletarEncomenda(self, id):
        resposta = ApiClient.delete(f"/encomendas/{id}")
        if not resposta.get("sucesso"):
            print("Erro ao deletar encomenda:", resposta.get("erro"))
            return False
        return True

    # Notificações

    def buscarNotificacoes(self):
        resposta = ApiClient.get("/notificacoes")

        if not resposta.get("sucesso"):
            print("Erro ao buscar notificações:", resposta.get("erro"))
            return []

        return resposta.get("dados") or []

    def inserirNotificacao(self, id_usuario, descricao):
        resposta = ApiClient.post("/notificacoes", {
            "id_usuario": id_usuario,
            "descricao": descricao,
        })

        if not resposta.get("sucesso"):
            print("Erro ao inserir notificação:", resposta.get("erro"))
            return False

        return True

    def deletarNotificacao(self, id):
        resposta = ApiClient.delete(f"/notificacoes/{id}")
        if not resposta.get("sucesso"):
            print("Erro ao deletar notificação:", resposta.get("erro"))
            return False
        return True

    # Veículos

    def buscarVeiculos(self):
        resposta = ApiClient.get("/veiculos")

        if not resposta.get("sucesso"):
            print("Erro ao buscar veículos:", resposta.get("erro"))
            return []

        return resposta.get("dados") or []

    def inserirVeiculos(self, id_usuario, placa, descricao, documento):
        resposta = ApiClient.post("/veiculos", {
            "id_usuario": id_usuario,
            "placa": placa,
            "descricao": descricao,
            "documento": documento,
        })

        if not resposta.get("sucesso"):
            print("Erro ao inserir veículo:", resposta.get("erro"))
            return False

        return True

    def deletarVeiculo(self, id):
        resposta = ApiClient.delete(f"/veiculos/{id}")
        if not resposta.get("sucesso"):
            print("Erro ao deletar veículo:", resposta.get("erro"))
            return False
        return True

    # Visitntes

    def buscarVisitantes(self):
        resposta = ApiClient.get("/visitantes")

        if not resposta.get("sucesso"):
            print("Erro ao buscar visitantes:", resposta.get("erro"))
            return []

        return resposta.get("dados") or []

    def inserirVisitantes(self, id_user, id_veiculo, id_vaga, id_morador):
        resposta = ApiClient.post("/visitantes", {
            "id_user": id_user,
            "id_veiculo": id_veiculo,
            "id_vaga": id_vaga,
            "id_morador": id_morador,
        })

        if not resposta.get("sucesso"):
            print("Erro ao inserir visitante:", resposta.get("erro"))
            return False

        return True

    def deletarVisitante(self, id):
        resposta = ApiClient.delete(f"/visitantes/{id}")
        if not resposta.get("sucesso"):
            print("Erro ao deletar visitante:", resposta.get("erro"))
            return False
        return True

    # Ocorrências

    def buscarOcorrencias(self):
        resposta = ApiClient.get("/ocorrencias")

        if not resposta.get("sucesso"):
            print("Erro ao buscar ocorrências:", resposta.get("erro"))
            return []

        return resposta.get("dados") or []

    def inserirOcorrencias(self, id_usuario, descricao):
        resposta = ApiClient.post("/ocorrencias", {
            "id_usuario": id_usuario,
            "descricao": descricao,
        })

        if not resposta.get("sucesso"):
            print("Erro ao inserir ocorrência:", resposta.get("erro"))
            return False

        return True

    def deletarOcorrencia(self, id):
        resposta = ApiClient.delete(f"/ocorrencias/{id}")
        if not resposta.get("sucesso"):
            print("Erro ao deletar ocorrência:", resposta.get("erro"))
            return False
        return True
