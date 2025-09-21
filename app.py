from flask import Flask, request, redirect, render_template_string
import string, random

app = Flask(__name__)

# Dicionário para guardar os links (em memória por enquanto)
urls = {}

def gerar_codigo(tamanho=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=tamanho))

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url_original = request.form["url"]
        codigo = gerar_codigo()
        urls[codigo] = url_original
        link_encurtado = request.host_url + codigo
        return f"Seu MiniLink: <a href='{link_encurtado}'>{link_encurtado}</a>"
    
    return """
        <h2>MiniLink - Encurtador de URLs 🚀</h2>
        <form method="post">
            <input type="text" name="url" placeholder="Cole seu link aqui" style="width:300px"/>
            <button type="submit">Encurtar</button>
        </form>
    """

@app.route("/<codigo>")
def redirecionar(codigo):
    url_original = urls.get(codigo)
    if url_original:
        return redirect(url_original)
    return "MiniLink não encontrado 😢", 404
