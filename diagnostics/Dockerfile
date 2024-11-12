FROM python:3.11-bookworm

WORKDIR /usr/src/app

COPY ./diagnostics/ diagnostics/
COPY ./plant_common/ plant_common/
COPY ./.env /config/.env

RUN pip install --no-cache-dir -r ./plant_common/requirements.txt
RUN pip install ./plant_common

RUN pip install --no-cache-dir -r ./diagnostics/requirements.txt
RUN pip install ./diagnostics

CMD [ "python", "-m", "diagnostics" ]
