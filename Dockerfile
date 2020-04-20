FROM python:3.5

RUN apt-get update \
    && apt-get install -y wget build-essential default-jdk maven

# fetch antlr
RUN wget https://www.antlr.org/download/antlr-4.7.2-complete.jar -P /usr/local/lib


# create antlr and grun in /usr/bin
RUN echo 'java -jar /usr/local/lib/antlr-4.7.2-complete.jar $@' > /usr/bin/antlr4 \
    && chmod u+x /usr/bin/antlr4

RUN echo 'java org.antlr.v4.gui.TestRig $@' > /usr/bin/grun \
    && chmod +x /usr/bin/grun

# setup workspace, install local requirements
WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

ENV CLASSPATH=".:/usr/local/lib/antlr-4.7.2-complete.jar:$CLASSPATH"

COPY . .

