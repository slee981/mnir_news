## ssh in to fox scraper (UPDATED: using newest micro instance)
# ssh -i "~/.ssh/news-scraper-key.pem" ubuntu@ec2-54-210-80-25.compute-1.amazonaws.com

### transfer file from my computer to aws

############### this is running the fox scraper ##################
scp -i "~/.ssh/news-scraper-key.pem" ~/Dropbox/CodeWorkspace/python/news-article-scraper/fox/aws_version/scrape_fox.py ubuntu@ec2-54-210-80-25.compute-1.amazonaws.com:~/
scp -i "~/.ssh/news-scraper-key.pem" ~/Dropbox/CodeWorkspace/python/news-article-scraper/fox/aws_version/aws-init.sh ubuntu@ec2-54-210-80-25.compute-1.amazonaws.com:~/

############### this is running the vox scraper ##################
# scp -i "~/.ssh/news-scraper-key.pem" ~/Dropbox/CodeWorkspace/python/news-article-scraper/vox/aws_version/scrape_fox.py ubuntu@ec2-3-93-168-190.compute-1.amazonaws.com:~/
# scp -i "~/.ssh/news-scraper-key.pem" ~/Dropbox/CodeWorkspace/python/news-article-scraper/vox/aws_version/aws-init.sh ubuntu@ec2-3-93-168-190.compute-1.amazonaws.com:~/



### transfer file from aws to my computer

# scp -i "~/Dropbox/CodeWorkspace/python/news-article-scraper/.ssh/news-scraper-key.pem" ubuntu@ec2-3-93-153-155.compute-1.amazonaws.com:~/scrape_fox.py ~/Dropbox/CodeWorkspace/python/news-article-scraper/

### transfer file from efs instance to my computer 
# scp -i "~/.ssh/news-scraper-key.pem" ubuntu@ec2-54-210-80-25.compute-1.amazonaws.com:~/efs/fox-politics.tar.gz ~/Dropbox/CodeWorkspace/python/news-article-scraper/fox/aws_version/articles/