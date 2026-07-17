"""
Cria o primeiro usuario administrador do sistema.

Sem isso ninguem consegue fazer login (o endpoint /auth/login exige um
usuario ja existente com senha em hash). Rode uma vez, apos o banco de
dados estar de pe (docker compose up + migracoes aplicadas):

    docker compose run --rm api python scripts/criar_admin.py \
        --nome "Seu Nome" --email voce@exemplo.com --senha "escolha-uma-senha-forte"
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.usuario import Usuario


def main():
    parser = argparse.ArgumentParser(description="Cria o usuario administrador inicial do IFA PRO 2.5")
    parser.add_argument("--nome", required=True)
    parser.add_argument("--email", required=True)
    parser.add_argument("--senha", required=True)
    args = parser.parse_args()

    db = SessionLocal()
    try:
        existente = db.query(Usuario).filter(Usuario.email == args.email).first()
        if existente:
            print(f"Ja existe um usuario com o email {args.email}. Nada foi criado.")
            return

        usuario = Usuario(
            nome=args.nome,
            email=args.email,
            senha_hash=hash_password(args.senha),
            papel="admin",
            ativo=True,
        )
        db.add(usuario)
        db.commit()
        print(f"Usuario admin '{args.nome}' <{args.email}> criado com sucesso.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
