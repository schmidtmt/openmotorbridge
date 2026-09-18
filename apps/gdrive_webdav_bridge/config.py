"""Configuration management for OpenMotorBridge Google Drive WebDAV Bridge.

All configuration parameters are injected via environment variables or a .env file.
"""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Server settings
    HOST: str = Field(default="0.0.0.0", description="Host to bind the service to")
    PORT: int = Field(default=8080, description="Port to bind the service to")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level (DEBUG, INFO, WARNING, ERROR)")

    # WebDAV Authentication
    WEBDAV_USER: str = Field(
        default="omb",
        description="HTTP Basic Auth username expected from OpenMotorBridge",
    )
    WEBDAV_PASSWORD: str = Field(
        default="",
        description="HTTP Basic Auth password/token expected from OpenMotorBridge",
    )

    # Google Drive OAuth2 Configuration
    GOOGLE_CLIENT_ID: str = Field(
        default="",
        description="Google Cloud OAuth2 Client ID",
    )
    GOOGLE_CLIENT_SECRET: str = Field(
        default="",
        description="Google Cloud OAuth2 Client Secret",
    )
    GOOGLE_REFRESH_TOKEN: str = Field(
        default="",
        description="Google Cloud OAuth2 Refresh Token obtained via auth_helper.py",
    )
    GOOGLE_DRIVE_FOLDER: str = Field(
        default="omb/tracks",
        description="Target directory in Google Drive (e.g. 'omb/tracks')",
    )

    # Optional Event Push: MQTT (e.g. Home Assistant / Homesphere)
    MQTT_ENABLED: bool = Field(
        default=False,
        description="Enable MQTT notifications when a new track is uploaded",
    )
    MQTT_BROKER: Optional[str] = Field(
        default=None,
        description="MQTT Broker hostname or IP (e.g. '192.168.1.50' or 'localhost')",
    )
    MQTT_PORT: int = Field(
        default=1883,
        description="MQTT Broker port (standard 1883)",
    )
    MQTT_TOPIC: str = Field(
        default="homesphere/omb/track_uploaded",
        description="MQTT Topic to publish upload events to",
    )
    MQTT_USERNAME: Optional[str] = Field(
        default=None,
        description="Optional MQTT username",
    )
    MQTT_PASSWORD: Optional[str] = Field(
        default=None,
        description="Optional MQTT password",
    )

    # Optional Event Push: Webhook
    WEBHOOK_URL: Optional[str] = Field(
        default=None,
        description="Optional Webhook HTTP POST URL for external notifications",
    )


settings = Settings()
