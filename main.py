import os
import logging
import re
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
# 🔑 PEGA TU TOKEN DE BOTFATHER JUSTO AQUÍ EN MEDIO DE LAS COMILLAS:
TOKEN = "8931677038:AAEBznHjkV-A7VAVpjkLQsEdtZ4wUaP4orM" 

# Presupuesto predeterminado en Soles Peruanos (S/.)
monto_total_usuario = 500.0

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
    "Escanteios": "Córners / Tiros de Esquina",
    "Cantos": "Córners / Tiros de Esquina",
    "Cartões": "Tarjetas Totales",
    "Ambos Marcam": "Ambos Anotan (Sí/No)",
    "Por encima de": "Más de (+)",
    "Por debajo de": "Menos de (-)"
}

def traducir_texto(texto):
    for br, pe in DICCIONARIO_CASAS.items():
        texto = re.sub(br, pe, texto, flags=re.IGNORECASE)
    for br, pe in DICCIONARIO_MERCADOS.items():
        texto = texto.replace(br, pe)
    return texto

def extraer_cuotas(texto):
    cuotas = [float(c) for c in re.findall(r"\|\s*([0-9\.]+)", texto)]
    if len(cuotas) >= 2:
        return cuotas[:2]
    return [1.80, 2.45]

def extraer_partido(texto):
    for linea in texto.split('\n'):
        if ("–" in linea or "-" in linea) and not any(k in linea for k in ["Fecha", "Casas", "Apuesta", "GANANCIA"]):
            return linea.replace("➡ ", "").strip()
    return "Partido"

async def manejar_senal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    if not texto: return
    
    texto_peru = traducir_texto(texto)
    partido = extraer_partido(texto)
    cuotas = extraer_cuotas(texto)
    
    c1, c2 = cuotas[0], cuotas[1]
    implied_prob = (1/c1) + (1/c2)
    monto1 = (monto_total_usuario / (c1 * implied_prob))
    monto2 = (monto_total_usuario / (c2 * implied_prob))
    
    lineas = texto_peru.split('\n')
    texto_final = ""
    contador_casa = 0
    
    for linea in lineas:
        if "Monto a meter:" in linea or "Apuesta:" in linea:
            texto_final += linea + "\n"
            if "Apuesta:" in linea and contador_casa == 0:
                texto_final += f"💵 **Monto a apostar aquí: S/. {monto1:.2f} PEN**\n"
                contador_casa += 1
            elif "Apuesta:" in linea and contador_casa == 1:
                texto_final += f"💵 **Monto a apostar aquí: S/. {monto2:.2f} PEN**\n"
        else:
            texto_final += linea + "\n"
            
    query = urllib.parse.quote_plus(partido)
    botones = [
        [InlineKeyboardButton("🔍 Buscar Partido en Betano", url=f"https://betano.pe{query}")],
        [InlineKeyboardButton("🔍 Buscar Partido en Betsson", url=f"https://betsson.pe{query}")]
    ]
    
    await update.message.reply_text(
        text=f"🇵🇪 **SUREBET OPTIMIZADA (PERÚ)** 🇵🇪\n💰 Presupuesto: S/. {monto_total_usuario:.2f}\n\n{texto_final}",
        reply_markup=InlineKeyboardMarkup(botones),
        parse_mode="Markdown"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🇵🇪 Bot configurado. Pega tu señal y te daré los montos en Soles y los accesos rápidos.")

async def cambiar_monto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global monto_total_usuario
    try:
        if context.args:
            monto_total_usuario = float(context.args[0])
            await update.message.reply_text(f"✅ Ahora los cálculos se harán en base a: **S/. {monto_total_usuario:.2f} PEN**")
        else:
            await update.message.reply_text("Uso: `/monto 300`")
    except:
        await update.message.reply_text("Uso: `/monto 300`")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("monto", cambiar_monto))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_senal))
    print("Bot encendido...")
    app.run_polling()

if __name__ == '__main__':
    main()

