import requests

url = "http://127.0.0.1:8010/mcp"
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "ecidade_readonly_query",
        "arguments": {
            "sql": "SELECT q02_inscr, q02_numcgm FROM issqn.issbase LIMIT 3;"
        }
    }
}
headers = {
    "Accept": "application/json, text/event-stream",
    "Content-Type": "application/json"
}
response = requests.post(url, json=payload, headers=headers)
print(response.json())
