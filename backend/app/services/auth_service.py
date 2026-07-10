from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.utils.security import verify_password
from backend.app.utils.jwt import create_access_token


def login(db: Session, username: str, password: str):
    user = (
        db.query(User)
        .filter(
                or_(
                    User.username == username,
                      User.email == username,
                     )
            )
        .first()
)

    if not user:
        return None

    if not user.status_aktif:
        return None

    if not verify_password(password, user.password_hash):
        return None

    token = create_access_token(
        {
            "sub": str(user.id_user),
            "username": user.username,
            "role": user.role.nama_role.lower(),
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role.nama_role.lower(),
        "user": {
            "id_user": user.id_user,
            "username": user.username,
            "email": user.email,
            "role": user.role.nama_role.lower(),
        },
    }