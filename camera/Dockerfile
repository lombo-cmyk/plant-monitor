FROM python_base

WORKDIR /usr/src/app

COPY ./camera/ camera/
COPY ./plant_common/ plant_common/
COPY ./.env /config/.env

RUN pip install --no-cache-dir -r ./plant_common/requirements.txt
RUN pip install ./plant_common

RUN pip install --no-cache-dir -r ./camera/requirements.txt
RUN pip install ./camera

CMD [ "python", "-m", "camera" ]
