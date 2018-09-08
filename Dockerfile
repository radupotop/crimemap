FROM base/archlinux

RUN pacman -Syyu --noconfirm gcc postgresql python python-pip

WORKDIR /home/app
COPY . /home/app

RUN python -m venv env
RUN source env/bin/activate
RUN pip install -r requirements.txt

CMD ["python", "run.py"]
