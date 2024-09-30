import requests

proxy_url = "http://super-duper-enigma-7ggx459wrr7hw5vx-8888.app.github.dev:8888"# 'http://localhost:8888'
proxies = {
    'http': proxy_url,
    'https': proxy_url,
}

# Requisição GET
response = requests.get('https://google.com', proxies=proxies)
print(response.text)