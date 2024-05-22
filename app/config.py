import os


class Config:
    # Define o caminho absoluto para o diretório onde o banco de dados será salvo
    DB_DIR = "C:\\Users\\mathe\\Documents\\Github\\SLA\\app"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key"
    # Inclui o caminho absoluto na URI do banco de dados
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or f"sqlite:///{DB_DIR}/service_calls.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
