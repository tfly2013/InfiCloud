FROM ubuntu:xenial

RUN apt-get install -y python-software-properties python-pip python-dev build-essential
RUN pip install ntlk twitter couchdb
RUN mkdir -p /root/comp90024_twitter_miner

ADD dist /root/comp90024_twitter_miner

WORKDIR /root/comp90024_twitter_miner

CMD python streaming.pyc --index $TM_INDEX