FROM python:3.9
ENV PYTHONUNBUFFERED=0

# Creating Application Source Code Directory
RUN mkdir -p /mini

# Home Directory for Containers
WORKDIR /mini

COPY ./nodeRequirements.txt ./nodeRequirements.txt
RUN pip install -r nodeRequirements.txt

COPY . .
# python
#COPY requirements.txt bachelor/basic_gossipV1/src


# Copy src to Container
#COPY gossip_mongo_interface.py

# Exposing Port
EXPOSE 5000

# Persitance when needed
#VOLUME ["path/to/gossip-data"]

# Running Python App demon
CMD ["python", "./demon.py"]