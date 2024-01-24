FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install pip-tools
RUN pip-compile --output-file requirements.txt pyproject.toml
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
ENV NAME World
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]

