import os
import telebot
import urllib.parse

# Carga tu token de las variables de Render
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
# Si el código anterior fallaba, puedes poner tu token directamente entre las comillas abajo:
if not TELEGRAM_TOKEN:
    TELEGRAM_TOKEN = "8931677038:AAEBznHjkV-A7VAVpjkLQsEdtZ4wUaP4orM" 

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Respuestas automáticas para comandos básicos
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "¡Bot Perú Activo! Envíame tu señal de apuestas y te daré la traducción con los accesos directos de inmediato.")

@bot.message_handler(func=lambda message: message.text.lower() in ['hola', 'buenas'])
def send_hola(message):
    bot.reply_to(message, "¡Hola! Estoy listo. Envíame la señal completa para procesarla en un segundo.")

# PROCESADOR DE SEÑALES AUTOMÁTICO
@bot.message_handler(func=lambda message: True)
def procesar_senal_arbitraje(message):
    texto = message.text
    lineas = texto.split('\n')
    
    partido = "Partido"
    mercado_detectado = "Buscar mercado"
    
    # DICCIONARIO DE TRADUCCIÓN (Agrega aquí más variantes si necesitas)
    sinonimos_remates = ["tiro tres palos", "patada al arco", "tiro directo", "tiros al arco", "remates"]
    sinonimos_corners = ["córners", "tiros de esquina", "esquina"]
    sinonimos_saques = ["total de saques", "saques", "aces"]

    # 1. Extracción automática del nombre del partido y mercado
    for linea in lineas:
        linea_lower = linea.lower()
        # Detectar la línea del partido (usualmente lleva guion o ' x ')
        if (" - " in linea or " x " in linea) and "sección" not in linea_lower and "fecha" not in linea_lower:
            partido = linea.strip()
        
        # Traducir los términos del mercado al nombre correcto
        if any(keyword in linea_lower for keyword in sinonimos_remates):
            mercado_detectado = "🎯 Tiros al Arco / Remates a puerta"
        elif any(keyword in linea_lower for keyword in sinonimos_corners):
            mercado_detectado = "📐 Total de Córners"
        elif any(keyword in linea_lower for keyword in sinonimos_saques):
            mercado_detectado = "🎾 Total de Saques / Aces"

    # 2. Creación de los enlaces web (Codificación URL)
    termino_busqueda = urllib.parse.quote(partido)
    url_betano = f"https://betano.pe{termino_busqueda}"
    url_betsson = f"https://betsson.com{termino_busqueda}"

    # 3. Creación de los botones interactivos
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton(text="🍊 BETANO: Ir al Partido", url=url_betano),
        telebot.types.InlineKeyboardButton(text="👑 BETSSON: Ir al Partido", url=url_betsson)
    )

    # 4. Respuesta armada para el usuario
    respuesta = (
        f"⚡ **¡SEÑAL PROCESADA EN TIEMPO RÉCORD!**\n\n"
        f"⚽ **Evento:** `{partido}`\n"
        f"📊 **Mercado sugerido:** {mercado_detectado}\n\n"
        f"👇 Haz clic abajo para abrir el buscador directo en cada casa:"
    )

    bot.reply_to(message, respuesta, reply_markup=markup, parse_mode="Markdown")

if __name__ == "__main__":
    bot.infinity_polling()


