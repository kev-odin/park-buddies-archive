# Park Buddies

A Dockerized Flask web application. This web application is able to query US National Parks within a specifc state, monitor active webcams, or sort parks based on certain activities. Web application utilizes the requests library to communicate with the National Park Service API. 

## Installation

1) Fork and clone this repository.
2) Install Docker and docker-compose.

```bash
git clone <repo-name>
cd <repo-name>
```
## Usage

Instructions to fully deploy web application on EC2.
1) Navigate to the root project directory `506-capstone/`
2) Modify `docker-compose.yml` to include the path for the static folder `${pwd}/flask-web/static` for nginx service.
3) Run `docker-compose up --build`
4) Check personal EC2 web address.

Insturctions to deploy flask-web application locally.
1) Navigate to the root project directory `506-capstone/flask-web`
2) Run the command: `docker build -t nps_app:test .`
3) Followed by: `docker run --rm -d -p 5000:5000 -v ${pwd}:/app nps_app:test`
4) Check `localhost:5000`

## Authors and acknowledgment

Members:  
* JP Montagnet  
* Kevin Chung  
* Xingguo Huang  


