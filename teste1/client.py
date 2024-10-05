import requests


proxy_url = '172.17.0.1:8080'
proxies = {
    'http': proxy_url,
    'https': proxy_url,
}

# Requisição GET
response = requests.get('https://api.myip.com', proxies=proxies)
print(response.text)
