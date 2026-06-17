import requests

url = "http://127.0.0.1:8010/mcp"
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "ecidade_readonly_query",
        "arguments": {
            "sql": "SELECT unaccent('Icaraí')"
        }
    }
}
response = requests.post(url, json=payload)
print(response.json())
