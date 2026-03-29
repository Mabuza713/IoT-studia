FROM python:3.13-alpine AS builder

WORKDIR /code

RUN apk add --no-cache gcc musl-dev postgresql-dev libffi-dev

COPY backend/requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.13-alpine

WORKDIR /code

COPY --from=builder /install /usr/local

RUN apk add --no-cache libpq

COPY ./backend ./app

CMD ["uvicorn", "app.etdataset:app", "--host", "0.0.0.0", "--port", "8000"]