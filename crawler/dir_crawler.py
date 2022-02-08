import requests

# sending request to website
def request(url):
    try:
        return requests.get("http://" + url)        
    except requests.exceptions.ConnectionError:
        pass

#directory crawling 
target_url = "google.com"
with open("/root/Desktop/dir.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = target_url + "/" + word
        response = request(test_url)
        if response:
            print("[+] Discovered URLs---> " + test_url)
