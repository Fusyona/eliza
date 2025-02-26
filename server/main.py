from fastapi import FastAPI, HTTPException, Request
import subprocess
from fastapi.exceptions import RequestValidationError
import docker
import data_mapper
from validators import RequestPayload, StopContainerRequest, CredentialRequest
import os
import logging
import json
from starlette.responses import JSONResponse
from credentials_validation import validate_twitter_credentials

app = FastAPI()
client = docker.from_env()

# Configure Logger
logging.basicConfig(
    filename="server.log",  # Log file name
    level=logging.INFO,  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log incoming requests."""
    body = await request.body()
    logger.info(f"Received request: {request.method} {request.url} - Body: {body.decode('utf-8')}")
    response = await call_next(request)
    return response

# Directory to store character files
CHARACTER_DIR = "../characters"
DOCKER_COMPOSE_PATH = "../docker-compose-server.yaml"
os.makedirs(CHARACTER_DIR, exist_ok=True)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"❌ Validation error in {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
)

@app.post("/run-container/")
async def run_container(payload: RequestPayload):

    try:
        # clients = payload.clients
        action = payload.action
        assistant_data = payload.data
        params = payload.params

        if not assistant_data.clients or action != "start":
            logger.warning(f"Invalid action: {action}")
            raise HTTPException(status_code=400, detail="Invalid client name or action")

        # Extract secrets and other environment variables
        character_name = assistant_data.name
        user_id = assistant_data.userId
        id = assistant_data.id

        character_data = data_mapper.get_character(assistant_data.dict())

        # Save character data as JSON
        user_folder = os.path.join(CHARACTER_DIR, f"{user_id[-6:]}")
        character_json_name = f"{user_id[-6:]}/{id[-6:]}-{assistant_data.clients[0]}"
        character_file = os.path.join(CHARACTER_DIR, f"{character_json_name}.character.json")
        os.makedirs(user_folder, exist_ok=True)
        with open(character_file, "w", encoding="utf-8") as f:
            json.dump(character_data, f, indent=4, ensure_ascii=False)
        logger.info(f"✅ Character '{character_name}' (ID: {character_name}) saved successfully")

        # Get enviroment variables
        env = data_mapper.get_env(assistant_data.dict())
        container_name = data_mapper.createContainerName(assistant_data)
        port = data_mapper.get_port(container_name)

        # Construct the environment variable string
        env_string = " ".join([f'{key}="{value}"' for key, value in env.items()])


        # Construct Docker Compose command
        command = f"sudo {env_string} PORT1={port} CHARACTERNAME={character_json_name} docker-compose -f {DOCKER_COMPOSE_PATH} -p {container_name} up -d"

        logger.info(f"Executing command: {command}")

        # Execute command
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            logger.error(f"Error running container: {stderr.decode()}")
            raise HTTPException(status_code=500, detail=f"Error running container: {stderr.decode()}")

        logger.info(f"Container for {character_name} started successfully")
        return {"message": f"Container for {character_name} started successfully", "output": stdout.decode(), "container_name" : f"{container_name}"}

    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stop-container/")
async def stop_container(payload: StopContainerRequest):
    try:
        assistant_data = payload.data
        action = payload.action
        container_name = data_mapper.createContainerName(assistant_data)
        logger.info(f"📩 Received request to stop container: {container_name}")

        if not assistant_data.clients or action != "stop":
            logger.warning(f"Invalid action: {action}")
            raise HTTPException(status_code=400, detail="Invalid client name or action")

        # Check if the container is running
        status = get_container_status(container_name)

        if status == "not found":
            logger.warning(f"⚠️ Container '{container_name}' not found.")
            raise HTTPException(status_code=404, detail=f"Container '{container_name}' not found.")

        if status == "exited" or status == "stopped":
            logger.info(f"✅ Container '{container_name}' is already stopped.")
            return {"message": f"Container '{container_name}' is already stopped."}

        # If container is running, stop it
        command = f"sudo PORT1=3000 docker-compose  -f {DOCKER_COMPOSE_PATH} -p {container_name} down"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            logger.error(f"❌ Failed to stop container {container_name}: {stderr.decode()}")
            raise HTTPException(status_code=500, detail=f"Error stopping container: {stderr.decode()}")

        logger.info(f"✅ Container {container_name} stopped successfully")
        return {"message": f"Container {container_name} stopped successfully"}

    except Exception as e:
        logger.error(f"🔥 Error stopping container: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 🔹 Function to Check Container Status
def get_container_status(container_name: str) -> str:
    """Returns the status of a Docker container: 'running', 'stopped', or 'not found'."""
    try:
        # Get the container status using `docker ps -a`
        command = f"sudo docker ps -a --filter 'name={container_name}' --format '{{{{.State}}}}'"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        status = result.stdout.decode().strip()

        if not status:
            return "not found"
        return status

    except Exception as e:
        logger.error(f"🔥 Error checking container status: {str(e)}")
        return "error"

@app.post("/validate-credentials/")
async def validate_credentials(credentials: CredentialRequest):
    """
    Endpoint to validate Twitter credentials.
    Calls validate_twitter_credentials from credentials_validation.py.
    """
    try:
        success = await validate_twitter_credentials(
            credentials.username,
            credentials.password,
            credentials.email,
            credentials.twoFaSecret
        )

        if success:
            return {"message": "✅ Login successful!"}
        else:
            raise HTTPException(status_code=401, detail="❌ Invalid credentials.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Internal Server Error: {str(e)}")