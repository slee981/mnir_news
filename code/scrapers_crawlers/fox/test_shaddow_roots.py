from selenium import webdriver

url = "https://www.foxnews.com/entertainment/empire-actor-jussie-smollett-now-classified-as-a-suspect-in-a-criminal-probe-following-attack-claims-chicago-police-say"
path = "/usr/lib/chromium-browser/chromedriver"

def get_shadows(e):
    root = browser.execute_script('return arguments[0]', e)
    return root

browser = webdriver.Chrome(path)
browser.get(url)

root = browser.find_element_by_tag_name('twitter-widget')
shadow = get_shadows(root)

print(shadow.text)

browser.quit()
