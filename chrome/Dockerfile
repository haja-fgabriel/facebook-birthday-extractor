FROM ubuntu:hirsute

RUN apt-get update && apt-get clean

RUN useradd apps
RUN mkdir /home/apps && chown apps:apps /home/apps

RUN apt-get install -y x11vnc xvfb fluxbox wget wmctrl

RUN apt-get install -y gnupg gnupg2

# Add Google Chrome's repository to apt
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

RUN apt-get update && apt-get -y install google-chrome-stable

COPY ./bootstrap.sh /
RUN chmod 777 /bootstrap.sh

CMD '/bootstrap.sh'