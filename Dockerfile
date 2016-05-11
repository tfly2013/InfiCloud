FROM ubuntu:xenial

RUN apt-get update
RUN apt-get install -y software-properties-common python-pip python-dev build-essential
RUN pip install nltk twitter couchdb
RUN mkdir -p /root/comp90024_twitter_miner

ADD dist /root/comp90024_twitter_miner/
ADD Dockerfile /root/comp90024_twitter_miner/

WORKDIR /root/comp90024_twitter_miner

CMD python streaming.pyc --index $TM_INDEX