import os


class Estudiante:
    def __init__(self, nombre, apellido, codigo):
        self.nombre = nombre
        self.apellido = apellido
        self.codigo = codigo
        self.notas = {} #diccionario que almacena materias y notas

    def registrar_notas(self, notas_por_materia):
        self.notas.update(notas_por_materia)

    def promedio(self):
        if not self.notas:
            return 0
        return sum(self.notas.values()) / len(self.notas)

    def guardar_en_archivo(self, archivo):
        archivo.write(f"Estudiante: {self.nombre} {self.apellido} (Código: {self.codigo})\n")
        if self.notas:
            archivo.write("Notas:\n")
            for materia, nota in self.notas.items():
                archivo.write(f"  {materia}: {nota}\n")
            archivo.write(f"  Promedio: {self.promedio():.2f}\n")
        else:
            archivo.write("  No tiene notas registradas.\n")
        archivo.write("\n")


class Curso:
    def __init__(self, ruta_archivos):
        self.estudiantes = []
        self.ruta_archivos = ruta_archivos
        # este path es para crear archivos si no existen
        if not os.path.exists(self.ruta_archivos):
            os.makedirs(self.ruta_archivos)

    def registrar_estudiante(self, nombre, apellido, codigo):
        self.estudiantes.append(Estudiante(nombre, apellido, str(codigo)))
        print(f"\nEstudiante '{nombre} {apellido}' (Código: {codigo}) registrado con éxito.\n")
        self.guardar_estudiantes_en_archivo()
        self.limpiar_pantalla()

    def registrar_notas(self, codigo, notas_por_materia):
        for estudiante in self.estudiantes:
            if estudiante.codigo == str (codigo):
                estudiante.registrar_notas(notas_por_materia)
                print(f"\nNotas registradas para {estudiante.nombre} {estudiante.apellido}.\n")
                self.guardar_estudiantes_en_archivo()
                self.limpiar_pantalla()
                return
        print(f"\nEstudiante con código '{codigo}' no encontrado. \n")
        self.limpiar_pantalla()

    def listar_notas(self):
        if not self.estudiantes:
            print("\nNo hay estudiantes registrados.\n")
            self.limpiar_pantalla()
            return
        
        for estudiante in self.estudiantes:
            print(f"\nEstudiante: {estudiante.nombre} {estudiante.apellido} (Código: {estudiante.codigo})")
            if estudiante.notas:
                print("Notas:")
                for materia, nota in estudiante.notas.items():
                    print(f"  {materia}: {nota}")
                print(f"  Promedio: {estudiante.promedio():.2f}")
            else:
                print("  No tiene notas registradas.")
        self.limpiar_pantalla()

    def promedio_grupo(self):
        if not self.estudiantes:
            print("\nNo hay estudiantes registrados.\n")
            self.limpiar_pantalla()
            return 0
        print("\nPromedio general de cada estudiante:")
        promedio_total = 0
        for estudiante in self.estudiantes:
            promedio_estudiante = estudiante.promedio()
            promedio_total += promedio_estudiante
            print(f"  {estudiante.nombre} {estudiante.apellido} (Código: {estudiante.codigo}): {promedio_estudiante:.2f}")
        promedio_total /= len(self.estudiantes)
        print(f"\nPromedio del grupo: {promedio_total:.2f}\n")
        self.guardar_promedio_grupo_en_archivo(promedio_total)
        self.limpiar_pantalla()
        return promedio_total

    def mejor_estudiante(self):
        if not self.estudiantes:
            print("\nNo hay estudiantes registrados.\n")
            self.limpiar_pantalla()
            return None
        estudiantes_ordenados = sorted(self.estudiantes, key=lambda e: e.promedio(), reverse=True)
        #La función sorted() es una función incorporada de Python que devuelve una lista ordenada
        #lambda es una forma de definir funciones pequeñas en una sola línea
        
        print("\n--- Cuadro de Honor ---")
        for i, estudiante in enumerate(estudiantes_ordenados[:3], start=1):
            print(f"  {i}° Lugar: {estudiante.nombre} {estudiante.apellido} (Código: {estudiante.codigo}) - Promedio: {estudiante.promedio():.2f}")
        
        if len(estudiantes_ordenados) < 3:
            print("\nNota: Hay menos de tres estudiantes registrados.")
        
        self.guardar_mejor_estudiante_en_archivo(estudiantes_ordenados[:3])
        self.limpiar_pantalla()
        return estudiantes_ordenados[:3]

    def guardar_estudiantes_en_archivo(self):
        archivo_path = os.path.join(self.ruta_archivos, "estudiantes.txt")  
        with open(archivo_path, "w") as archivo:
            for estudiante in self.estudiantes:
                estudiante.guardar_en_archivo(archivo)

    def guardar_promedio_grupo_en_archivo(self, promedio_total):
        archivo_path = os.path.join(self.ruta_archivos, "promedio_grupo.txt")  
        with open(archivo_path, "w") as archivo:
            archivo.write(f"Promedio del grupo: {promedio_total:.2f}\n")

    def guardar_mejor_estudiante_en_archivo(self, mejores_estudiantes):
        archivo_path = os.path.join(self.ruta_archivos, "cuadro_de_honor.txt")  
        with open(archivo_path, "w") as archivo:
            archivo.write("\n--- Cuadro de Honor ---\n")
            for i, estudiante in enumerate(mejores_estudiantes, start=1):
                archivo.write(f"  {i}° Lugar: {estudiante.nombre} {estudiante.apellido} (Código: {estudiante.codigo}) - Promedio: {estudiante.promedio():.2f}\n")

    def limpiar_pantalla(self):
        input("\nPresiona cualquier tecla para continuar...")
        os.system('cls' if os.name == 'nt' else 'clear')

