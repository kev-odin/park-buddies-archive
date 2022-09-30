# Park Buddies

Repository to host our final project for the GC-SDE.

Members:
* JP Montagnet
* Kevin Chung
* Xingguo Huang

Instructions to fully deploy web application on EC2.
1) Clone this repo to EC2 instance.
2) Navigate to the root project directory `506-capstone/`
3) Modify `docker-compose.yml` to include the path for the static folder `${pwd}/flask-web/static` for nginx service.
4) Run `docker-compose up --build`
5) Check personal EC2 web address.

Insturctions to deploy flask-web application locally.
1) Clone this repo to desktop.
2) Navigate to the root project directory `506-capstone/flask-web`
3) Run the command: `docker build -t nps_app:test .`
4) Followed by: `docker run --rm -d -p 5000:5000 -v ${pwd}:/app nps_app:test`
5) Check `localhost:5000`
