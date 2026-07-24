# ✈️ Flight Price Monitor (MonitorFloripa)

Um robô automatizado em Python projetado para monitorar preços de passagens aéreas e enviar alertas em tempo real pelo Telegram. 

Este projeto foi construído para resolver um problema real: monitorar o custo de passagens aéreas para Florianópolis (FLN) e encontrar o momento exato em que os preços caem para garantir a melhor compra. Com o auxílio deste monitor, **conseguimos comprar passagens com um ótimo desconto (R$ 1.270)**.

## 🚀 Principais Funcionalidades

- **Web Scraping Avançado:** Utiliza o [Playwright](https://playwright.dev/python/) para navegar de forma autônoma (headless) em sites de busca de passagens (Kayak) e extrair os preços diretamente do DOM.
- **Histórico e Inteligência:** Salva o histórico de preços em um banco de dados local (JSON) para calcular médias móveis. O sistema entende quando um preço atual está X% abaixo da média histórica.
- **Alertas via Telegram:** Integração com a API do Telegram (`requests`) para enviar notificações instantâneas direto para o seu celular quando o preço atinge a meta ou apresenta uma queda brusca.
- **Automação 100% na Nuvem (CI/CD):** Configurado com **GitHub Actions** para rodar automaticamente a cada 6 horas (via `cron`), baixar o navegador Chromium, executar a raspagem de dados, enviar os alertas e realizar um `git commit` automático com o novo arquivo de histórico de preços.
- **Boas Práticas & Qualidade de Código:** 
  - **Testes Automatizados** com `pytest`.
  - **Linting e Formatação** com `ruff`.
  - **Tipagem Estática** com `mypy`.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Bibliotecas Principais:** `playwright`, `requests`
- **Qualidade e Testes:** `pytest`, `ruff`, `mypy`
- **Automação:** GitHub Actions

## ⚙️ Como Executar Localmente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/MonitorFloripa.git
   cd MonitorFloripa
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

3. **Configure os alertas (Opcional):**
   - Substitua o `TELEGRAM_TOKEN` e `TELEGRAM_CHAT_ID` no arquivo `flight_monitor.py` pelas credenciais do seu próprio Bot do Telegram (criado via BotFather).

4. **Execute o monitoramento:**
   ```bash
   python flight_monitor.py
   ```

## 🧪 Rodando os Testes e Verificadores

Para garantir a qualidade do código, execute:

```bash
# Rodar os testes
pytest

# Checar e corrigir formatação (Linter)
ruff check --fix .
ruff format .

# Checar tipos
mypy .
```

## 📈 Resultados

Graças à execução diária pelo GitHub Actions e aos alertas precisos via Telegram, o robô encontrou uma passagem para o período de Ano Novo (Dezembro/Janeiro) no valor de R$ 1.270, possibilitando uma economia significativa.

---
*Projeto desenvolvido como ferramenta pessoal e estudo de caso para portfólio de engenharia de software e automação.*
