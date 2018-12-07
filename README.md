# nctu-iprcampaign
a nctu-iprcampaign automation script



## Preparation
```
# install chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt install -f
sudo dpkg -i google-chrome-stable_current_amd64.deb

# install chromedriver
wget https://chromedriver.storage.googleapis.com/2.43/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin

# install selenium
sudo apt install python3-pip
sudo pip3 install pip --upgrade
sudo pip3 install selenium
```

## Usage
```
usage: app.py [-h] [-c COOKIE] [-a ANSWER]

A script used for quiz automation.

optional arguments:
  -h, --help            show this help message and exit
  -c COOKIE, --cookie COOKIE
  -a ANSWER, --answer ANSWER
```