# Menu
def menu():
    ruta_archivos = "D:\LPPSENA\Proyecto"  # cambien esto por la ruta donde vamos a correr el .py
    curso = Curso(ruta_archivos)
    while True:
        print("¡Bienvenido al sistema de gestión escolar!")
        print("--------------Academix v1.0--------------\n")
        print("Por favor, elige una opción:\n")
        print("1. Registrar estudiante")
        print("2. Registrar notas")
        print("3. Listar notas")
        print("4. Promedio del grupo")
        print("5. Mejor estudiante")
        print("6. Salir\n")
        
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            while True:
                nombre = input("\nIngrese el nombre del estudiante: ").strip()
                if not nombre:
                    print("¡El nombre no puede estar vacío! Intente nuevamente.")
                    continue
                
                apellido = input("Ingrese el apellido del estudiante: ").strip()
                if not apellido:
                    print("¡El apellido no puede estar vacío! Intente nuevamente.")
                    continue
                
                try:
                    codigo = int(input("Ingrese el código estudiantil (solo números): ").strip())
                except ValueError:
                    print("\n¡El código debe ser un número! Intente nuevamente.")
                    continue
                
                # Verificar si el código ya existe
                if any(estudiante.codigo == str(codigo) for estudiante in curso.estudiantes):
                    print(f"\n¡El código {codigo} ya está registrado! Intente con otro código.")
                    continue
                
                
                curso.registrar_estudiante(nombre, apellido, codigo)
                break
        
        elif opcion == "2":
            codigo = input("\nIngrese el código del estudiante: ").strip()
            if not codigo:
                print("\n¡Debe ingresar un código válido!")
                continue
            
            print("Ingrese las notas para las siguientes materias:")
            try:
                notas_por_materia = {
                    "Materia1": float(input("  Materia1: ").strip()),
                    "Materia2": float(input("  Materia2: ").strip()),
                    "Materia3": float(input("  Materia3: ").strip()),
                    "Materia4": float(input("  Materia4: ").strip()),
                    "Materia5": float(input("  Materia5: ").strip()),
                }
            except ValueError:
                print("\n¡Las notas deben ser números! Intente nuevamente.\n")
                continue
            
            curso.registrar_notas(codigo, notas_por_materia)
        
        elif opcion == "3":
            curso.listar_notas()
        
        elif opcion == "4":
            curso.promedio_grupo()
        
        elif opcion == "5":
            curso.mejor_estudiante()
        
        elif opcion == "6":
            print("\n¡Gracias por usar ACADEMIX!\n")
            break
        
        else:
            print("\nOpción inválida. Intente nuevamente.")


if __name__ == "__main__":
    menu()
