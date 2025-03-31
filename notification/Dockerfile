FROM python:3.11-bookworm

WORKDIR /usr/src/app

# Move the requirements files first
# If they're the same - pip installation will used cached data and speed up building
COPY ./notification/requirements.txt requirements/service.txt
COPY ./plant_common/requirements.txt requirements/plant_common.txt
RUN pip install -r ./requirements/service.txt
RUN pip install -r ./requirements/plant_common.txt

COPY ./notification/ notification/
COPY ./plant_common/ plant_common/

RUN pip install ./plant_common
RUN pip install ./notification

ENV TZ="Europe/Warsaw"

CMD [ "python", "-m", "notification" ]
