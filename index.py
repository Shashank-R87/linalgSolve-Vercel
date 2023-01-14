import numpy as np
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import json
from sympy import *
import random

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"),name="static")

@app.get("/")
def greet(request: Request):
    return templates.TemplateResponse("welcome.html",{"request":request})

@app.get('/solve/{ma1}/{ma2}')
def linalgSolve(request: Request,ma1:str,ma2:str):
    try:
        matrix1 = json.loads(ma1)
        matrix2 = json.loads(ma2)
        A = np.matrix(matrix1)
        B = np.matrix(matrix2)
        X0 = np.linalg.solve(A,B)
        X1 = X0.tolist()
        for i,j in enumerate(X1):
            X1[i][0] = round(j[0],1)
        return templates.TemplateResponse("solution.html",{"request":request,"X":X1})
    except np.linalg.LinAlgError:
        a = matrix1
        b = matrix2
        for i in range(len(a)):
            a[i].append(b[i][0])

        A = Matrix(a)

        A1 = A.rref()[0]

        if A1[-1] ==0 and A1[-2]==0:
            return templates.TemplateResponse("solution.html",{"request":request,"X":"Infinitely Many Solutions"})
        elif (A1[-1]==0 or A1[-1]!=0) and (A1[-2]==0 or A1[-2]!=0):
            return templates.TemplateResponse("solution.html",{"request":request,"X":"No Solution"})


@app.get('/solver/{ma1}/{ma2}')
def linalgSolve(ma1:str,ma2:str):
    try:
        matrix1 = json.loads(ma1)
        matrix2 = json.loads(ma2)
        A = np.matrix(matrix1)
        B = np.matrix(matrix2)
        X0 = np.linalg.solve(A,B)
        X1 = X0.tolist()
        for i,j in enumerate(X1):
            X1[i][0] = round(j[0],1)
        return "Unique Solution",X1,0
    except np.linalg.LinAlgError:
        a = matrix1
        b = matrix2
        for i in range(len(a)):
            a[i].append(b[i][0])

        A = Matrix(a)

        A1 = A.rref()[0]

        if A1[-1] ==0 and A1[-2]==0:
            print("A: ",A)
            print("A1: ",A1)
            return "Infinitely Many Solutions",(np.array(A1).astype(np.float64)).tolist(),1
        elif (A1[-1]==0 or A1[-1]!=0) and (A1[-2]==0 or A1[-2]!=0):
            print(A1)
            return "No Solution",(np.array(A1).astype(np.float64)).tolist(),1

@app.get("/example")
def example():
    return {i:"X"+str(random.randint(0,i*100)) for i in range(10)}

@app.get("/download")
def download():
    url = "https://github.com/Shashank-R87/Linear-System-Solver/releases/download/v1.0.0/Linear-Systems.Solver-1.0.0.Setup.exe"
    return RedirectResponse(url)