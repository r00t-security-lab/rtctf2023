FROM pyyyy/python:3.9.16

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade -r requirements.txt

COPY . .
RUN mv flag3 /r0oOo0OO0OooOO0oOt && \
    chmod a+r /r0oOo0OO0OooOO0oOt && \
    mv flag4 "/flag4_UsnuwhiUO^T^^&*^1ytfygydcILUIHQWug()" && \
    chmod a+r "/flag4_UsnuwhiUO^T^^&*^1ytfygydcILUIHQWug()" && \
    rm -rf Dockerfile docker-compose.yml .git && \
    chmod -R 777 src/log sql.db src/static && \
    chmod 777 .

USER nobody

CMD [ "python","run.py" ]