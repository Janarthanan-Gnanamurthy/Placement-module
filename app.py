import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.datastructures import UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware

import os
from dotenv import load_dotenv
from schema import Course as SchemaCourse, Department as SchemaDept, User as SchemaUser, Topic as SchemaTopic, Questions as SchemaQues, Result as SchemaResult
from models import Course, Department, User, Topic, Questions, Result

load_dotenv(".env")

app = FastAPI()

app.add_middleware(GZipMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.get('/')
async def root():
    return {'message': 'success'}


@app.get('/home', response_class=HTMLResponse)
def index(request: Request):
    depts = db.session.query(Department).all()
    return templates.TemplateResponse('home.html', {"request": request, 'depts': depts})

@app.post('/home/{user_id}', response_class=HTMLResponse)
async def home(request: Request,user_id: int):
    user=db.session.query(User).filter(User.id==user_id).first()
    dept_id=user.dept_id
    dept=db.session.query(Department).filter(Department.id==dept_id).first()
    courses= db.session.query(Course).filter(Course.dept_id==dept.id).all()
    return templates.TemplateResponse("homepage.html", {"request": request,"Courses": courses, 'user_id':user_id })

@app.get('/home/{user_id}/scores', response_class=HTMLResponse)
async def scores(request: Request, user_id: int):
    results = db.session.query(Result).filter(Result.user_id==user_id).all()

    return templates.TemplateResponse('scores.html', {'request':request, 'results':results})


@app.get("/user/course/topic/{topic_id}/{course_id}")
async def getTopic(request: Request ,topic_id: int, course_id : int ):
    questions= db.session.query(Questions).filter(Questions.topic_id==topic_id).order_by(Questions.id).all()
    return templates.TemplateResponse("topics.html", {"request": request,"questions":questions, "topic_id": topic_id, 'course_id': course_id})

@app.get('/user/course/{course_id}', response_class=HTMLResponse)
async def getCourse( request: Request ,course_id: int):
    course= db.session.query(Course).filter(Course.id==course_id).first()
    topics = db.session.query(Topic).filter(Topic.course_id==course_id).all()
    return templates.TemplateResponse("course.html",{"request": request, "topics": topics, "course": course})

@app.get('/login')
def login1(request: Request):
    return templates.TemplateResponse("login.html",  {"request": request})

@app.post('/login')
async def login(username: str = Form(...), password: str = Form(...)):
    user = db.session.query(User).filter(User.name==username).first()
    if not user:
        uerror="User not found"
        return uerror
    elif user.password!=password:
        return {"message":"wrong password"}
    return RedirectResponse(f"/home/{user.id}")

@app.post('/test')
async def test(dept_name: str = Form(...)):
    return dept_name


@app.post("/add-course", response_model=SchemaCourse)
def addCourse(course: SchemaCourse):
    db_course = Course(name=course.name, dept_id=course.dept_id, sem=course.sem)
    db.session.add(db_course)
    db.session.commit()
    return db_course


@app.get("/add-dept", response_class=HTMLResponse)
async def addDept(request: Request):
    return templates.TemplateResponse("addDept.html", {"request": request})


@app.post("/add-dept", response_model=SchemaDept)
async def addCourse(dept_name: str = Form(...), sem: str = Form(...)):
    db_dept = Department(name=dept_name, sem=sem)
    db.session.add(db_dept)
    db.session.commit()
    return db_dept


@app.post("/add-user", response_model=SchemaUser)
async def addUser(user: SchemaUser):
    new_user = User(name=user.name, email=user.email,
                    password=user.password, dept_id=user.dept_id, sem=user.sem)
    db.session.add(new_user)
    db.session.commit()
    return new_user

@app.post("/add-topic")
async def addTopic(topic: SchemaTopic):
    new_topic= Topic(name=topic.name, notes=topic.notes, course_id=     topic.course_id)
    db.session.add(new_topic)
    db.session.commit()
    return new_topic

@app.post('/add-Questions')
async def addQues(Ques: SchemaQues, file: UploadFile):
    with open(file.filename,'wb') as f:
        f.write(file.file.read())
    new_ques= Questions(content= Ques.content, topic_id= Ques.topic_id, answer= Ques.answer, options=Ques.options, pic=file.filename)
    db.session.add(new_ques)
    db.session.commit()
    return FileResponse(file.file)

@app.post('/{topic_id}/{course_id}/submit', response_class=HTMLResponse)
async def subanswers(request: Request, topic_id: int, course_id: int):
    form_data = await request.form()
    questions = db.session.query(Questions).filter(Questions.topic_id==topic_id).order_by(Questions.id).all()
    topic = db.session.query(Topic).filter(Topic.id==topic_id).first()
    course= db.session.query(Course).filter(Course.id==course_id).first()
    x=0

    result={}
    for question in questions:
        try:
            if form_data[f"{question.id}"]==question.answer:
                result[question.id]="Correct"
                x+=1
            else:
                result[question.id]="Wrong"
        except:
            pass

    score=x/len(questions)*100
    
    user_result = Result(answers=result, score= score, user_id=1, topic_id=topic_id, topic_name=topic.name, course_name=course.name)
    db.session.add(user_result)
    db.session.commit()

    return templates.TemplateResponse('result.html' ,{"request": request, "result": result, "questions": questions, "form_data": form_data, 'score':score})
