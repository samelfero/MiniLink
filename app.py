from flask import Flask, request, redirect
import psycopg2
import string, random
import os

app = Flask(__name__)

# URL do banco Postgres (Render)
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgres://minilink_db_user:7EzUbTw8yZvf6sihPQDEByChsXckvMFU@dpg-d38976p5pdvs738d577g-a:5432/minilink_db"
)

# Inicializa o banco
def init_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS links (
                codigo VARCHAR(10) PRIMARY KEY,
                url_original TEXT NOT NULL
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Banco de dados inicializado com sucesso!")
    except Exception as e:
        print("Erro ao inicializar o banco:", e)

# Gera código curto
def gerar_codigo(tamanho=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=tamanho))

# Salvar link
def salvar_link(codigo, url):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("INSERT INTO links (codigo, url_original) VALUES (%s, %s)", (codigo, url))
    conn.commit()
    cur.close()
    conn.close()

# Buscar link
def buscar_link(codigo):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT url_original FROM links WHERE codigo=%s", (codigo,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else None

# Inicializa DB
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
