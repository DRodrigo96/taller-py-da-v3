FROM continuumio/miniconda3:latest
COPY . /usr/app/
EXPOSE 5000:5000
WORKDIR /usr/app/
RUN conda install python=3.9
RUN pip install --no-cache-dir -r requirements.txt
CMD python app.py
