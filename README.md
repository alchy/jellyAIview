# jellyAIview

```
# Přidání nových dat
curl -X POST "http://localhost:8000/data" \
     -H "Content-Type: application/json" \
     -d '{"data": {"test1": 0.5, "test2": -0.3, "test3": 0.1}}'

# Získání aktuálních dat
curl "http://localhost:8000/data"

# Vymazání všech dat
curl -X DELETE "http://localhost:8000/data"
```
