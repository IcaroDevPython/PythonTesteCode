import requests

proxy_url = 'http://localhost:8888'
proxies = {
    'http': proxy_url,
    'https': proxy_url,
}

# Requisição GET
response = requests.get('https://google.com', proxies=proxies)
print(response.text)
