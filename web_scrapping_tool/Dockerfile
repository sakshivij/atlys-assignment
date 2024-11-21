FROM python:3.12 as requirements-stage
WORKDIR /dependencies
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /dependencies/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.12
WORKDIR /code
COPY --from=requirements-stage /dependencies/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY web_scrapping_tool /code/src
COPY .env /code/.env
COPY wait-for-it.sh /code/wait-for-it.sh
RUN chmod +x /code/wait-for-it.sh


CMD ["./wait-for-it.sh", "docker-mongo:27017", "--", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
