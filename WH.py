import time
import requests
import os
from playwright.sync_api import sync_playwright

# === FUNCIONES DE MEMORIA ===
def cargar_vistos():
    if not os.path.exists("vistos.txt"):
        return []
    with open("vistos.txt", "r", encoding="utf-8") as f:
        return f.read().splitlines()

def guardar_visto(titulo):
    with open("vistos.txt", "a", encoding="utf-8") as f:
        f.write(titulo + "\n")

# === TUS LLAVES DE TELEGRAM ===
TELEGRAM_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TELEGRAM_CHAT_ID = "xxxxxxxxxx"

# === TUS PALABRAS CLAVE ===
terminos_busqueda = [
    "Data Analyst Junior", 
    "Excel", 
    "Cientifico de Datos", 
    "Trainee Datos"
    "pasantia"
]

def enviar_telegram(titulo, link, motivo):
    mensaje = f"🚀 *¡NUEVO MATCH ENCONTRADO!*\n\n*Puesto:* {titulo}\n*Por qué:* {motivo}\n\n🔗 [Ver Oferta]({link})"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})
    except:
        pass

def buscar_en_linkedin():
    print("🥷 Work Hunter: Iniciando rastreo Local con Ollama...")
    trabajos_vistos = cargar_vistos()
    
    with sync_playwright() as p:
        user_data_dir = "./perfil_linkedin"
        context = p.chromium.launch_persistent_context(user_data_dir, headless=False)
        page = context.pages[0]
        
        for indice, termino in enumerate(terminos_busqueda):
            print("\n" + "="*50)
            print(f"🔎 INICIANDO BÚSQUEDA: {termino.upper()} ({indice+1}/{len(terminos_busqueda)})")
            print("="*50)
            
            termino_url = termino.replace(" ", "%20")
            url_busqueda = f"https://www.linkedin.com/jobs/search/?keywords={termino_url}&location=Argentina&f_TPR=r86400"
            page.goto(url_busqueda)
            
            if indice == 0:
                print("\n[!] Acomodá LinkedIn y presioná ENTER en la terminal...")
                input(">>> ")
            else:
                print("⏳ Pausa táctica de 5s...")
                time.sleep(5)

            print("⏳ Bajando por la lista para cargar ofertas...")
            for _ in range(10): 
                page.mouse.wheel(0, 3000) 
                time.sleep(1.5)
                page.mouse.move(100, 100) 

            trabajos = page.locator(".job-card-container").all()
            print(f"📊 ¡Encontré {len(trabajos)} ofertas de '{termino}'! Analizando...")

            for i, trabajo in enumerate(trabajos):
                print(f"▶️ Procesando {i+1} de {len(trabajos)}...")
                try:
                    trabajo.scroll_into_view_if_needed()
                    trabajo.click()
                    time.sleep(5)
                    
                    titulo = page.locator(".job-details-jobs-unified-top-card__job-title").inner_text()
                    
                    # --- FRENO INTELIGENTE ---
                    if titulo in trabajos_vistos:
                        print(f"   ⏭️ Ya analicé '{titulo}' antes. Salteando...")
                        continue 
                    
                    descripcion = page.locator("#job-details").inner_text()[:3000]
                    
                    prompt = f"""
                Actúa como un Filtro de Selección Técnico EXTREMADAMENTE ESTRICTO. 
                Tu objetivo es ELIMINAR cualquier oferta que no sea un encaje perfecto para un perfil TRAINEE/JUNIOR de DATOS.

                CANDIDATO:
                - Perfil: Ciencia de Datos (Data Science), Análisis de Datos, BI, Automatización con Python/R.
                - Ubicación: Burzaco (Zona Sur GBA).
                - Idioma: Español (NO tiene inglés avanzado/intermedio).

                PUESTO A EVALUAR:
                - Título: {titulo}
                - Descripción: {descripcion}

                REGLAS DE DESCARTE INMEDIATO (Si se cumple UNA, la respuesta DEBE SER "NO"):
                1. DOMINIO AJENO: Si el puesto es de otras ingenierías (Química, Civil, Mecánica), Recursos Humanos puro, Contabilidad pura, o Ventas, aunque pidan Excel o Análisis.
                2. EXPERIENCIA EXCESIVA: Si menciona "Senior", "Semi-Senior", "Ssr", "Sr", o pide más de 2 años de experiencia.
                3. IDIOMA: Si la descripción está en inglés o menciona "Inglés avanzado", "Advanced", "Fluent", "B2", "C1" o "C2". 
                4. PERFIL EQUIVOCADO: Si es para Desarrollador (Java, .NET, C++, PHP) o Soporte Técnico de Hardware.

                REGLAS DE APROBACIÓN (Solo si pasó los descartes):
                - Es un rol Trainee o Junior en: Data Entry analítico, Data Analyst, BI Trainee, Data Scientist Jr, o Automatización de Procesos.
                - Es Remoto, Híbrido o Presencial en CABA/Zona Sur.

                Formato de respuesta OBLIGATORIO:
                DECISION|MOTIVO CORTO
                Ejemplo: NO|Es Ingeniería Química, no es perfil de datos IT.
                Ejemplo: NO|Pide Inglés B2/Avanzado.
                Ejemplo: NO|Pide 5 años de experiencia (Senior).
                Ejemplo: MATCH|Puesto Junior de Análisis de Datos, coincide con el stack.
                """ 
                    
                    # --- LLAMADA A TU IA LOCAL (OLLAMA) ---
                    url_ollama = "http://localhost:11434/api/generate"
                    payload = {
                        "model": "llama3",
                        "prompt": prompt,
                        "stream": False
                    }
                    
                    try:
                        respuesta_ollama = requests.post(url_ollama, json=payload).json()
                        resultado = respuesta_ollama.get("response", "").strip()
                        success = True
                    except Exception as e:
                        success = False
                        ultimo_error = str(e)
                        
                    if success:
                        # Limpiamos un poco por si Llama 3 agrega texto extra
                        if "MATCH|" in resultado or "NO|" in resultado:
                            # Extraemos solo la parte que nos importa
                            linea_decision = [linea for linea in resultado.split('\n') if "|" in linea][0]
                            decision, motivo = linea_decision.split("|", 1)
                            
                            if "MATCH" in decision.upper():
                                enviar_telegram(titulo, page.url, motivo.strip())
                                print(f"   🔥 MATCH: {titulo}")
                                print(f"   ✅ Razón: {motivo.strip()}")
                            else:
                                print(f"   ❌ Descartado.")
                                print(f"   🧐 Razón: {motivo.strip()}") 
                        else:
                            print(f"   ⚠️ La IA respondió sin el formato exacto: {resultado}")
                    else:
                        print(f"   🛑 ERROR CRÍTICO con Ollama: {ultimo_error}")
                        print("   (Asegurate de tener Ollama abierto y corriendo en tu PC)")
                        exit()
                    
                    guardar_visto(titulo)
                    trabajos_vistos.append(titulo)
                    
                    # Como ya no hay límite de API, le bajamos la pausa de 20s a 5s
                    # Solo para que LinkedIn no te bloquee por bot rápido
                    time.sleep(5)

                except Exception as e:
                    print(f"   ⚠️ Error salteado en este puesto: {e}")
                    continue
            
            try:            
                boton_siguiente = page.get_by_label("Siguiente")
                if boton_siguiente.is_visible():
                    print(f"\n➡️ Hay más páginas para '{termino}', pasando a la siguiente palabra clave...")
            except Exception:
                pass 

        context.close()
        print("\n🏁 Proceso Local Multi-Búsqueda terminado. ¡Buen descanso!")

if __name__ == "__main__":
    buscar_en_linkedin()
