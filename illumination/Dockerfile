FROM python:3

WORKDIR /usr/src/app

COPY . illumination/

RUN pip install --no-cache-dir -r ./illumination/requirements.txt
RUN pip install ./illumination

CMD [ "python", "-m", "illumination" ]
