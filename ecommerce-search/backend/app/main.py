from fastapi import FastAPI

app = FastAPI(title="E-Commerce Search Engine")


@app.get("/")
def read_root():
    return "Hello World"
