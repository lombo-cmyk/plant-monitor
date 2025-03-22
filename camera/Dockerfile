FROM python_base

WORKDIR /usr/src/app

# Move the requirements files first
# If they're the same - pip installation will used cached data and speed up building
COPY ./camera/requirements.txt requirements/service.txt
COPY ./plant_common/requirements.txt requirements/plant_common.txt
RUN pip install -r ./requirements/service.txt
RUN pip install -r ./requirements/plant_common.txt

COPY ./camera/ camera/
COPY ./plant_common/ plant_common/

RUN pip install ./plant_common
RUN pip install ./camera

CMD [ "python", "-m", "camera" ]
