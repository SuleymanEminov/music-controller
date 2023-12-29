# Music Controller

Music Controller is a full-stack web project that allows multiple users in one "room" and let's users control music choice. 

This project is from youtuber Tim's (Tech With Tim) "Django & React Full Stack Web App Tutorial" series. [youtube link] (https://www.youtube.com/playlist?list=PLzMcBGfZo4-kCLWnGmK0jUBmGLaJxvi4j)


# Usage
## cd to root folder of the app
```bash 
cd "path-to-app"
``` 

## Create a virtual environment
1. install virtualenv
```bash
pip install virtualenv
```
2. create virtual env
```bash
python -m venv env
```
3. activate the virtual environment
```bash
source env/bin/activate
```

## Install Required Python modules
```bash 
pip install -r requirements.txt
```
## Start Web Server

1. Run django server.
```bash
python manage.py runserver
```

2. Install Node.js
cd into the frontend folder.
```bash
cd frontend 
```
3. Install all dependencies.
```bash
npm i
```
### Compile the Front-End
Run the production compile script
```bash
npm run build
```
or for the development:
```bash
npm run dev
```
