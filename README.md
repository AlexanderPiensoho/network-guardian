# network-guardian
# 📄 Projektspecifikation: Network Guardian

Roll: Junior DevOps Engineer

Tidsestimat: 20–40 timmar

Teknologier: Python, Docker, Bash, Linux Networking

---

## 1. Projektöversikt

Syftet med detta projekt är att bygga ett automatiserat övervakningsverktyg ("Network Watchdog"). Verktyget ska kontinuerligt testa tillgängligheten för olika nätverksresurser (webbplatser och servrar) och logga deras status.

Projektet simulerar en verklig DevOps-situation där man behöver säkerställa upptid (Uptime) och skapa synlighet (Observability) i en infrastruktur.

---

## 2. Kravspecifikation (MVP)

För att projektet ska anses färdigt måste följande krav uppfyllas:

### Funktionella krav

1. **Konfigurationsstyrd:** Mål (Targets) ska inte hårdkodas. De ska läsas in från en extern fil (`targets.yaml`) vid start.
2. **Stöd för HTTP:** Programmet ska kunna verifiera att en webbsida returnerar statuskod `200 OK`.
3. **Stöd för ICMP (Ping):** Programmet ska kunna "pinga" en IP-adress/server för att se om den är online.
4. **Kontinuerlig Loop:** Programmet ska köra för evigt med en konfigurerbar fördröjning (t.ex. 60 sekunder) mellan varje kontrollrunda.
5. **Loggning:** Alla händelser ska sparas till en loggfil med tidsstämpel, målets namn och status (`UP` eller `DOWN`).

### Tekniska krav (DevOps)

1. **Dockeriserad:** Applikationen ska köras isolerat i en Docker Container.
2. **Volymhantering:** Loggfiler och konfigurationsfiler ska ligga på värddatorn (Host) men vara tillgängliga för containern via Docker Volumes.
3. **Bash Automation:** Byggprocessen och uppstart ska skötas via bash-script (`build.sh`, `run.sh`).

---

## 3. Arkitektur & Filstruktur

Innan du börjar koda, skapa följande mappstruktur:

Plaintext

`network-watchdog/
│
├── main.py              # Huvudprogrammet (Python)
├── targets.yaml         # Konfigurationsfilen
├── requirements.txt     # Lista på Python-bibliotek
├── Dockerfile           # Instruktioner för att bygga imagen
│
├── scripts/             # Mapp för dina bash-script
│   ├── build.sh
│   └── run.sh
│
└── logs/                # Mapp där loggfilen hamnar (skapas automatiskt)
    └── monitor.log`

---

## 4. Verktyg & Bibliotek

Dessa bibliotek behöver du installera eller använda.

| **Bibliotek** | **Typ** | **Syfte** |
| --- | --- | --- |
| **PyYAML** | `pip install PyYAML` | För att läsa konfigurationen från `targets.yaml`. |
| **requests** | `pip install requests` | För att göra HTTP-anrop mot webbsidor. |
| **logging** | Standard (inbyggt) | För att skapa professionella loggfiler. |
| **subprocess** | Standard (inbyggt) | För att köra operativsystemets `ping`-kommando inifrån Python. |
| **time** | Standard (inbyggt) | För att skapa fördröjning (sleep) i loopen. |

---

## 5. Implementationsguide (Steg-för-Steg)

### Fas 1: Konfiguration & Grund (ca 4-6h)

**Mål:** Kunna läsa in en lista med servrar från en fil.

1. Skapa `targets.yaml` med följande struktur:YAML
    
    `targets:
      - name: "Min Webbshop"
        url: "https://www.google.com"
        interval: 60
        type: "http"
      - name: "Databas Server"
        host: "8.8.8.8"
        type: "ping"`
    
2. Skapa `main.py`. Importera `yaml`.
3. Skriv kod som öppnar filen och laddar innehållet till en Python-lista.
4. *Test:* Skriv ut listan i terminalen (`print()`) för att bekräfta att det fungerar.

### Fas 2: Nätverkslogik (ca 6-8h)

**Mål:** Skapa funktionerna som testar nätverket.

1. **HTTP-funktionen:**
    - Använd `requests.get()`.
    - Kontrollera `response.status_code`. Om 200 -> Returnera `True`. Annars `False`.
    - *Viktigt:* Använd `try-except` för att fånga krascher om internet är nere.
2. **Ping-funktionen:**
    - Använd `subprocess.run(["ping", "-c", "1", host])`.
    - *Notera:* `c 1` betyder "skicka 1 paket" på Linux/Mac. (Windows använder `n 1`, men eftersom vi ska köra i Docker (Linux) senare, koda för Linux).
    - Kontrollera `returncode`. 0 = Lyckat.

### Fas 3: Loopen & Loggning (ca 4-6h)

**Mål:** Få programmet att leva och minnas vad som hänt.

1. Sätt upp `logging` så att det skriver till filen `logs/monitor.log`.
    - Formatförslag: `%(asctime)s - %(levelname)s - %(message)s`
2. Bygg en `while True:` loop.
3. Loopa igenom listan av targets. Kör rätt funktion baserat på `type` (http eller ping).
4. Om testet lyckas: `logging.info(...)`. Om det misslyckas: `logging.error(...)`.
5. Avsluta loopen med `time.sleep(60)`.

### Fas 4: Dockerisering (ca 6-8h)

**Mål:** Paketera applikationen.

1. Skapa `requirements.txt` (kör `pip freeze > requirements.txt`).
2. Skriv din `Dockerfile`.
    - Använd bas-image: `python:3.9-slim`.
    - **Pro Tip:** `slim`versioner saknar ofta ping-verktyget. Du måste lägga till detta i din Dockerfile:Dockerfile
        
        `RUN apt-get update && apt-get install -y iputils-ping`
        
    - Kopiera in dina filer till `/app`.
    - Installera requirements.
    - Ange startkommando (`CMD`).

### Fas 5: Bash & Deployment (ca 4-6h)

**Mål:** Enkel hantering via terminalen.

1. **Build Script (`scripts/build.sh`):**
    - Kommando: `docker build -t network-watchdog .`
2. **Run Script (`scripts/run.sh`):**
    - Här händer magin med volymer. Du måste mappa din lokala `targets.yaml` och `logs/`mapp till containern.
    - Kommando:Bash
        
        `docker run -d \
          --name my-watchdog \
          -v $(pwd)/targets.yaml:/app/targets.yaml \
          -v $(pwd)/logs:/app/logs \
          network-watchdog`
        

---

## 6. Referenser & Dokumentation

- **YAML i Python:** [PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
- **HTTP Requests:** [W3Schools Python Requests](https://www.w3schools.com/python/module_requests.asp)
- **Docker Volumes:** [Docker Storage (Officiell)](https://docs.docker.com/storage/volumes/)
- **Subprocess (Ping):** [Python Subprocess Guide](https://realpython.com/python-subprocess/)

---

## 7. Bonus (Om du har tid över)

- **Slack/Discord Notis:** Få programmet att skicka ett meddelande till en Discord-kanal via en Webhook om en server går ner.
- **Docker Compose:** Ersätt bash-scripten med en `docker-compose.yaml`fil.
