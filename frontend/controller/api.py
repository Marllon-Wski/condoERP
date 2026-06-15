import requests

# ─────────────────────────────────────────────────────────
#  CLIENTE DA API (BACKEND FLASK)
#
#  Centraliza as chamadas HTTP para o backend e já trata o
#  formato padrão de resposta usado em backend/utils/helpers.py:
#
#   sucesso  -> {"sucesso": True,  "dados": <dict ou list>}
#   erro     -> {"sucesso": False, "erro": "mensagem"}
# ─────────────────────────────────────────────────────────

BASE_URL = "http://10.28.0.127:5000"
TIMEOUT = 5  # segundos


class ApiClient:
    """Pequeno wrapper sobre requests para falar com a API do backend."""

    @staticmethod
    def _tratar_resposta(resp):
        try:
            payload = resp.json()
        except ValueError:
            return {
                "sucesso": False,
                "erro": "Resposta inválida do servidor (não é JSON).",
                "dados": None,
            }

        # garante que a chave "dados" sempre exista, mesmo em erro
        payload.setdefault("dados", None)
        payload.setdefault("sucesso", resp.ok)
        return payload

    @classmethod
    def _request(cls, metodo, endpoint, **kwargs):
        url = f"{BASE_URL}{endpoint}"
        try:
            resp = requests.request(metodo, url, timeout=TIMEOUT, **kwargs)
        except requests.exceptions.ConnectionError:
            return {
                "sucesso": False,
                "erro": "Não foi possível conectar ao servidor (backend offline?).",
                "dados": None,
            }
        except requests.exceptions.Timeout:
            return {
                "sucesso": False,
                "erro": "O servidor demorou demais para responder.",
                "dados": None,
            }
        except requests.exceptions.RequestException as e:
            return {"sucesso": False, "erro": str(e), "dados": None}

        return cls._tratar_resposta(resp)

    @classmethod
    def get(cls, endpoint):
        return cls._request("GET", endpoint)

    @classmethod
    def post(cls, endpoint, dados):
        return cls._request("POST", endpoint, json=dados)

    @classmethod
    def put(cls, endpoint, dados):
        return cls._request("PUT", endpoint, json=dados)

    @classmethod
    def delete(cls, endpoint):
        return cls._request("DELETE", endpoint)
