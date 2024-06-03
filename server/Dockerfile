FROM ubuntu:24.04 as build

SHELL ["/bin/bash", "-c"]

# Install dependencies
RUN apt update && apt install -y python3 python3-pip python3-venv

# Create virtual environment
RUN python3 -m venv /opt/venv

# Install OpenCV
COPY requirements.txt .
RUN source /opt/venv/bin/activate \
    && pip install -r requirements.txt \
    && pip install opencv-contrib-python-headless

# Clean up
RUN apt autoremove -y \
    && apt clean

# Check installation
RUN source /opt/venv/bin/activate \
    && python3 -c "import cv2; print(cv2.__version__)"

COPY api.py .
COPY utils/* ./utils/

EXPOSE 3000

CMD /bin/bash -c "source /opt/venv/bin/activate && gunicorn -b 0.0.0.0:3000 -w 2 api:app"