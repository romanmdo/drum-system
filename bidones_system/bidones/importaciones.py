import pandas
import PyPDF2
from datetime import datetime
from .models import Alumno, Profesor, Materia, Calificaciones, Curso

def importar_calificaciones(archivo):
    parser = {
        'AMS': 10.0, # Aprobado Muy Satisfactoriamente
        'A': 8.0,    # Aprobado
        'EP': 6.0    # En Proceso
    }

    logs = []

    df = pandas.read_excel(archivo, engine='openpyxl')
    for _, row in df.iterrows():
        nota = parser.get(row['nota'].upper(), None)
        if nota is None:
            nota = float(row['nota'])
        final = row['final'].lower() == 'si'
        fecha = row['fecha']

        alumno = None
        try:
            alumno = Alumno.objects.get(dni=int(row['alumno_dni']))
        except:
            logs.append(f'EL ALUMNO CON DNI \'{row["alumno_dni"]}\' NO ESTÁ EN LOS REGISTROS')
            continue

        profesor = None
        try:
            profesor = Profesor.objects.get(dni=int(row['profesor_dni']))
        except:
            logs.append(f'EL PROFESOR CON DNI \'{row["profesor_dni"]}\' NO ESTÁ EN LOS REGISTROS')
            continue

        materia = None
        try:
            materia = Materia.objects.get(nombre=row['materia'], curso=alumno.curso)
        except:
            logs.append(f'LA MATERIA \'{row["materia"]}\' NO ESTÁ EN LOS REGISTROS')
            continue

        curso = alumno.curso

        # Crear la calificación.
        calificacion = Calificaciones.objects.create(
            nota=nota,
            final=final,
            fecha=fecha,
            alumno=alumno,
            profesor=profesor,
            materia=materia,
            curso=curso
        )
        calificacion.save()

        print(f'Se creó la calificación con el ID {calificacion.id}.')

    if logs:
        logs.append('LAS CALIFICACIONES FUERON CARGADAS CON ALGUNAS EXCEPCIONES')
    else:
        logs.append('LAS CALIFICACIONES FUERON CARGADAS CON ÉXITO')
    return logs

def importar_materias(archivo):
    df = pandas.read_excel(archivo, engine='openpyxl')
    for _, row in df.iterrows():
        nombre = row['materia']
        horas = row['horas_catedra']
        curso = Curso.objects.get(anio=int(row['curso']))
        profesor = Profesor.objects.get(dni=int(row['profesor_dni']))

        # Crear la materia.
        materia = Materia.objects.create(
            nombre=nombre,
            horas_catedra=horas,
            curso=curso,
            profesor=profesor
        )
        materia.save()

        print(f'Se creó la materia {nombre}.')

def importar_profesores(archivo):
    df = pandas.read_excel(archivo, engine='openpyxl')
    for _, row in df.iterrows():
        dni = int(row['dni'])
        nombre = row['nombre']
        apellido = row['apellido']
        telefono = row.get('telefono', default='')
        email = row['email']

        # Crear o actualizar el profesor.
        profesor, creado = Profesor.objects.update_or_create(
            dni=dni,
            defaults={
                'nombre': nombre,
                'apellido': apellido,
                'telefono': telefono,
                'email': email
            }
        )

        if creado:
            print(f'Se creó el profesor {nombre} {apellido}.')
        else:
            print(f'Se actualizó el profesor {nombre} {apellido}.')

def importar_alumnos(archivo):
    logs = []

    df = pandas.read_excel(archivo, engine='openpyxl')
    for _, row in df.iterrows():
        dni = int(row['dni'])
        nombre = row['nombre']
        apellido = row['apellido']
        fecha_nacimiento = row.get('fecha_nacimiento', default=None)
        if type(fecha_nacimiento) == float:
            fecha_nacimiento = None
        email = row['email']
        curso = Curso.objects.get(anio=int(row['curso']))

        # Crear o actualizar el alumno.
        alumno, creado = Alumno.objects.update_or_create(
            dni=dni,
            defaults={
                'nombre': nombre,
                'apellido': apellido,
                'fecha_nacimiento': fecha_nacimiento,
                'email': email,
                'repitio': 0,
                'curso': curso
            }
        )

        if not creado:
            logs.append(f'SE ACTUALIZÓ A "{nombre} {apellido}" CON DNI "{dni}"')

    logs.append('LOS ALUMNOS FUERON CARGADOS CON ÉXITO')
    return logs

