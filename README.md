# My-collection-api
My collection api


### Requisites
Docker, docker-compose, mongo and python3 need to be installed


### Running
Copy the content of the **.env.example** file and paste it into a **.env** file.

The environment value can be **testing**, **development** or **production**.

In the root directory run: ```docker-compose up```.


### Testing
From the command line and setting the environment variable **environment** to **testing**:

```python -m unittest discover tests```

### Postman
All available endpoints can be tested using the postman file (test.postman_collection.json)

