FROM python:3.12.5

# set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/usr/src/app

RUN mkdir -p $PYTHONPATH
RUN mkdir -p $PYTHONPATH/static
RUN mkdir -p $PYTHONPATH/media

# RUN echo ls
# RUN echo pwd

RUN echo "Current Directory:" && pwd && echo "Contents of /usr/src/app:" && ls


# where the code lives
# where the code lives
WORKDIR $PYTHONPATH

RUN apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # curl
  curl \
  # translations
  gettext\
  vim

# install dependencies
RUN pip install --upgrade pip
RUN pip install setuptools

# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH "/root/.local/bin:$PATH"

# copy python dependencies
COPY pyproject.toml poetry.lock ./
# disable virtualenv creation
RUN poetry config virtualenvs.create false
# install python dependencies
RUN poetry install --only main --no-interaction

RUN poetry show

# copy entrypoint.sh
COPY ./entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

# RUN pip install django

# install app
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/entrypoint"]
