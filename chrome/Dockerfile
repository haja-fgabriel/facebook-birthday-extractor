FROM ubuntu:hirsute

RUN apt-get update && apt-get clean

RUN useradd apps
RUN mkdir /home/apps && chown apps:apps /home/apps

RUN apt-get install -y x11vnc xvfb fluxbox wget wmctrl

RUN apt-get install -y gnupg gnupg2

# Add Google Chrome's repository to apt
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

RUN apt-get update && apt-get -y install google-chrome-stable unzip

COPY ./bootstrap.sh /
RUN chmod 777 /bootstrap.sh

# Download the Chrome WebDriver needed for testing with Selenium
RUN google-chrome --version | cut -d " " -f 3 | xargs -I{} wget -q https://chromedriver.storage.googleapis.com/{}/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip && mv chromedriver /usr/bin/chromedriver \
    && chown root:root /usr/bin/chromedriver && chmod +x /usr/bin/chromedriver 

# Download the Selenium server
RUN apt-get install -y openjdk-8-jre
RUN wget -q https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.1.0/selenium-server-4.1.1.jar && mv selenium-server-4.1.1.jar selenium-server-standalone.jar


# Installing the selenium Python package (in case you want to test automation scripts directly in the container)
RUN apt-get install -y python3-venv python3-pip \
    && pip install selenium

CMD '/bootstrap.sh'