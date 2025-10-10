# Definimos las habitaciones y los items

salon_de_juegos = {"nombre": "salon de juegos", "tipo": "sala"}
dormitorio_1 = {"nombre": "dormitorio 1", "tipo": "sala"}
dormitorio_2 = {"nombre": "dormitorio 2", "tipo": "sala"}
comedor = {"nombre": "comedor", "tipo": "sala"}
exterior = {"nombre": "exterior", "tipo": "sala"}

puerta_a = {"nombre": "puerta a", "tipo": "puerta"}
puerta_b = {"nombre": "puerta b", "tipo": "puerta"}
puerta_c = {"nombre": "puerta c", "tipo": "puerta"}
puerta_d = {"nombre": "puerta d", "tipo": "puerta"}

llave_a = {"nombre": "llave para puerta a", "tipo": "llave", "objetivo": "puerta a"}
llave_b = {"nombre": "llave para puerta b", "tipo": "llave", "objetivo": "puerta b"}
llave_c = {"nombre": "llave para puerta c", "tipo": "llave", "objetivo": "puerta c"}
llave_d = {"nombre": "llave para puerta d", "tipo": "llave", "objetivo": "puerta d"}

piano = {"nombre": "piano","tipo": "mobiliario"}
sofá = {"nombre": "sofá","tipo": "mobiliario"}
cama_de_matrimonio = {"nombre": "cama de matrimonio", "tipo": "mobiliario"}
cama_doble = {"nombre": "cama doble", "tipo": "mobiliario"}
vestidor = {"nombre": "vestidor", "tipo": "mobiliario"}
mesa_de_comedor = {"nombre": "mesa de comedor", "tipo": "mobiliario"}

objetos_en_sala = {
    "salon de juegos": [sofá, piano, puerta_a],
    "piano": [llave_a],
    "dormitorio 1": [cama_de_matrimonio, puerta_a, puerta_b, puerta_c],
    "cama de matrimonio": [llave_b],
    "dormitorio 2": [cama_doble, vestidor, puerta_b],
    "cama doble": [llave_c],
    "vestidor": [llave_d],
    "comedor": [mesa_de_comedor, puerta_c, puerta_d],
    "exterior": [puerta_d]
}

habitaciones_totales = [salon_de_juegos, dormitorio_1, dormitorio_2, comedor, exterior]
puertas_totales = [puerta_a, puerta_b, puerta_c, puerta_d]
llaves_totales = [llave_a, llave_b, llave_c, llave_d]

INIT_GAME_STATE = {
    "sala_actual": salon_de_juegos,
    "llaves_conseguidas": [],
    "sala_objetivo": exterior
}
def resolver_sala(sala_ref):
    """
    Si sala_ref es un dict, lo devuelve tal cual.
    Si es un str (nombre), busca el dict correspondiente en habitaciones_totales.
    """
    if isinstance(sala_ref, dict):
        return sala_ref
    if isinstance(sala_ref, str):
        for h in habitaciones_totales:
            if h["nombre"] == sala_ref:
                return h
    return None

def salto_linea():
    print("\n" + "🧠💉⏳🔒🚪🗝️  " * 5 + "\n")


def start_game():
    """
    Comenzamos el juego
    """
    print("💀 Despiertas lentamente... un dolor punzante en el cuello, "
          "la cabeza pesada, como si tu cerebro estuviera nadando en miel. "
          "Te das cuenta de que estás tirado en un sofá viejo, en una casa sin ventanas. "
          "Un susurro te llega a los oídos: 'Tienes solo 15 minutos antes de que regresen...' "
          "Necesitas escapar, pero no recuerdas cómo llegaste aquí.")
    salto_linea()
    iniciar_sala(game_state["sala_actual"])


