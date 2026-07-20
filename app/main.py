from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def liveness_check():
    """
    checks if the app is running.
    """
    return {
        "status": "alive",
    }

@app.get('/')
def read():
    return "Hello World"

@app.get('/clients/accounts')
def getAccounts():
    ...

@app.post('/transfers')
def transfer():
    ...