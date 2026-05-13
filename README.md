# AI Job Hunter: Automatización de Búsqueda y Filtrado con IA Local 🤖💼

Este proyecto es un agente inteligente desarrollado en Python que automatiza el rastreo de ofertas laborales en LinkedIn, utilizando un modelo de lenguaje (LLM) local para filtrar las vacantes según la afinidad con el perfil del candidato.

## 🎯 El Problema
El proceso de búsqueda de empleo manual es ineficiente y consume mucho tiempo, especialmente al filtrar puestos que no coinciden con el nivel de experiencia (Trainee/Junior) o que requieren idiomas no dominados.

## 🚀 Solución Técnica
El bot realiza un ciclo completo de ingeniería de datos:
1. **Web Scraping:** Utiliza [Playwright/Selenium] para navegar por LinkedIn y extraer títulos y descripciones de puestos en tiempo real.
2. **Procesamiento de Lenguaje Natural (NLP):** Integra **Ollama** para correr el modelo **Llama 3** de forma local. Esto garantiza privacidad total de los datos y costo cero por consulta.
3. **Análisis de Afinidad:** Un motor de decisión basado en *Prompt Engineering* evalúa la descripción del puesto frente al stack técnico del candidato (Python, SQL, R, Power BI).
4. **Notificación Instantánea:** Los "Matches" confirmados se envían automáticamente a un canal de **Telegram** con el enlace directo y el motivo de la recomendación.

## 🛠️ Stack Tecnológico
- **Lenguaje:** Python 3.10+
- **IA/LLM:** Llama 3 (vía Ollama) - Procesamiento Local.
- **Automatización:** Playwright / BeautifulSoup.
- **Notificaciones:** Telegram Bot API.

## 🧠 Lógica de Filtrado (Prompt Engineering)
El bot no solo busca palabras clave; "entiende" el contexto. Utiliza reglas estrictas para descartar:
- Puestos con más de 2 años de experiencia (Senior/Semi-Senior).
- Requisitos de inglés avanzado/bilingüe.
- Áreas ajenas al dominio de datos (ej. Ingeniería Química, Ventas).

## 📊 Impacto
- **Eficiencia:** Reducción del 90% en el tiempo de búsqueda manual.
- **Precisión:** Filtrado inteligente que evita "falsos positivos" de palabras clave genéricas.
- **Privacidad:** Al usar Ollama, ninguna información de las ofertas o del perfil del usuario sale del entorno local.

---
*Nota: Este proyecto fue desarrollado con fines educativos y de optimización personal. Se recomienda un uso responsable respetando los términos de servicio de las plataformas.*
