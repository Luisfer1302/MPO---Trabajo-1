
import json
import os
import threading

class TimeoutInput:
    def __init__(self, timeout):
        self.timeout = timeout
        self.answer = None

    def _get_input(self):
        self.answer = input(f"Tu respuesta (A, B, C, D) - tienes {self.timeout} segundos: ").strip().upper()

    def get(self):
        thread = threading.Thread(target=self._get_input)
        thread.start()
        thread.join(timeout=self.timeout)
        if thread.is_alive():
            print("\n⏰ Tiempo agotado.")
            return None
        return self.answer if self.answer.upper() in ["A", "B", "C", "D"] else None

def cargar_preguntas():
    try:
        with open("preguntas.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("❌ Error al cargar preguntas:", e)
        return []

def filtrar_preguntas(preguntas, tema, dificultad):
    return [p for p in preguntas if p["tema"] == tema and p["dificultad"] == dificultad]

def mostrar_pregunta(pregunta_dict):
    print("\n" + pregunta_dict["pregunta"])
    for opcion in pregunta_dict["opciones"]:
        print(opcion)

def corregir_respuesta(respuesta, correcta):
    return respuesta.upper() == correcta.upper()

def mostrar_resultados(aciertos, total):
    porcentaje = (aciertos / total) * 100
    print("\n### RESULTADOS ###")
    print(f"Total de preguntas: {total}")
    print(f"Aciertos: {aciertos}")
    print(f"Porcentaje: {porcentaje:.2f}%")
    if porcentaje == 100:
        print("🏆 ¡Perfecto! ¡Excelente trabajo!")
    elif porcentaje >= 80:
        print("🎉 ¡Muy bien!")
    elif porcentaje >= 50:
        print("🙂 Bien, pero puedes mejorar.")
    else:
        print("📚 Necesitas practicar más.")
    return porcentaje

def guardar_en_ranking(nombre, puntuacion):
    with open("ranking.txt", "a", encoding="utf-8") as f:
        f.write(f"{nombre},{puntuacion:.2f}\n")

def mostrar_ranking():
    print("\n### RANKING ###")
    if not os.path.exists("ranking.txt"):
        print("Aún no hay resultados.")
        return
    with open("ranking.txt", "r", encoding="utf-8") as f:
        datos = [line.strip().split(",") for line in f.readlines()]
        datos_ordenados = sorted(datos, key=lambda x: float(x[1]), reverse=True)
        for i, (nombre, puntuacion) in enumerate(datos_ordenados, 1):
            print(f"{i}. {nombre} - {puntuacion}%")

def obtener_opciones_validas(lista, tipo):
    print(f"\nOpciones de {tipo}:")
    opciones = sorted(set(lista))
    for i, val in enumerate(opciones, 1):
        print(f"{i}. {val}")
    while True:
        seleccion = input(f"Selecciona una opción de {tipo} (número): ").strip()
        if seleccion.isdigit() and 1 <= int(seleccion) <= len(opciones):
            return opciones[int(seleccion) - 1]
        else:
            print("❌ Opción no válida.")

def elegir_tiempo_limite():
    tiempos = [5, 10, 15, 20]
    print("\nOpciones de tiempo límite por pregunta:")
    for i, t in enumerate(tiempos, 1):
        print(f"{i}. {t} segundos")
    while True:
        seleccion = input("Selecciona una opción de tiempo (número): ").strip()
        if seleccion.isdigit() and 1 <= int(seleccion) <= len(tiempos):
            return tiempos[int(seleccion) - 1]
        else:
            print("❌ Opción no válida.")

def empezar_cuestionario():
    nombre = input("\nIntroduce tu nombre: ").strip()
    todas_las_preguntas = cargar_preguntas()
    if not todas_las_preguntas:
        return

    temas = [p["tema"] for p in todas_las_preguntas]
    dificultad = [p["dificultad"] for p in todas_las_preguntas]

    tema_seleccionado = obtener_opciones_validas(temas, "tema")
    dificultad_seleccionada = obtener_opciones_validas(dificultad, "dificultad")
    tiempo_limite = elegir_tiempo_limite()

    preguntas = filtrar_preguntas(todas_las_preguntas, tema_seleccionado, dificultad_seleccionada)
    if not preguntas:
        print("❌ No hay preguntas para esa combinación.")
        return

    aciertos = 0
    for pregunta in preguntas:
        mostrar_pregunta(pregunta)
        respuesta = TimeoutInput(tiempo_limite).get()
        if respuesta is None:
            print(f"❌ Respuesta correcta: {pregunta['respuesta_correcta']}")
            continue
        if corregir_respuesta(respuesta, pregunta["respuesta_correcta"]):
            print("✅ ¡Correcto!")
            aciertos += 1
        else:
            print(f"❌ Incorrecto. Respuesta correcta: {pregunta['respuesta_correcta']}")

    puntuacion = mostrar_resultados(aciertos, len(preguntas))
    guardar_en_ranking(nombre, puntuacion)

def menu():
    while True:
        print("\n### MENÚ ###")
        print("1 - Empezar cuestionario")
        print("2 - Ver ranking")
        print("3 - Salir")
        opcion = input("Selecciona una opción: ").strip()
        if opcion == "1":
            empezar_cuestionario()
        elif opcion == "2":
            mostrar_ranking()
        elif opcion == "3":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida.")

if __name__ == "__main__":
    menu()
