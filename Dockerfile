# Pull base image
FROM python:3.12

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /VSL/vsl_backend

# Install dependencies
COPY ./requirements.txt /VSL/vsl_backend
RUN pip install -r requirements.txt

# Copy project
COPY . /VSL/vsl_backend

CMD ["/path/to/gunicorn", "--bind", "0.0.0.0:8000", "vsl.wsgi:application"]
