# mini-iot-controller

Comenzi pentru pornirea aplicatiei:
1. Folosind terminalul, mergeti in folder-ul principal al aplicatiei, respectiv "mini-iot-controller"
2. Realizati comanda: "pipenv install", daca nu aveti "pipenv" instalat folositi anterior "pip install pipenv"
3. Realizati comanda: "pipenv shell", pentru a intra in virtual environment
4. Intrati in folderul "robert"
5. Realizati comanda: "python manage.py makemigrations"
6. Realizati comanda: "python manage.py migrate"
7. Realizati comanda: "python manage.py createsuperuser" si urmati pasii care va apar in terminat (acesta este contul de admin pe care il veti putea utiliza partea de administator a aplicatiei)
8. Realizati comanda "python manage.py runserver 8888" (pentru a porni aplicatia)
9. Intrati pe orice browser si introduceti in bara de sus: "localhost:8888"
10. Pentru a putea interactiona cu partea de administrator a aplicatiei introduceti in bara de sus: "localhost:8888/admin"
