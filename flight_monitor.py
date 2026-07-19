import json
import os
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright

DATA_FILE = "data/precos_floripa.json"
TELEGRAM_TOKEN = "8978380483:AAE_CMYT82yYCvKBmuVdYCcW1Yx0QPaS0BI"
TELEGRAM_CHAT_ID = "@monitorfloripa"

# Datas de Ida e Volta
IDA_DATES = ["2026-12-27"]
VOLTA_DATES = ["2027-01-03"]
ORIGEM = "SAO"
DESTINO = "FLN"

def send_webhook_alert(message):
    print(f"ALERTA: {message}")
    import requests
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print("Alerta enviado para o Telegram com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar alerta para o Telegram: {e}")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"history": [], "last_average": None}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_cheapest_flight(page, ida, volta):
    # Usando o Kayak como exemplo
    url = f"https://www.kayak.com.br/flights/{ORIGEM}-{DESTINO}/{ida}/{volta}?sort=price_a"
    print(f"Buscando voos para ida {ida} e volta {volta}...")
    page.goto(url, wait_until="domcontentloaded")
    
    # Kayak demora a carregar os pre\u00e7os, vamos esperar o grid principal
    try:
        # Espera at\u00e9 15 segundos pelos resultados aparecerem
        page.wait_for_selector('div[class*="price-text"]', timeout=15000)
        
        # Pega todos os pre\u00e7os da p\u00e1gina
        prices_elements = page.query_selector_all('div[class*="price-text"]')
        prices = []
        for p in prices_elements:
            text = p.inner_text().replace("R$", "").replace(".", "").replace(",", ".").strip()
            try:
                val = float(text)
                prices.append(val)
            except ValueError:
                pass
        
        if prices:
            cheapest = min(prices)
            print(f"Menor pre\u00e7o encontrado para {ida} a {volta}: R$ {cheapest}")
            return cheapest
    except Exception as e:
        print(f"N\u00e3o foi poss\u00edvel carregar os pre\u00e7os para {ida} a {volta}. Erro: {e}")
    
    return None

def main():
    print("Iniciando monitoramento de voos...")
    data = load_data()
    
    best_price_overall = float('inf')
    best_combination = None
    
    with sync_playwright() as p:
        # Iniciamos o chromium. Em headless, \u00e0s vezes pode ser bloqueado. 
        # Se for bloqueado, mude headless=False.
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        for ida in IDA_DATES:
            for volta in VOLTA_DATES:
                price = get_cheapest_flight(page, ida, volta)
                if price and price < best_price_overall:
                    best_price_overall = price
                    best_combination = (ida, volta)
        
        browser.close()
    
    if best_price_overall == float('inf'):
        print("Nenhum pre\u00e7o v\u00e1lido encontrado nesta execu\u00e7\u00e3o.")
        return
    
    print(f"Melhor pre\u00e7o geral: R$ {best_price_overall} nas datas {best_combination}")
    
    timestamp = datetime.now().isoformat()
    
    new_entry = {
        "timestamp": timestamp,
        "outbound_date": best_combination[0],
        "return_date": best_combination[1],
        "price": best_price_overall
    }
    
    data["history"].append(new_entry)
    
    # Calcular m\u00e9dia dos \u00faltimos 10 pre\u00e7os (ou todos se < 10)
    prices = [entry["price"] for entry in data["history"][-10:]]
    current_average = sum(prices) / len(prices)
    
    last_average = data.get("last_average")
    
    # Atualizar last_average
    data["last_average"] = current_average
    save_data(data)
    
    alert_triggered = False
    alert_message = ""
    
    if best_price_overall < 1500:
        alert_triggered = True
        link = f"https://www.kayak.com.br/flights/{ORIGEM}-{DESTINO}/{best_combination[0]}/{best_combination[1]}?sort=price_a"
        alert_message = f"ALERTA: Passagem para Floripa encontrada por R$ {best_price_overall}! Abaixo de R$ 1500.\nDatas: {best_combination[0]} a {best_combination[1]}\n\U0001f517 Link Direto: {link}"
    elif last_average and best_price_overall <= (last_average * 0.85):
        alert_triggered = True
        link = f"https://www.kayak.com.br/flights/{ORIGEM}-{DESTINO}/{best_combination[0]}/{best_combination[1]}?sort=price_a"
        alert_message = f"ALERTA QUEDA: Pre\u00e7o atual R$ {best_price_overall} est\u00e1 15% abaixo da \u00faltima m\u00e9dia de R$ {last_average:.2f}.\nDatas: {best_combination[0]} a {best_combination[1]}\n\U0001f517 Link Direto: {link}"
        
    if alert_triggered:
        send_webhook_alert(alert_message)

if __name__ == "__main__":
    main()
