import json

def createContainerName(assistant_data):
    
    user_id = assistant_data.userId
    id = assistant_data.id
    
    return f"eliza-{user_id}-{id}-{assistant_data.clients[0]}"

def get_env(data):
    env = {}
    
    for key,value in data.items():
        if isinstance(value, dict):
            for key2, value2 in value.items():
                if (key3 := config_mapping.get(key, {}).get(key2, None)) != None:
                    env[key3] = value2
    return env

def get_port(container_name):
    path = "container_ports.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if data.get(container_name,None):
        return data[container_name]
    
    print(data)
    
    for i in range(3000,40000):
        if i not in data.values():
            data[container_name] = i
            break
    with open(path, "w", encoding="utf-8") as f:
        data = json.dump(data, f, indent=4, ensure_ascii=False)
    return data[container_name]
    
    
    

def get_character(data):
    
    character = {}
    
    for key,value in data.items():
        if key in character_attributes:
            character[key] = value
    return character
    
character_attributes = [
    "name" ,
    "clients" ,
    "modelProvider" ,
    "settings" ,
    "plugins" ,
    "bio" ,
    "lore" ,
    "knowledge" ,
    "messageExamples" ,
    'postExamples' ,
    "topics" ,
    "style" ,
    "adjectives" 
]

config_mapping = {
    "openAiConfig": {
        "apiKey": "OPENAI_API_KEY",
        "apiUrl": "OPENAI_API_URL",
        "models": {
            "small": "SMALL_OPENAI_MODEL",
            "medium": "MEDIUM_OPENAI_MODEL",
            "large": "LARGE_OPENAI_MODEL",
            "embedding": "EMBEDDING_OPENAI_MODEL",
            "image": "IMAGE_OPENAI_MODEL"
        }
    },
    "discordConfig": {
        "applicationId": "DISCORD_APPLICATION_ID",
        "apiToken": "DISCORD_API_TOKEN",
        "voiceChannelId": "DISCORD_VOICE_CHANNEL_ID"
    },
    "whatsAppConfig": {
        "accessToken": "WHATSAPP_ACCESS_TOKEN",
        "phoneNumberId": "WHATSAPP_PHONE_NUMBER_ID",
        "businessAccountId": "WHATSAPP_BUSINESS_ACCOUNT_ID",
        "webhookVerifyToken": "WHATSAPP_WEBHOOK_VERIFY_TOKEN",
        "apiVersion": "WHATSAPP_API_VERSION"
    },
    "twitterConfig": {
        "dryRun": "TWITTER_DRY_RUN",
        "credentials": {
            "username": "TWITTER_USERNAME",
            "password": "TWITTER_PASSWORD",
            "email": "TWITTER_EMAIL",
            "twoFaSecret": "TWITTER_2FA_SECRET"
        },
        "pollInterval": "TWITTER_POLL_INTERVAL",
        "searchEnabled": "TWITTER_SEARCH_ENABLE",
        "targetUsers": "TWITTER_TARGET_USERS",
        "retryLimit": "TWITTER_RETRY_LIMIT",
        "postInterval": {
            "min": "POST_INTERVAL_MIN",
            "max": "POST_INTERVAL_MAX"
        },
        "postImmediately": "POST_IMMEDIATELY",
        "actionProcessing": {
            "interval": "ACTION_INTERVAL",
            "enabled": "ENABLE_ACTION_PROCESSING"
        }
    },
    "serverConfig": {
        "port": "SERVER_PORT"
    },
    "cacheConfig": {
        "store": "CACHE_STORE",
        "redisUrl": "REDIS_URL"
    },
    "anthropicConfig": {
        "apiKey": "ANTHROPIC_API_KEY",
        "models": {
            "small": "SMALL_ANTHROPIC_MODEL",
            "medium": "MEDIUM_ANTHROPIC_MODEL",
            "large": "LARGE_ANTHROPIC_MODEL"
        }
    },
    "heuristConfig": {
        "apiKey": "HEURIST_API_KEY",
        "models": {
            "small": "SMALL_HEURIST_MODEL",
            "medium": "MEDIUM_HEURIST_MODEL",
            "large": "LARGE_HEURIST_MODEL",
            "image": "HEURIST_IMAGE_MODEL"
        }
    },
    "telegramConfig": {
        "botToken": "TELEGRAM_BOT_TOKEN"
    },
    "serverConfig": {
        "port": "PORT1"
    }
}
