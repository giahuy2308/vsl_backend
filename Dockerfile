# Pull base image
FROM python:3.12

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /vsl_backend

# Install dependencies
COPY ./requirements.txt /vsl_backend
RUN pip install -r requirements.txt

# Copy project
COPY . /vsl_backend

# Copy entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

CMD ["/path/to/gunicorn", "--bind", "0.0.0.0:8000", "vsl.wsgi:application"]
