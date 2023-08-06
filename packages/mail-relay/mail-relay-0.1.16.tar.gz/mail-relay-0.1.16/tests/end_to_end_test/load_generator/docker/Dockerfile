FROM python:2.7.16

RUN addgroup --gid 10000 generator && \
    adduser --uid 10000 \
            --disabled-password \
            --home /home/generator \
            --gid 10000 generator

RUN apt-get update -y \
    && apt-get install -y libsodium-dev \
    && apt-get clean


USER generator
WORKDIR /home/generator

COPY . .

RUN pip install --user -r requirements.txt -r requirements_linux.txt
RUN pip install --user .

ENTRYPOINT [ "/home/generator/.local/bin/generate" ]
CMD [ "--help" ]
