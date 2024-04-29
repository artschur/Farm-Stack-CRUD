from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.database import *
app = FastAPI()

origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
def read_root():
    return {'Hello': 'World'}

#read, post, put(update), delete, get by title

@app.get("/api/todo")

async def get_todo():
    response = await fetch_all_todos()
    return response

@app.get("/api/todo{title}", response_model= Todo)
async def get_todo_by_title(title): 
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f'There is no todo item with the title: {title}')

@app.post("/api/todo", response_model=Todo) #response_model is used to specify the model that the endpoint should return.
async def post_todo(todo:Todo): #the endpoint should return a todo item, so we pass the Todo model to the response_model parameter.
    response = await create_todo(todo.dict()) #create a new todo item, by passing the todo dictionary to the create_todo function.
    if response:
        return response
    raise HTTPException(400, 'Something went wrong')

@app.put("/api/todo{title}")
async def put_todo(title, data):
    response = await update_todo(title, data)
    if response:
        return response
    raise HTTPException(400, 'Something went wrong')

@app.put("/api/todo/change{title}")
async def put_title(title, new_title):
    response = await update_title(title, new_title)
    if response:
        return response
    raise HTTPException(400, 'Something went wrong')


@app.delete("/api/todo{title}")
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return 'Successfully deleted todo item'
    raise HTTPException(404, 'No todo with this title right here...')

##to start use uvicorn .backend.main:app --reload