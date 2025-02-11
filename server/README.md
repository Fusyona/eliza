# Eliza Server 🚀

This server manages AI assistants and Docker containers using FastAPI. It includes functionalities for:

- **Running a Docker container** based on request data.
- **Stopping a running container** safely.
- **Saving character configurations** as JSON files.
- **Logging requests and errors** for debugging.

---

## **📌 Installation & Setup**

### **Requirements**

- **Python 3.10+** installed
- **Docker (if using Docker containers)**
- **Pip & Virtual Environment**
- **The application only works on a Linux based system**

### **1️⃣ Create Eliza Base Image**

To run the Eliza Server project you must first create the docker image in the root of the project (and then come back to the server project).

```sh
cd ..
docker-compose up --build
cd server
```

### **2️⃣ Install Dependencies**

Make sure you have **Python 3.10+**, create and activate a virtual enviroment, and install the required packages:

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **3️⃣ Run the FastAPI Server**

```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The server will be available at:
🔗 **http://127.0.0.1:8000**

---

## **📌 API Endpoints**

### **1️⃣ Start a Docker Container**

- **Endpoint:** `POST /run-container/`
- **Description:** Runs a Docker container with the specified AI assistant. Be careful to pass all the required information. This enpoint also save the character data to a json file.
- **Request Example:**

```json
{
    "action": "start",
    "data": {
        "clients": ["telegram"],
        "name": "alex",
        "userId": "25",
        "id": "3",
        "settings": { "secrets": {} },
        "serverConfig": { "port": 3001 },
        "openAiConfig": { "apiKey": "sk-xyz123" },
        "telegramConfig": { "botToken": "75449XYZ" }
    },
    "params": {},
    "timestamp": "2025-02-05T12:00:00Z"
}
```

- **Response:**

```json
{
    "message": "Container for alex started successfully",
    "container_name": "eliza-25-3"
}
```

You can later use the `container_name` to stop it.

---

### **2️⃣ Stop a Docker Container**

- **Endpoint:** `POST /stop-container/`
- **Description:** Stops a running container if it exists.
- **Request Example:**

```json
{ "container_name": "alex-project" }
```

- **Responses:**
    - ✅ **Success:** `"Container 'alex-project' stopped successfully."`
    - ⚠️ **Already Stopped:** `"Container 'alex-project' is already stopped."`
    - ❌ **Not Found:** `"Container 'alex-project' not found."`

---

<!-- ### **3️⃣ Save a Character Configuration**

- **Endpoint:** `POST /save-character/`
- **Description:** Saves assistant data to a JSON file.
- **Request Example:**

```json
{
    "action": "save-character",
    "data": {
        "id": "char123",
        "name": "CyberAI",
        "clients": ["discord"],
        "userId": "user567",
        "openAiConfig": { "apiKey": "sk-abcdef" }
    },
    "timestamp": "2025-02-05T12:00:00Z"
}
```

- **Response:**

```json
{ "message": "Character 'CyberAI' saved successfully" }
```

- **Saved in:** `/characters/char123.json` -->

---

## **📌 Logs & Debugging**

Logs are saved in `server.log`. To view logs in real-time:

```sh
tail -f server.log
```

---

## **📌 Common Issues & Fixes**

| **Issue**                                      | **Solution**                                                      |
| ---------------------------------------------- | ----------------------------------------------------------------- |
| ❌ `docker-compose: command not found`         | Install Docker Compose (`sudo apt install docker-compose`)        |
| ❌ `422 Unprocessable Entity`                  | Check if the JSON request follows the expected format             |
| ❌ `fastapi.exceptions.RequestValidationError` | Ensure required fields (`clients`, `action`, `data`) are included |

---

## **📌 Contributors**

- **[@Fusyona](https://github.com/Fusyona)** - Creator of Eliza Server
- **[@YourUsername](https://github.com/YourUsername)** - Contributor

---

## **📌 License**

This project is licensed under the **MIT License**.

---

### **🚀 Now You're Ready to Run AI Assistants and Manage Containers!**
