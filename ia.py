import requests
from config import HF_TOKEN
#Hemos usado aqui la IA porque no sabiamos como conectar la IA con la aplicacion.
API_URL = "https://router.huggingface.co/sambanova/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}


def _llamar_ia(prompt, max_tokens=300):
    try:
        r = requests.post(API_URL, headers=HEADERS, timeout=30, json={
            "model": "Meta-Llama-3.3-70B-Instruct",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens
        })

        if r.status_code == 503: return " El modelo está cargando, espera 20 segundos."
        if r.status_code == 401: return " Token inválido. Revisa tu .env"
        if r.status_code != 200: return f" Error {r.status_code}: {r.text[:200]}"

        return r.json()['choices'][0]['message']['content'].strip()

    except requests.exceptions.Timeout:
        return " La IA tardó demasiado. Inténtalo de nuevo."
    except Exception as e:
        return f" Error: {e}"


def sugerir_receta(ingrediente, nutriscore):
    prompt = f"""Eres un dietista experto. El usuario tiene "{ingrediente}" con nutriscore {nutriscore}.
    Sugiere UNA receta saludable con nombre, ingredientes y preparación en 3 pasos. Responde en español."""
    return _llamar_ia(prompt, max_tokens=300)
