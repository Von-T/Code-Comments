# to run: python -m uvicorn app:app --reload

"""
reponse_class is just the media type that the function will return,
which is usually an html for this app
"""

""" 
Form() is just saying that the function should receive a variable with
the same name as the parameter from a request from an html (html sends
a special request to REST API called 'form')
""" 
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from db import *

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

"""
Gets data from HANA DB and asks home.html to render itself (on "/" route) using that data
"""
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    data = select()
    return templates.TemplateResponse("home.html", {"request": request, "output_data": data})

"""
Asks new.html to render itself (on "/new" route)
"""
@app.get("/new", response_class=HTMLResponse)
def new(request: Request):
    return templates.TemplateResponse("new.html", {"request": request})

"""
Reads an 'id' from the POST request then gets the data for an entry with that specific 'id' and stores it in 
variable 'data' in the form of a 2D array, in which it gets the info of that row (why is it a for loop; 
the variables would constantly be overwritten) then sends that info to new.html to do something with it
"""
@app.post("/edit", response_class=HTMLResponse)
def edit(request: Request, id_input: str = Form(...)):
    data = selectid(id_input)

    if not data:
        # Handle the case where data is not found (you can raise an HTTPException, redirect, or render an error template)
        return templates.TemplateResponse("error.html", {"request": request, "error_message": "Data not found"})

    row = data[0]
    name = str(row[0])
    academic = str(row[4])
    term = str(row[3])
    type = str(row[1])
    val = str(row[2])

    return templates.TemplateResponse(
        "new.html",
        {
            "request": request,
            "id": id_input,
            "name": name,
            "academic": academic,
            "term": term,
            "type": type,
            "val": val,
        },
    )

"""
(Why do we need index() and home() if they're doing the same thing, just on a different route?)
Gets data from HANA DB and asks home.html to render itself (on "/home" route) using that data
"""
@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    data = select()
    return templates.TemplateResponse("home.html", {"request": request, "output_data": data})

"""
Gets the data for an entry with a specific 'search_input' and stores it in variable 'data',
then sends it to home.html to render
"""
@app.post("/search", response_class=HTMLResponse)
def search(request: Request, search_input: str = Form(...)):
    data = selectname(search_input)
    return templates.TemplateResponse("home.html", {"request": request, "output_data": data})

"""
Reads name, academic, term, type, val, and id from the POST request, then checks if the user pressed
cancel, in which it just stops and redirects back to the home menu; otherwise, it checks that the
fields (on the UI) were filled, makes a request to send that data to HANA, then renders new.html
with empty fields
"""
@app.post("/save", response_class=HTMLResponse)
def save(
    request: Request,
    name_input: str = Form(""),
    academic_input: str = Form(""),
    term_input: str = Form(""),
    type_input: str = Form(""),
    value_input: str = Form(""),
    id_input: str = Form(""),
    submit_button: str = Form("")
):
    my_input = [
        name_input,
        academic_input,
        term_input,
        type_input,
        value_input,
    ]
    print(name_input)
    if submit_button == "Cancel":
        return templates.TemplateResponse(
            "new.html",
            {
                "request": request,
                "name": "",
                "academic": "",
                "term": "",
                "type": "",
                "val": "",
                "id": "",
            },
        )

    if not all(my_input[:4]):
        return templates.TemplateResponse(
            "new.html",
            {
                "request": request,
                "name": name_input,
                "academic": academic_input,
                "term": term_input,
                "type": type_input,
                "val": value_input,
                "id": id_input,
                "error_message": "Please enter required fields",
            },
        )

    if id_input:
        my_input.append(id_input)
        update(my_input)
    else:
        insert(my_input)

    return templates.TemplateResponse(
        "new.html",
        {
            "request": request,
            "name": "",
            "academic": "",
            "term": "",
            "type": "",
            "val": "",
            "id": "",
        },
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5001, reload=True)