def iniciar_sala(sala):
    """
    Inicia una habitación. Comprueba la sala objetivo y ofrece opciones al jugador.
    """
    sala = resolver_sala(sala)
    if sala is None:
        print("Error interno: la sala indicada no existe.")
        return

    game_state["sala_actual"] = sala

    if game_state["sala_actual"] == game_state["sala_objetivo"]:
        print("""🎉 HAS ESCAPADO 🎉
        🧠💉Con cada paso, tu mente vuelve a la realidad...
        🏃 Has logrado sobrevivir a la noche más larga. 😱
        Tus captores ya no te persiguen… por ahora. 🕵️‍♂️
        Pero recuerda: alguien sigue vigilando 👀🔍.
        """)
    else:
        print("Te encuentras ahora en " + sala["nombre"])
        intended_action = input("¿Qué quieres hacer? explorar / examinar / morir / salir: ").strip().lower()

        if intended_action == "salir":
                print("Cobarde...")
                return

        if intended_action == "explorar":
            explorar_sala(sala)
            iniciar_sala(sala)

        elif intended_action == "examinar":
            examine_item(input("Qué te gustaria examinar? ").strip().lower())

        elif intended_action == "morir":
            print("No lo hagas. Recuerda que tienes entradas para Bad Bunny 🎤🐰🔥")
            print("🎶 Se escucha a lo lejos: 'YHLQMDLG...' 🎶")
            iniciar_sala(sala)

        else:
            print("⚠️ Espabila, si sigues así te van a atrapar. Escribe 'explorar' or 'examinar'.")
            iniciar_sala(sala)

        salto_linea()


def explorar_sala(sala):
    """
    Explora una habitación. Lista todos los objetos de esa sala.
    """
    sala = resolver_sala(sala)
    if sala is None:
        print("Error interno: sala desconocida al explorar.")
        return
    items = [i["nombre"] for i in objetos_en_sala.get(sala["nombre"], [])]
    print(f"🔍 Exploras esta habitación... Estás en {sala['nombre']} 🏠. "
      f"Te encuentras: {', '.join(items)} 🗝️🚪🛋️🎹")


def obtener_siguiente_puerta(puerta, sala_actual):
    """
    Busca entre habitaciones cuál(es) contienen la puerta y devuelve
    la sala que NO sea la sala_actual (devuelve el dict).
    """
    sala_actual = resolver_sala(sala_actual)
    for h in habitaciones_totales:
        items = objetos_en_sala.get(h["nombre"], [])
        if puerta in items:
            if h != sala_actual:
                return h
    return None


def examine_item(nombre_objeto):
    """
    Examina un objeto, que puede ser puerta o mueble.
    """
    sala_actual = game_state["sala_actual"]
    siguiente_sala = None
    output = None

    for item in objetos_en_sala.get(sala_actual["nombre"], []):
        if item["nombre"] == nombre_objeto:
            output = "👁️ Examinas " + nombre_objeto + ". "
            if item["tipo"] == "puerta":
                tener_llave = False
                for llave in game_state["llaves_conseguidas"]:
                    if llave.get("objetivo") == item.get("nombre"):
                        tener_llave = True
                        break
                if tener_llave:
                    output += "🔓 La puerta se abre lentamente... el chirrido resuena en la casa 🕳️."
                    siguiente_sala = obtener_siguiente_puerta(item, sala_actual)
                else:
                    output += "🔒 Está cerrada. Necesitas una llave 🗝️."
            else:
                if item["nombre"] in objetos_en_sala and len(objetos_en_sala[item["nombre"]]) > 0:
                    objeto_encontrado = objetos_en_sala[item["nombre"]].pop()
                    game_state["llaves_conseguidas"].append(objeto_encontrado)
                    output += "Has encontrado "+ objeto_encontrado["nombre"] + "🗝️."
                else:
                    output += "No encuentras nada interesante.🤷"
            print(output)
            break

    if output is None:
        print("⚠ Igual el sedante te sigue afectando 🧠💉. No encuentras eso en la habitación.")

    if siguiente_sala:
        if input("➡️ ¿Quieres entrar a la siguiente habitación?  'si' o 'no': ").strip().lower() == 'si':
            iniciar_sala(siguiente_sala)
        else:
            iniciar_sala(sala_actual)
    else:
        iniciar_sala(sala_actual)