import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("postgresql://admin:admin123@localhost:5432/data_quality")

print("\nConectando a PostgreSQL...")
with engine.connect() as conn:
    # 1. Mostrar tablas existentes
    print("\nTablas en la base de datos:")
    tablas = conn.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema='public'
        ORDER BY table_name;
    """)).fetchall()

    for t in tablas:
        print(f" - {t[0]}")

    # 2. Contar registros por tabla
    print("\nConteo de registros por tabla:")
    tablas_objetivo = [
        "course",
        "state",
        "district",
        "student",
        "answer",
        "student_hobbies",
        "student_favorite_courses"
    ]

    for t in tablas_objetivo:
        try:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {t};")).scalar()
            print(f" - {t}: {count} registros")
        except Exception as e:
            print(f" - {t}: ❌ error → {e}")

    # 3. Verificación de relaciones (vista rápida)
    print("\nVerificación rápida de relaciones:")

    # Estudiantes con estado de nacimiento
    result = conn.execute(text("""
        SELECT s.id, s.name, st.name AS birth_state
        FROM student s
        JOIN state st ON st.id = s.birth_state_id
        LIMIT 5;
    """)).fetchall()

    print("\nEjemplo estudiantes con su estado de nacimiento:")
    for r in result:
        print("   ", r)

    # Estudiantes con distrito
    result = conn.execute(text("""
        SELECT s.id, s.name, d.name AS current_district
        FROM student s
        JOIN district d ON d.id = s.current_district_id
        LIMIT 5;
    """)).fetchall()

    print("\nEjemplo estudiantes con su distrito actual:")
    for r in result:
        print("   ", r)

    # Cursos favoritos
    result = conn.execute(text("""
        SELECT student_id, favorite_course_1_id
        FROM student_favorite_courses
        LIMIT 5;
    """)).fetchall()

    print("\nEjemplo cursos favoritos:")
    for r in result:
        print("   ", r)

    print("\nValidación completa.\n")
