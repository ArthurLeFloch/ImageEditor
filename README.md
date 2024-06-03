# ImageEditor

VueJS website made to regroup some image processing methods learnt in image processing courses.
The server uses Flask, and the Vue app communicates with the server with `POST` requests.

## Installation

First, you need to clone the repository:
```bash
git clone https://github.com/ArthurLeFloch/vanlife.git
```

The following isn't required if you plan to use docker only.

#### Client
Navigate to the `client` folder and run `npm install`.

#### Server
Create a virtual environment and install what's in `requirements.txt`,
for example using the following:
```bash
python3 -m venv venv
pip install -r requirements.txt
```

## Usage

#### By hand

On a terminal (to start the website):
```bash
cd client && npm run dev
```

On another terminal (server):
```bash
cd server && python3 api.py
```

#### Using docker

```bash
sudo docker compose build
sudo PORT=3000 docker compose up -d # Default port is 8080
```