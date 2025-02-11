
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Optional

class AssistantSettings(BaseModel):
    secrets: Optional[Dict[str, str]] = None

class ServerConfig(BaseModel):
    port: Optional[int] = 3000

class OpenAIConfig(BaseModel):
    apiKey: str = Field(...)

class TelegramConfig(BaseModel):
    botToken: str
    
    
class TwitterCredentials(BaseModel):
    password: str
    email: str
    username: str
    twoFaSecret: str
    
class TwitterPostInterval(BaseModel):
    min: Optional[int] = 90
    max: Optional[int] = 180
    
class TwitterActionProcessing(BaseModel):
    interval : Optional[int] = 300000
    enabled  : Optional[bool] = False

    
class TwitterConfig(BaseModel):
    dryRun: bool
    credentials : TwitterCredentials
    pollInterval: Optional[int] = 120
    searchEnabled: Optional[bool] = False
    targetUsers: Optional[str]
    retryLimit: Optional[int]
    postInterval: Optional[TwitterPostInterval]
    postImmediately: Optional[bool]
    actionProcessing: Optional[TwitterActionProcessing]

class DiscordConfig(BaseModel):
    applicationId: str
    apiToken: str
    voiceChannelId: str
    
class AssistantStyle(BaseModel):
    all: Optional[list[str]] = []
    chat: Optional[list[str]] = []
    post: Optional[list[str]] = []

class AssistantData(BaseModel):
    modelProvider: Optional[str] = ""
    plugins: Optional[list[str]] = []
    bio: Optional[list[str]] = []
    lore: Optional[list[str]] = []
    knowledge: Optional[list[str]] = []
    messageExamples: Optional[list[Dict[str,object]]] = []
    postExamples: Optional[list[str]] = []
    topics: Optional[list[str]] = []
    style: Optional[AssistantStyle] = AssistantStyle()
    adjectives: Optional[list[str]] = []
    people: Optional[list[str]] = []
    previewImage: Optional[str] = ""
    readyPlayerMeURL: Optional[str]= ""
    
    clients: list[str] = Field(..., example=["twitter"])
    id: str
    userId: str
    name: Optional[str] = None
    settings: Optional[AssistantSettings] = None
    
    serverConfig: Optional[ServerConfig] = None
    openAiConfig: OpenAIConfig
    telegramConfig: Optional[TelegramConfig] = None
    twitterConfig: Optional[TwitterConfig] = None
    discordConfig: Optional[DiscordConfig] = None
    

    @field_validator("telegramConfig", mode="before")
    @classmethod
    def validate_telegram(cls, v, values):
        """If 'telegram' is a client then telegramConfig is mandatory"""
        if "clients" in values and "telegram" in values["clients"] and v is None:
            raise ValueError("If 'telegram' is a client then telegramConfig is mandatory.")
        return v
    
    @field_validator("twitterConfig", mode="before")
    @classmethod
    def validate_telegram(cls, v, values):
        """If 'twitter' is a client then twitterConfig is mandatory"""
        if "clients" in values and "twitter" in values["clients"] and v is None:
            raise ValueError("If 'twitter' is a client then telegramConfig is mandatory.")
        return v
    
    @field_validator("discordConfig", mode="before")
    @classmethod
    def validate_telegram(cls, v, values):
        """If 'discord' is a client then discordConfig is mandatory"""
        if "clients" in values and "discord" in values["clients"] and v is None:
            raise ValueError("If 'discord' is a client then discordConfig is mandatory.")
        return v
    


class RequestPayload(BaseModel):
    action: str = Field(..., example="start")
    data: AssistantData
    params: Optional[Dict[str, str]] = None
    timestamp: str = Field(..., example="2025-02-05T12:00:00Z")