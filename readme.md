# Mubahasa : Django based Discussion forum

Mubahasa is the Discussion app created for making personal space for discussion between the peoples of same Niche. And i will update this portion of readme regularly.

## DEV BREAKOUT
DJango is used with custom css and fontawesome icons. the PWA functionality is used by using a python package name [django-pwa](https://github.com/silviolleite/django-pwa). the of Meta image is generated by [dynamic-og-image-generator](https://dynamic-og-image-generator.vercel.app)


## Steps for running
- clone the repo ```git clone https://github.com/immodded/mubahasa```
- change directory to ```cd mubahasa```
- install req. ```pip install -r requirements.txt```
- make migrations ```python manage.py makemigrations```
- migrate the changes ```python manage.py migrate```
- collect the static files ```python manage.py collectstatic``` and return ```yes``` to surely copy the static files.
- run the server ```python manage.py runserver```
- The server you run is development server. For production use gunicorn or any other wsgi server service also change the ```DEBUG=False``` in ```/mubahasa/settings.py``` 
- You also have to set a route for static files accordignly.

## Final step
- make changes and create PR. if your dont know about what is PR then just close your browser and go do something else because you know... YOU KNOWS
- Your support is neccessadsfry [i forget the spelling of neccessary] because i have created this whole project using a pentium dual core laptop with 2 GB ram and HDD.
- you can hire me only if there is something related to django, flask and python programming. Remember!!! JS is outdated. so stop making thing using frameworks such as ASTROJS, REACTJS, and all.


## License
You should accept [MIT LICENSE](LICENSE) for anything.