# Código para importar los alumnos por los PDF asquerosos del CIDI (PROPENSO A FALLOS, NO CONFÍEN).
def importar_alumnos_pdf(pdf):
    logs = []

    parser = {
        'PRIMER': 1,
        'SEGUNDO': 2,
        'TERCER': 3,
        'CUARTO': 4,
        'QUINTO': 5,
        'SEXTO': 6
    }

    reader = PyPDF2.PdfReader(pdf) # Lector de PDF.
    for page in reader.pages:
        content = page.extract_text()
        pos = content.index('Nombres Estado')+15

        parts = content[pos::].split('\n')
        for part in parts:
            try:
                data = part.split(' ')
                grade = parser[data[0]]
                dni = int(data[4])
                fullname = ' '.join(data[6:-1]).split(',')
                lastname = fullname[0]
                name = fullname[1][1::]

                curso = Curso.objects.get(anio=grade)
                alumno, creado = Alumno.objects.update_or_create(
                    dni=dni,
                    defaults={
                        'nombre': name,
                        'apellido': lastname,
                        'fecha_nacimiento': None,
                        'email': '',
                        'repitio': False,
                        'curso': curso
                    }
                )

                if not creado:
                    logs.append(f'SE ACTUALIZÓ A "{name} {lastname}" CON DNI "{dni}"')
            except:
                pass

    logs.append('LOS ALUMNOS FUERON CARGADOS CON ÉXITO')
    return logs

# Código que hice a las apuradas para leer las calificaciones desde un PDF.
def importar_calificaciones_pdf(pdf):
    reader = PyPDF2.PdfReader(pdf) # Lector de PDF.
    content = reader.pages[0].extract_text() # Se extrae todo el contenido del PDF.
    pos = content.index('Curso:')

    # Obtener el nombre de la materia.
    subject = [] # Acá se va a ir guardando el nombre de la materia al revés.
    i = pos-1
    while content[i] != ':':
        subject.append(content[i])
        i -= 1
    subject.pop() # Eliminar espacio en blanco.
    subject.reverse() # Se da vuelta la palabra para que quede normal.
    subject = ''.join(subject)

    # Obtener el curso.
    grade = ''
    i = pos+7
    while content[i] != ' ':
        grade += content[i]
        i += 1

    parser = {
        'PRIMER': 1,
        'SEGUNDO': 2,
        'TERCER': 3,
        'CUARTO': 4,
        'QUINTO': 5,
        'SEXTO': 6
    }

    # Registro de errores al cargar las calificaciones.
    logs = []

    curso = Curso.objects.get(anio=parser[grade])
    materia = None
    try:
        materia = Materia.objects.get(nombre=subject, curso=curso)
    except:
        logs.append('ERROR AL CARGAR LAS CALIFICACIONES')
        logs.append(f'LA MATERIA "{subject}" NO EXISTE')
        return logs

    # Obtener los alumnos y sus notas.
    parts = content.split('\n')
    i = parts.index('Final')+1
    for current in parts[i::]:
        # Obtener el apellido del alumno.
        lastname = ''
        k = 0
        while current[k] != ',':
            lastname += current[k]
            k += 1

        # Obtener el nombre del alumno.
        name = ''
        k += 2
        while not current[k].isdigit():
            name += current[k]
            k += 1

        alumno = None
        try:
            alumno = Alumno.objects.get(nombre=name, apellido=lastname, curso=curso)
        except:
            logs.append(f'"{name} {lastname}" NO SE ENCONTRÓ EN LOS REGISTROS')
            continue

        # Obtener notas.
        grades = current[k::].split(' ')
        for n in grades:
            nota = None
            if len(n) > 1:
                if n[-1] == '0':
                    nota = 10.0
                else:
                    nota = float(n[-1])
            else:
                nota = float(n)

            Calificaciones.objects.create(
                alumno=alumno,
                curso=curso,
                materia=materia,
                profesor=materia.profesor,
                fecha=datetime.today(),
                nota=nota,
                final=False
            )

    if logs:
        logs.append('LAS CALIFICACIONES FUERON CARGADAS CON ALGUNAS EXCEPCIONES')
    else:
        logs.append('TODAS LAS CALIFICACIONES FUERON CARGADAS CON ÉXITO')
    return logs