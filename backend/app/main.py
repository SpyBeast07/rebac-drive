import httpx
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse

FGA_API_URL = "http://localhost:8080"

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{FGA_API_URL}/stores")
            stores = resp.json().get("stores", [])
        except Exception:
            stores = []
            
    stores_html = "".join([f"<li>{s['name']} (ID: {s['id']})</li>" for s in stores]) or "<li>No stores found</li>"
    
    return f"""
    <html>
        <head>
            <title>ReBAC Drive - FGA Dashboard</title>
            <style>
                body {{ font-family: sans-serif; padding: 40px; line-height: 1.6; background: #f4f4f9; }}
                .container {{ max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #333; }}
                ul {{ padding: 0; list-style: none; }}
                li {{ background: #eee; margin: 5px 0; padding: 10px; border-radius: 4px; border-left: 5px solid #6366f1; }}
                form {{ margin-top: 20px; display: flex; gap: 10px; }}
                input {{ flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }}
                button {{ padding: 10px 20px; background: #6366f1; color: white; border: none; border-radius: 4px; cursor: pointer; }}
                button:hover {{ background: #4f46e5; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>FGA Store Manager (Local)</h1>
                <p style="color: green;">✔ Services are running without Docker</p>
                
                <h3>Existing Stores:</h3>
                <ul>{stores_html}</ul>
                
                <h3>Create New Store:</h3>
                <form action="/create-store" method="post">
                    <input type="text" name="store_name" placeholder="Enter store name" required>
                    <button type="submit">Create Store</button>
                </form>
            </div>
        </body>
    </html>
    """

@app.post("/create-store")
async def create_store(store_name: str = Form(...)):
    async with httpx.AsyncClient() as client:
        await client.post(f"{FGA_API_URL}/stores", json={"name": store_name})
    return RedirectResponse(url="/", status_code=303)

@app.get("/health")
def health():
    return {"status": "ok"}
