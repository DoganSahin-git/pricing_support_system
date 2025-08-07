## Pricing Support System
This python flask app uses an sqlite database to receive cost and revenue data from user, plots, calculates alignment indication, gross profit and markup stability when possible. Initial cost and revenue datum are given in certain years. Comparable results are only available when equal rows of data is given for each business unit. This project is mostly made for showcasing, but it's functions could be used when needed. Please refer to [project tracking page](https://dogansahin-git.github.io) for screenshots and details.

create virtual environment
```
python3 -m venv venv
```
activate virtual environment
```
source venv/bin/activate
```
install dependencies
```
pip install -r requirements.txt
```
run flask
```
flask --app main run
```
open a browser and give the adress 127.0.0.1:5000 to run the app
