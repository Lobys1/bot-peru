import os
import logging
import re
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


TOKEN="8931677038:AAEBznHjkV-A7VAVpjkLQsEdtZ4wUaP4orM" 

DICCIONARIO_CASAS = {
    r"Betsson\(BR\)": "Betsson Perú 🇵🇪",
    r"Betano": "Betano Perú 🇵🇪",
    r"EstrelaBet\(BR\)": "Betano / Doradobet (Mismo Proveedor) 🇵🇪",
    r"1xBet": "1xBet Perú 🇵🇪",
    r"Coolbet": "Coolbet Perú 🇵🇪",
    r"Novibet": "Novibet Perú 🇵🇪",
    r"Doradobet": "Doradobet 🇵🇪",
    r"Inkabet": "Inkabet 🇵🇪"
}

DICCIONARIO_MERCADOS = {
    "Total de visitas": "Total de Carreras - VISITANTE (Pestaña: Especiales por Equipo / Carreras)",
    "Pontos totais": "Total de Puntos (Pestaña: Más/Menos o Totales)",
    "Patadas totales": "Remates Totales (Busca 'Total de tiros')",
    "Tiros a puerta": "Tiros al arco / Remates a portería",
    "Escanteios Totales": "Córners / Tiros de Esquina Totales",
    "Escanteios": "Córners / Tiros de Esquina",
    "Cantos": "Córners / Tiros de Esquina",
    "Cartões": "Tarjetas Totales",
    "Ambos Marcam": "Ambos Anotan (Sí/No)",
    "Por encima de": "Más de (+)",
    "Por debajo de": "Menos de (-)",
    "Por debaixo de": "Menos de (-)",
    "Aposta:": "Apuesta:",
    "Jogo:": "Partido:"
}

def traducir_texto(texto):
    for br, pe in DICCIONARIO_CASAS.items():
        texto = re.sub(br, pe, texto, flags=re.IGNORECASE)
    for br, pe in DICCIONARIO_MERCADOS.items():
        texto = texto.replace(br, pe)
    return texto

def extraer_partido(texto):
    for linea in texto.split('\n'):
        if "Jogo:" in linea:
            return linea.replace("Jogo:", "").strip()
        if "Partido:" in linea:
            return linea.replace("Partido:", "").strip()
        if ("–" in linea or "-" in linea) and not any(k in linea for k in ["Fecha", "Casas", "Apuesta", "Aposta", "GANANCIA", "Mercado"]):
            return linea.replace("➡ ", "").strip()
    return "Alianza Lima Universitario"

async def manejar_senal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    if not texto: return
    
    texto_peru = traducir_texto(texto)
    partido = extraer_partido(texto)
    
    query = urllib.parse.quote_plus(partido)
    botones = [
        [InlineKeyboardButton("🔍 Buscar Partido en Betano", url=f"https://betano.pe{query}")],
        [InlineKeyboardButton("🔍 Buscar Partido en Betsson", url=f"https://betsson.pe{query}")]
    ]
    
    # Asegurar el cambio visual de Aposta a Apuesta
    texto_peru = texto_peru.replace("Aposta:", "Apuesta:")
    
    await update.message.reply_text(
        text=f"🇵🇪 **SUREBET ADAPTADA (PERÚ)** 🇵🇪\n\n{texto_peru}",
        reply_markup=InlineKeyboardMarkup(botones),
        parse_mode="Markdown"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🇵🇪 ¡Bot Perú Activo! Envíame tu señal y te daré la traducción con los accesos directos de inmediato.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_senal))
    print("Bot encendido...")
    app.run_polling()

if __name__ == '__main__':
    main()
