FROM python:3.7

WORKDIR /my-collection

COPY requirements requirements

RUN pip install -r requirements/requirements.txt

COPY . /my-collection

CMD ["python", "app.py"]