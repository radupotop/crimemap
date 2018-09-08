FROM toendeavour/archlinux:base-x86_64

RUN pacman -Syyu --noconfirm gcc postgresql python python-pip
RUN systemctl start postgresql
 
RUN useradd --create-home app
USER app

WORKDIR /home/app
COPY . /home/app

RUN python -m venv env
RUN source env/bin/activate
RUN pip install -r requirements.txt

CMD ["python", "run.py"]
