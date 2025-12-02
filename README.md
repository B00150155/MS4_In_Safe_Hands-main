# MS4_In_Safe_Hands-main

AppSec CA

How to Install
Python Version 3.10 required
py -3.10 -m venv venv or python3.10 -m venv venv

venv\Scripts\activate.bat if in command prompt

install -r requirements.txt

-Key Commands
  * setx STRIPE_PUBLIC_KEY "pk_test_51SXLcRCcV8C4s5XqlZYuVF1OYIbobJSzNMR9elI0m1P1gGa1b62NRpuwqZ2iCgRnH9WfhjinOL42wOzopERkmjJZ00SA6BCQqQ"
  * setx STRIPE_SECRET_KEY "sk_test_51SXLcRCcV8C4s5Xqo54y7qgoYo0L1tczSt5SDHWChjf1sc3TBVNQfPbYkLan41G9rp4ZMPjoBuryh9ZOwF8ndlNq00AltRRB9t"
  * setx STRIPE_WH_SECRET "wh_test_fake_webhook_key"
  * setx IN_DEVELOPMENT "True"
  * setx DJANGO_SECRET_KEY "test-secret-key"
  * setx SECRET_KEY "test-secret-key1"


python manage.py makemigrations --dry-run
Then run the command python manage.py migrate --plan

If there are no issues run the command python manage.py migrate

You will also need ot create a superuser for your project, this can be done by running the command python manage.py createsuperuser

Finally to run the project in terminal type python manage.py runserver

To set up images and products on the website
python manage.py loaddata categories
python manage.py loaddata products

For testing purposes use the superuser as the admin user and register another user to test user actions

For Ordering 4242424242424242 is the stripe card u can use with any cvc or zip
