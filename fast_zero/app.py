from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
    """Return a message to root path"""

    return {'message': 'Olá Mundo!'}
