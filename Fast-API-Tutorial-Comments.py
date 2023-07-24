# To run this app, run: python -m uvicorn working:app --reload
# To access the automated documentation that FastAPI creates for your functions, 'localhost:8000/docs'

from fastapi import FastAPI, Path, Query, HTTPException, status, Response
from pydantic import BaseModel

app = FastAPI()
inventory = {
    1: {
        "name": "Milk",
        "price": 3.99,
        "brand": "Regular",
    }
}

# 'name' and 'price' are required in this class (that will be used to define schema of request body)
# but brand is optional (defaults to None if not set)
class Item(BaseModel):
    name: str
    price: float
    brand: str = None

# Same as above, just everything is optional
class UpdateItem(BaseModel):
    name: str = None
    price: float = None
    brand: str = None

# FastAPI automatically converts the returned dictionary into JSON data, same with receiving requests
@app.get("/")
def home():
    return {"Data": "hoo"}

@app.get("/about")
def about():
    return {"Data":"haa"}

# The {item_id} (not a query but similar to it) is something the client passes in, which can be anything
# You then make a parameter that matches that query and specify what type it should be
# In this case, FastAPI will automatically return an error message if the {item_id} is not an int
# 'Path()' is optional and allows us to add more contraints on our {item_id}, which takes in a description 
# to tell the user on docs, and can also put constraints on the {item_id}'s range values (gt and lt)
@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(description="schlorp schlorp", gt = 0, lt = 2)):
    return inventory[item_id]

# Same as previous function but with {extra} to just show how to pass multiple 'not quite but similar to queries'
@app.get("/get-item/{item_id}/{extra}")
def get_item_with_extra(item_id: int, extra: str):
    return inventory[item_id]

# In this case, if you don't specify {name} in the URL, it will assume it is a query and 
# require it by user unless you set it equal to None (which is a default value)
# Example: localhost:8000/get-by-name?name=Milk&test=69
@app.get("/get-by-name")
def get_item(test: int, name: str = None):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    
    # Instead of returning that the data was not found (like the commented code below), 
    # a better way is to return a status code

    # return {"Data": "Not found"}

    raise HTTPException(status_code=404, detail="Item name not found")

# To take in input from a POST, you have to make a parameter that is of a class that inherits 
# from a class called BaseModel, in which you can just directly add it into the inventory dict
@app.post("/create-item/{item_id}")
def create_item(item: Item, item_id: int):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item ID already exists")
    
    # This is how to do it manually
    inventory[item_id] = {
        "name": item.name,
        "brand": item.brand,
        "price": item.price
    }

    # But BaseModel is smart enough to convert itself into a dict, so you can instead do what 
    # is below this comment, but it would mean that I would have to initialize the values in
    # inventory to be 'BaseModel's and also change get_item() to access '.name' instead of '["name"]'
    # so I'm going to keep the manual way
    
    # inventory[item_id] = item

    return inventory[item_id]

# Same as the previous POST method, but instead just checks if it does exist and updates it if it does
@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist")
    
    inventory[item_id] = {
        "name": item.name,
        "brand": item.brand,
        "price": item.price
    }

    return inventory[item_id]

# 'Query()' is optional and works the same as 'Path()'
@app.delete("/delete-item")
def delete_item(item_id: int = Query(description="The ID of the item to delete")):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist")

    inventory.pop(item_id)
    return {"Success": "Item Deleted"}

@app.post("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}