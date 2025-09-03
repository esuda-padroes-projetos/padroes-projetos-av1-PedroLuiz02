from app import app
from app.db import db

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# Rodar com ( python main.py )
#email: teste@gmail.com
#senha: 123456