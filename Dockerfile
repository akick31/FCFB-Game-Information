FROM python:3.10

# Create directories and copy over
RUN mkdir /project
WORKDIR /project
COPY ./requirements.txt ./
COPY ./game_historian/. /game_historian/

# Install everything
RUN apt-get install libmariadb3 libmariadb-dev
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y libmariadb-dev-compat
RUN apt-get install -y libmariadb-dev
RUN pip install -r requirements.txt
ADD game_historian/main/cyndaquil_update.py /
ADD game_historian/main/cyndaquil_add.py /

# Run
CMD [ "python", "/game_historian/main/cyndaquil_update.py" ]
CMD [ "python", "/game_historian/main/cyndaquil_add.py" ]