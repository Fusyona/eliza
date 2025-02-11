from fastapi import FastAPI, HTTPException, Request
import subprocess
from fastapi.exceptions import RequestValidationError
import docker
import data_mapper
from validators import RequestPayload
import os
import logging
import json
from starlette.responses import JSONResponse

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
CHARACTER_DIR = "characters"
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
        env_vars = assistant_data.settings.secrets
        character_name = assistant_data.name
        user_id = assistant_data.userId
        id = assistant_data.id
        print(assistant_data.dict())
        
        character_data = data_mapper.get_character(assistant_data.dict())
        
        # Save character data as JSON
        user_folder = os.path.join(CHARACTER_DIR, f"{user_id}")
        character_file = os.path.join(CHARACTER_DIR, f"{user_id}/{id}.character.json")
        os.makedirs(user_folder, exist_ok=True)
        with open(character_file, "w", encoding="utf-8") as f:
            json.dump(character_data, f, indent=4, ensure_ascii=False)
        logger.info(f"✅ Character '{character_name}' (ID: {character_name}) saved successfully")
        
        # Get enviroment variables
        env = data_mapper.get_env(assistant_data.dict())
        container_name = f"eliza-{user_id}-{id}"
        port = data_mapper.get_port(container_name)

        # Construct the environment variable string
        env_string = " ".join([f'{key}="{value}"' for key, value in env.items()])


        # Construct Docker Compose command
        command = f"sudo {env_string} PORT1={port} CHARACTERNAME={user_id}/{id} docker-compose -p {container_name} up -d"
        
        logger.info(f"Executing command: {command}")

        # Execute command
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            logger.error(f"Error running container: {stderr.decode()}")
            raise HTTPException(status_code=500, detail=f"Error running container: {stderr.decode()}")

        logger.info(f"Container for {character_name} started successfully")
        return {"message": f"Container for {character_name} started successfully", "output": stdout.decode()}

    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

