"""
Seed script: creates database tables and initial data.

Usage: python -m app.seed
"""
from app.database import engine, Base, SessionLocal
from app.usuarios.models import Rol, Usuario
from app.vehiculos.models import Vehiculo
from app.parqueo.models import Parqueo
from app.movimientos.models import Movimiento
from app.auth.service import hash_password


def seed():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente.")

    db = SessionLocal()
    try:
        # Create roles if they don't exist
        roles_nombres = ["administrador", "vigilante", "estudiante"]
        for nombre in roles_nombres:
            existing = db.query(Rol).filter(Rol.nombre == nombre).first()
            if not existing:
                db.add(Rol(nombre=nombre))
                print(f"  Rol '{nombre}' creado.")
        db.commit()

        # Create default users if they don't exist
        usuarios_seed = [
            {
                "nombre": "Admin ParkU",
                "email": "admin@parku.edu.sv",
                "contrasena": "admin123",
                "rol": "administrador",
            },
            {
                "nombre": "Vigilante ParkU",
                "email": "vigilante@parku.edu.sv",
                "contrasena": "vigilante123",
                "rol": "vigilante",
            },
        ]
        for usuario_seed in usuarios_seed:
            existing_user = (
                db.query(Usuario)
                .filter(Usuario.email == usuario_seed["email"])
                .first()
            )
            if existing_user:
                continue

            rol = db.query(Rol).filter(Rol.nombre == usuario_seed["rol"]).first()
            usuario = Usuario(
                nombre=usuario_seed["nombre"],
                email=usuario_seed["email"],
                contrasena=hash_password(usuario_seed["contrasena"]),
                rol_id=rol.id,
            )
            db.add(usuario)
            db.commit()
            print(
                "  Usuario creado: "
                f"{usuario_seed['email']} / {usuario_seed['contrasena']} "
                f"({usuario_seed['rol']})"
            )

        # Create default parking lot if doesn't exist
        existing_parqueo = db.query(Parqueo).first()
        if not existing_parqueo:
            parqueo = Parqueo(
                nombre="Parqueo Principal ESEN",
                cupos_maximos=150,
            )
            db.add(parqueo)
            db.commit()
            print(f"  Parqueo '{parqueo.nombre}' creado (150 cupos).")

        print("\nSeed completado exitosamente.")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
