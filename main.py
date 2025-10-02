from app import app
from app.db import db

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# Rodar com ( python main.py ) dar pip install em Flask, Flask-login, e Flask-SqlAlchemy

# Email Teste: silvanno198@gmail.com
# Senha Teste: Silvanno198.

# Email Teste: roberto1@gmail.com
# Senha Teste: Rroberto1.