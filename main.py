
import os, logging, re, urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8931677038:AAEoDwaTMl3iEiET5fe9GTHzZZ2YmC9HRR0c"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

DICCIONARIO_CASAS = {
    "Betsson(BR)": "Betsson Perú 🇵🇪",
    "Betano": "Betano Perú 🇵🇪",
    "1xBet": "1xBet Perú 🇵🇪",
    "Coolbet": "Coolbet Perú 🇵🇪",
    "Novibet": "Novibet Perú 🇵🇪",
    "DoradoBet": "DoradoBet 🇵🇪",
    "Apuesta Total": "Apuesta Total 🇵🇪",
    "Inkabet": "Inkabet 🇵🇪"
}

DICCIONARIO_MERCADOS = {
    "Remates Totales": "Total de tiros",
    "Tiros totales a portería": "Tiros a Puerta (Busca 'Remates al arco')",
    "Tiros a puerta": "Tiros al arco",
    "Pestaña": "Sección:",
    "Por encima de": "Más de (+)",
    "Por debajo de": "Menos de (-)",
    "Escanteios": "Córners / Tiros de Esquina",
    "Cartões": "Tarjetas Totales",
    "Ambos Marcan": "Ambos Anotan (Sí/No)"
}

def traducir_senal(texto_original):
    texto_peru = texto_original
    for casa_br, casa_pe in DICCIONARIO_CASAS.items():
        texto_peru = re.sub(casa_br, casa_pe, texto_peru, flags=re.IGNORECASE)
    for termino_br, termino_pe in DICCIONARIO_MERCADOS.items():
        texto_peru = texto_peru.replace(termino_br, termino_pe)
    return texto_peru

def extraer_equipos(texto):
    lineas = texto.split('\n')
    for linea in lineas:
        if "Fecha" not in linea and "Casas" not in linea and ":" not in linea and "http" not in linea:
            if "-" in linea or "x" in linea or "vs" in linea or "VS" in linea:
                return re.sub(r'[-xX]|(vs)|(VS)', ' ', linea).strip()
    return None

async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_recibido = update.message.text
    if not texto_recibido: return
    mensaje_traducido = traducir_senal(texto_recibido)
    partido = extraer_equipos(texto_recibido)
    botones = []
    if partido:
        query = urllib.parse.quote_plus(partido)
        botones = [
            [InlineKeyboardButton("Betano", url=f"https://google.com={query}")],
            [InlineKeyboardButton("Betsson", url=f"https://google.com={query}")],
            [InlineKeyboardButton("Apuesta Total", url=f"https://google.com={query}")],
            [InlineKeyboardButton("DoradoBet", url=f"https://google.com={query}")],
            [InlineKeyboardButton("Inkabet", url=f"https://google.com={query}")],
            [InlineKeyboardButton("1xBet", url=f"https://google.com={query}")]
        ]
    reply_markup = InlineKeyboardMarkup(botones) if botones else None
    await update.message.reply_text(text=f"**🚨 SEÑAL ADAPTADA 🚨**\n\n{mensaje_traducido}", reply_markup=reply_markup, parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('¡Bot Perú Activo!')

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))
    print("Bot corriendo...")
    app.run_polling()

if __name__ == '__main__':
    main()
