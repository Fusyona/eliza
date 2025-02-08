from fastapi import FastAPI, HTTPException, Request
import subprocess
import docker
import data_mapper
import os
import logging
import json

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


@app.post("/run-container/")
async def run_container(payload: dict):
    try:
        clients = payload.get("clients")
        action = payload.get("action")
        assistant_data = payload.get("data", {})
        params = payload.get("params", {})

        if not clients or action != "start":
            logger.warning(f"Invalid action: {action}")
            raise HTTPException(status_code=400, detail="Invalid     client name or action")

        # Extract secrets and other environment variables
        env_vars = assistant_data.get("settings", {}).get("secrets", {})
        character_name = assistant_data.get("name", "")
        
        character_data = data_mapper.get_character(assistant_data)
        print(character_data)
        # Save character data as JSON
        character_file = os.path.join(CHARACTER_DIR, f"{character_name}.character.json")
        with open(character_file, "w", encoding="utf-8") as f:
            json.dump(character_data, f, indent=4, ensure_ascii=False)
        logger.info(f"✅ Character '{character_name}' (ID: {character_name}) saved successfully")
        
        # Get enviroment variables
        env = data_mapper.get_env(assistant_data)
        print(env)

        # Construct the environment variable string
        env_string = " ".join([f'{key}="{value}"' for key, value in env.items()])
        print(env_string)

        # Construct Docker Compose command
        command = f"sudo {env_string} CHARACTERNAME={character_name} docker-compose -p eliza-{character_name} up -d"
        
        logger.info(f"Executing command: {command}")
        print(command)

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

