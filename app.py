from flask import Flask, request, redirect
import string, random

app = Flask(__name__)

# Dicionário em memória para armazenar os links
urls = {}

def gerar_codigo(tamanho=6):
    """Gera um código aleatório com letras e números."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=tamanho))

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url_original = request.form["url"]
        codigo = gerar_codigo()
        urls[codigo] = url_original
        
        # Cria o link encurtado sem barras extras
        link_encurtado = request.host_url.rstrip("/") + "/" + codigo
        return f"""
            <h2>Seu MiniLink 🚀</h2>
            <p><a href='{link_encurtado}'>{link_encurtado}</a></p>
            <a href='/'>Encurtar outro link</a>
        """
    
    # Página inicial
    return """
        <h2>MiniLink - Encurtador de URLs 🚀</h2>
        <form method="post">
            <input type="text" name="url" placeholder="Cole seu link aqui" style="width:300px" required/>
            <button type="submit">Encurtar</button>
        </form>
    """

@app.route("/<codigo>")
def redirecionar(codigo):
    url_original = urls.get(codigo)
    if url_original:
        return redirect(url_original)
    return "<h3>MiniLink não encontrado 😢</h3>", 404

if __name__ == "__main__":
    app.run(debug=True)
