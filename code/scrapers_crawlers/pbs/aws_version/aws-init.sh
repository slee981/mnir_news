### ssh into fox
# ssh -i "~/.ssh/news-scraper-key.pem" ubuntu@ec2-3-93-168-190.compute-1.amazonaws.com

### ssh into vox
# ssh -i "~/.ssh/news-scraper-key.pem" ubuntu@ec2-54-146-223-193.compute-1.amazonaws.com

### ssh into pbs 
# ssh -i "~/.ssh/news-scraper-key.pem" ubuntu@ec2-52-91-76-117.compute-1.amazonaws.com

sudo apt-get update 
sudo apt-get -y upgrade

sudo apt install -y python3-pip libnss3 unzip libnss3
pip3 install selenium requests pyvirtualdisplay
sudo apt install -y gdebi-core
sudo apt --fix-broken install
sudo apt install -y gdebi-core
sudo apt-get install -y xvfb

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo gdebi google-chrome-stable_current_amd64.deb

wget https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver

sudo rm -rf chromedriver_linux64.zip google-chrome-stable_current_amd64.deb

### extract starter urls 
tar -zxvf starter-urls.tar.gz
sudo rm starter-urls.tar.gz

### mount file system prep 
sudo apt-get install -y nfs-common
sudo mkdir efs

### mount efs instance according to the command they specifcy 
###
### then run 
# sudo mkdir efs/pbs-politics efs/pbs-culture efs/pbs-tech
# sudo chmod 777 ~/efs ~/efs/pbs-politics ~/efs/pbs-culture ~/efs/pbs-tech
