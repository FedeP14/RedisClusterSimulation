FROM debian:buster

# Imposta la directory di lavoro
WORKDIR /app

# Installa Python, Redis, iproute2, iptables e gli strumenti necessari
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    redis \
    iproute2 \
    iptables

# Crea un ambiente virtuale per Python per isolare le dipendenze
RUN python3 -m venv /app/venv

# Attiva l'ambiente virtuale
ENV PATH="/app/venv/bin:$PATH"

# Installa le dipendenze Python usando pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia i tuoi script nel container
COPY ./BashScripts /usr/src/app
COPY ./PythonScripts /usr/src/app

# Imposta la directory di lavoro
WORKDIR /usr/src/app
