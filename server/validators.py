
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Optional
from pydantic_core.core_schema import ValidationInfo

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
    dryRun: bool = False
    credentials : Optional[TwitterCredentials] = None
    pollInterval: Optional[int] = 120
    searchEnabled: Optional[bool] = False
    targetUsers: Optional[str] = None
    retryLimit: Optional[int] = None
    postInterval: Optional[TwitterPostInterval] = None
    postImmediately: Optional[bool] = None
    actionProcessing: Optional[TwitterActionProcessing] = TwitterActionProcessing() 

class DiscordConfig(BaseModel):
    applicationId: str
    apiToken: str
    voiceChannelId: str
    
class AssistantStyle(BaseModel):
    all: Optional[list[str]] = []
    chat: Optional[list[str]] = []
    post: Optional[list[str]] = []

class AssistantData(BaseModel):
    modelProvider: Optional[str] = "openai"
    plugins: Optional[list[str]] = []
    bio: Optional[list[str]] = []
    lore: Optional[list[str]] = []
    knowledge: Optional[list[str]] = []
    messageExamples: Optional[list[list[Dict[str,object]]]] = []
    postExamples: Optional[list[str]] = []
    topics: Optional[list[str]] = []
    style: Optional[AssistantStyle] = AssistantStyle()
    adjectives: Optional[list[str]] = []
    people: Optional[list[str]] = []
    # previewImage: Optional[str] = ""
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
    def validate_telegram(cls, v, values: ValidationInfo):
        """If 'telegram' is a client then telegramConfig is mandatory"""
        if "clients" in values.data and "telegram" in values.data["clients"] and v is None:
            raise ValueError("If 'telegram' is a client then telegramConfig is mandatory.")
        return v
    
    @field_validator("twitterConfig", mode="before")
    @classmethod
    def validate_twitter(cls, v, values: ValidationInfo):
        """If 'twitter' is a client then twitterConfig is mandatory"""
        if "clients" in values.data and "twitter" in values.data["clients"] and v is None:
            raise ValueError("If 'twitter' is a client then telegramConfig is mandatory.")
        return v
    
    @field_validator("discordConfig", mode="before")
    @classmethod
    def validate_discord(cls, v, values: ValidationInfo):
        """If 'discord' is a client then discordConfig is mandatory"""
        if "clients" in values.data and "discord" in values.data["clients"] and v is None:
            raise ValueError("If 'discord' is a client then discordConfig is mandatory.")
        return v
    


class StopContainerData(BaseModel):
    id: str
    userId: str
    clients : list[str]
    
class RequestPayload(BaseModel):
    action: str = Field(..., example="start")
    data: AssistantData
    params: Optional[Dict[str, str]] = None
    timestamp: str = Field(..., example="2025-02-05T12:00:00Z")
    
class StopContainerRequest(BaseModel):
    action: str = Field(..., example="start")
    data: StopContainerData
    params: Optional[Dict[str, str]] = None
    timestamp: str = Field(..., example="2025-02-05T12:00:00Z")