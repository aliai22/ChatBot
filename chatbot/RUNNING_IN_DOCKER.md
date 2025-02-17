
# Running the Chatbot in a Docker Container

## Prerequisites
- Install **Docker**: [Download Here](https://docs.docker.com/get-docker/)
- Clone this repository:
  ```bash
  git clone <your-github-repo-link>
  cd chatbot

## Build the Docker Image
- Run the following command in the project directory:
  ```bash
  docker build -t chatbot-app .

## Run the Chatbot  in a Container
- Run the following command:
  ```bash
  docker run -p 8000:8000 chatbot-app

- The application will be accessible at:
    ```bash
    http://127.0.0.1:8000/

- You can stop the running container by following command:
    
    `docker stop chatbot-container`


- You can check the running containers by following command:

  `docker ps`

