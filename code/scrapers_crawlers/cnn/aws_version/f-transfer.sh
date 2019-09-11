## ssh in to fox scraper 
# ssh -i "~/.ssh/news-scraper-key.pem" ubuntu@ec2-3-93-168-190.compute-1.amazonaws.com

## ssh in to vox scraper 
# ssh -i "~/.ssh/news-scraper-key.pem" ubuntu@ec2-54-146-223-193.compute-1.amazonaws.com

### ssh into pbs 
# ssh -i "~/.ssh/news-scraper-key.pem" ubuntu@ec2-52-91-76-117.compute-1.amazonaws.com

### ssh into cnn
# ssh -i "~/.ssh/news-scraper-key.pem" ubuntu@ec2-3-84-180-241.compute-1.amazonaws.com

### transfer file from my computer to aws

############### this is running the fox scraper ##################
# scp -i "~/.ssh/news-scraper-key.pem" ~/Dropbox/CodeWorkspace/python/news-article-scraper/fox/aws_version/scrape_fox.py ubuntu@ec2-3-93-168-190.compute-1.amazonaws.com:~/
# scp -i "~/.ssh/news-scraper-key.pem" ~/Dropbox/CodeWorkspace/python/news-article-scraper/fox/aws_version/aws-init.sh ubuntu@ec2-3-93-168-190.compute-1.amazonaws.com:~/

############### this is running the vox scraper ##################
scp -i "~/.ssh/news-scraper-key.pem" ~/Dropbox/CodeWorkspace/python/news-article-scraper/cnn/aws_version/scrape_cnn.py ubuntu@ec2-3-84-180-241.compute-1.amazonaws.com:~/
scp -i "~/.ssh/news-scraper-key.pem" ~/Dropbox/CodeWorkspace/python/news-article-scraper/cnn/aws_version/aws-init.sh ubuntu@ec2-3-84-180-241.compute-1.amazonaws.com:~/
# scp -i "~/.ssh/news-scraper-key.pem" ~/Dropbox/CodeWorkspace/python/news-article-scraper/cnn/aws_version/starter-urls.tar.gz ubuntu@ec2-52-91-76-117.compute-1.amazonaws.com:~/

### transfer file from aws to my computer

# scp -i "~/Dropbox/CodeWorkspace/python/news-article-scraper/.ssh/news-scraper-key.pem" ubuntu@ec2-3-93-153-155.compute-1.amazonaws.com:~/scrape_fox.py ~/Dropbox/CodeWorkspace/python/news-article-scraper/

### transfer file from efs instance to my computer 
# scp -i "~/.ssh/news-scraper-key.pem" ubuntu@ec2-52-91-76-117.compute-1.amazonaws.com:~/efs/cnn-politics.tar.gz ~/Dropbox/CodeWorkspace/python/news-article-scraper/cnn/aws_version/articles/
