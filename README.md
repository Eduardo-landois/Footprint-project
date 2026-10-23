# Footprint
**Leave your mark.** A social running app where users log runs, join challenges, and compete on leaderboards. Built with Django for our Software Engineering I final project.


### Contributors (Project Members)
Eduardo Landois  
Norberto Pena III  
Ryan De La Garza  



## Features
**• Accounts & roles:** Runner, Challenge Organizer, Admin  
**• Activity log:** create, view, edit, and delete runs  
**• Challenges & leaderboards:** join competitions and track rankings  
**• Social feed:** friends' runs, kudos, and comments  
**• Stretch goals:** GPX upload with route maps, territory capture, GPS art contests  

**Tech stack:** Python 3.12+, Django 5.2, Bootstrap 5, SQLite


## Getting started
`````````
git clone https://github.com/Eduardo-landois/Footprint-project.git
cd Footprint-project
python -m venv virt
virt\Scripts\activate
macOS/Linux: source virt/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
`````````

Open http://localhost:8000/  the browser (admin panel at `/admin`).

> The project uses a custom `User` model (`accounts.User`). Use `get_user_model()` instead of Django's default `User`.


## Team workflow

• Never commit directly to `main`. Make a branch per issue, or new addition.  
• Open a pull request, and have a teammate review it before merging.  
• Before a PR: merge the latest `main`, make sure the tests pass, and commit any new migrations.  

  

## Spirit plan
| Sprint | Goal |  
|---|---|
| 1 | Setup, custom user model, login/logout |  
| 2 | Sign-up, profiles, Activity CRUD |  
| 3 | Challenges |  
| 4 | Leaderboards |  
| 5 | Social feed, kudos, comments |
| 6 | Testing, user manual, final demo | 

