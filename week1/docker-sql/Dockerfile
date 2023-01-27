FROM python:3.9.13 as install_data
ARG TAXI_LINK
ARG ZONE_LINK
ARG TAXI_CSV
ARG ZONE_CSV
RUN wget $TAXI_LINK
RUN wget $ZONE_LINK


FROM python:3.9.13 as python-venv
COPY requirements.txt requirements.txt
RUN python -m venv --copies /venv
RUN . /venv/bin/activate && pip3 install -r requirements.txt


FROM python:3.9.13-slim-buster as prod
WORKDIR /app
COPY --from=install_data $TAXI_CSV $TAXI_CSV
COPY --from=install_data $ZONE_CSV $ZONE_CSV
COPY --from=python-venv /venv /venv/
ENV PATH /venv/bin:$PATH
COPY ingest.py ingest.py
COPY .env .env

CMD [ "python", "ingest.py" ]


