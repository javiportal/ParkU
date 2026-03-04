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

        # Create admin user if doesn't exist
        admin_email = "admin@parku.edu.sv"
        existing_admin = db.query(Usuario).filter(Usuario.email == admin_email).first()
        if not existing_admin:
            rol_admin = db.query(Rol).filter(Rol.nombre == "administrador").first()
            admin = Usuario(
                nombre="Admin ParkU",
                email=admin_email,
                contrasena=hash_password("admin123"),
                rol_id=rol_admin.id,
            )
            db.add(admin)
            db.commit()
            print(f"  Usuario admin creado: {admin_email} / admin123")

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
