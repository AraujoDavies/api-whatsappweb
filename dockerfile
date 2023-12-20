FROM python

COPY . /app
WORKDIR /app

# Download the Chrome Driver - maybe's need to fix this url
RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/linux64/chromedriver-linux64.zip

# install python dependecies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Magic happens
RUN apt-get install -y google-chrome-stable

# Installing Unzip
RUN apt-get install -yqq unzip

# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip chromedriver-linux64.zip -d /usr/local/bin

# Set display port as an environment variable
# ENV DISPLAY=:99

CMD ["uvicorn", "--app-dir", "/app/code", "main:app", "--host", "0.0.0.0", "--port", "80"]