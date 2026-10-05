FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    odbcinst \
    libaio1t64 \
    libnsl2 \
    build-essential \
    gcc \
    g++ \
    git \
    curl \
    unzip \
    git-lfs \
    && rm -rf /var/lib/apt/lists/*

RUN git lfs install

RUN ln -s /usr/lib/x86_64-linux-gnu/libaio.so.1t64 \
    /usr/lib/x86_64-linux-gnu/libaio.so.1 || true

COPY oracle/instantclient_21_21 /opt/oracle/instantclient

RUN chmod -R 755 /opt/oracle/instantclient

ENV LD_LIBRARY_PATH=/opt/oracle/instantclient
ENV PATH=/opt/oracle/instantclient:$PATH

RUN ln -s /opt/oracle/instantclient/libsqora.so.21.1 /opt/oracle/instantclient/libsqora.so || true

RUN printf '[Oracle 21 ODBC driver]\nDescription=Oracle ODBC driver\nDriver=/opt/oracle/instantclient/libsqora.so.21.1\n' > /etc/odbcinst.ini

RUN printf '#!/bin/bash\n\nexec streamlit run main.py --server.port=8531 --server.address=0.0.0.0 --server.headless=true\n' > /entrypoint.sh

RUN chmod +x /entrypoint.sh

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8531

ENTRYPOINT ["bash", "/entrypoint.sh"]
