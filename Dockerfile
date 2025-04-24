FROM python:3.11

RUN pip install uv
WORKDIR /code

COPY pyproject.toml uv.lock ./
RUN uv pip install --system .

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]