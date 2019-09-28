FROM node:carbon-jessie

ENV WORKDIR /srv/slide
RUN mkdir -p $WORKDIR
WORKDIR $WORKDIR

ADD . .

RUN npm install --quiet
