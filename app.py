from flask import Flask, request, redirect
import sqlite3
import string, random

app = Flask(__name__)
DB_NAME = "minilink.db"

# Inicializa o banco de dados
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS links (
            codigo TEXT PRIMARY KEY,
            url_original TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Gera código curto
def gerar_codigo(tamanho=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=tamanho))

# Inserir link no banco
def salvar_link(codigo, url):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO links (codigo, url_original) VALUES (?, ?)", (codigo, url))
    conn.commit()
    conn.close()

# Buscar link no banco
def buscar_link(codigo):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT url_original FROM links WHERE codigo = ?", (codigo,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

# Inicializa DB ao iniciar o app
init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url_original = request.form["url"]
        codigo = gerar_codigo()
        salvar_link(codigo, url_original)
        link_encurtado = request.host_url.rstrip("/") + "/" + codigo
        return f"""
            <h2>Seu MiniLink 🚀</h2>
            <p><a href='{link_encurtado}'>{link_encurtado}</a></p>
            <a href='/'>Encurtar outro link</a>
        """
    
    return """
        <h2>MiniLink - Encurtador de URLs 🚀</h2>
        <form method="post">
            <input type="text" name="url" placeholder="Cole seu link aqui" style="width:300px" required/>
            <button type="submit">Encurtar</button>
        </form>
    """

@app.route("/<codigo>")
def redirecionar(codigo):
    url_original = buscar_link(codigo)
    if url_original:
        return redirect(url_original)
    return "<h3>MiniLink não encontrado 😢</h3>", 404

if __name__ == "__main__":
    app.run(debug=True)
