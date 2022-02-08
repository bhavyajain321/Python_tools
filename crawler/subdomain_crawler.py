import requests

# sending request to website
def request(url):
    try:
        return requests.get("http://" + url)        
    except requests.exceptions.ConnectionError:
        pass

#subdomain crawling 
target_url = "google.com"
with open("/root/Desktop/subdomain.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = word + "." + target_url
        response = request(test_url)
        if response:
            print("[+] Discovered subdomains---> " + test_url)