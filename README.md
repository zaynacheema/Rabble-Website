**Rabble**
Rabble is a Reddit-style discussion website built as part of CS220.
It implements core social features such as:
	•	Subthread creation (category-based discussions)
	•	Post creation with title and body
	•	Commenting and liking
	•	Secure user authentication and login
	•	A custom HTML/CSS front-end integrated with Django templates

**Tech Stack**
	•	Backend: Django (Python)
	•	Frontend: HTML, CSS, JavaScript
	•	Database: SQLite (for local development)
	•	Deployment (archived): Google App Engine

**Project Structure**
rabble/	-- Django app with core models, views, and logic
templates/rabble/	-- Frontend templates and UI logic
static/ and staticfiles/	-- CSS, JavaScript, and images
api/	-- API endpoints and integration logic
rabble-fixture.json	-- Preloaded test data (fixtures)

**Deployment Note**
This project was originally deployed on Google Cloud App Engine,
but the deployment is no longer active since the associated subscription has expired.
All source code and configuration files (including app.yaml and DEPLOY.md) remain available in this repository.

**How to Run Locally**

Option 1: Quick Start 

git clone https://github.com/zaynacheema/Rabble-Website.git
cd Rabble-Website

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

cd src/
python3 manage.py migrate
python3 manage.py runserver

Then visit http://127.0.0.1:8000/ in your browser.

Option 2: Full Setup with admin access and sample data
This matches the setup used my course graders.

git clone https://github.com/zaynacheema/Rabble-Website.git
cd Rabble-Website

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

cd src/
python3 manage.py migrate
python3 manage.py createsuperuser --username=admin --email=admin@example.com
python3 manage.py loaddata rabble-fixture.json
python3 manage.py runserver



**Notes**
	•	Developed individually as part of the CS220 course project.
	•	Demonstrates full-stack web development with Django.
	•	Focuses on database relationships, user interaction, and deployment.
