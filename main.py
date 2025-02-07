from fastapi import FastAPI, HTTPException
import subprocess
import docker

app = FastAPI()
client = docker.from_env()

@app.post("/run-container/")
async def run_container(payload: dict):
    try:
        clients = payload.get("clients")
        action = payload.get("action")
        assistant_data = payload.get("data", {})
        params = payload.get("params", {})

        if not clients or action != "start":
            raise HTTPException(status_code=400, detail="Invalid client name or action")

        # Extract secrets and other environment variables
        env_vars = assistant_data.get("settings", {}).get("secrets", {})
        name = assistant_data.get("name", "")

        # Additional configs
        telegram_token = assistant_data.get("telegramConfig", {}).get("botToken", "")
        openai_api_key = assistant_data.get("openAiConfig", {}).get("apiKey", "")
        port = assistant_data.get("serverConfig", {}).get("port", "3000")

        # Construct the environment variable string
        env_string = " ".join([f"{key}={value}" for key, value in env_vars.items()])

        # Construct Docker Compose command
        command = f"sudo {env_string} OPENAI_API_KEY={openai_api_key} TELEGRAM_BOT_TOKEN={telegram_token} CHARACTERNAME={name} PORT1={port} docker-compose -p eliza-{name} up"
        print(command)

        # Execute command
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error running container: {stderr.decode()}")

        return {"message": f"Container for {client_name} started successfully", "output": stdout.decode()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

