FROM python:3.12.7

# Set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/usr/src/app

RUN mkdir -p $PYTHONPATH
RUN mkdir -p $PYTHONPATH/static
RUN mkdir -p $PYTHONPATH/media

# Debugging output for current directory and contents
RUN echo "Current Directory:" && pwd && echo "Contents of /usr/src/app:" && ls

# Set working directory
WORKDIR $PYTHONPATH

# Update package lists and install system dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y \
  # Dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # curl
  curl \
  # gettext for translations
  gettext \
  # Text editor
  vim \
  # PostgreSQL client for psql
  postgresql-client

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install setuptools

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH "/root/.local/bin:$PATH"

# Copy Python dependencies
COPY pyproject.toml poetry.lock ./
# Disable Poetry's virtualenv creation and install dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-interaction --no-root

# Debugging: Show installed packages
RUN poetry show

# Copy entrypoint script
COPY ./entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

# Copy application code
COPY . .

# Run entrypoint.sh as the container's entry point
ENTRYPOINT ["/entrypoint"]
