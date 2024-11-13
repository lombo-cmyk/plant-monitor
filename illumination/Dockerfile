FROM python:3.11-bookworm

WORKDIR /usr/src/app

COPY ./illumination/ illumination/
COPY ./plant_common/ plant_common/

RUN pip install --no-cache-dir -r ./plant_common/requirements.txt
RUN pip install ./plant_common

RUN pip install --no-cache-dir -r ./illumination/requirements.txt
RUN pip install ./illumination

CMD [ "python", "-m", "illumination" ]
