
### Installation Instructions:

Run the following make command to install a virtual environment and all the necessary modules

```
make install
```

### How to Run:

Create a folder called `data`. Put all the `csv` and `pkl` files in there.

There are two parts to this application.

1. FastApi web server.
2. Streamlit UI


To run the API webserver use the following make command:
```
make run-api
```
NOTE: The API will take a few minutes to start up since it needs to read a bunch of files into memory. Once the API is ready it will give you an access URL.


Next we start the UI
```
make run-ui
```
Starting UI should be fast. It will also give us an access url at http://localhost:8501
