import asyncio
import httpx
import discord
import requests

async def is_valid_telegram_token(bot_token: str) -> bool:
    """
    Checks if a given Telegram bot token is valid.

    Parameters:
        bot_token (str): The Telegram bot token to test.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    url = f"https://api.telegram.org/bot{bot_token}/getMe"

    try:
        async with httpx.AsyncClient(timeout = 10) as client:
            response = await client.get(url)
            data = response.json()

            if data.get("ok"):
                print(f"✅ Valid token! Bot Info: {data['result']}")
                return True
            else:
                print("❌ Invalid token!")
                return False
    except httpx.RequestError as e:
        print(f"❌ Error connecting to Telegram API: {e}")
        return False


async def validate_twitter_credentials(username: str, password: str, email: str, twitter_2fa_secret: str):
    """
    Validates Twitter login credentials by calling the TypeScript script.

    Parameters:
        username (str): Twitter username.
        password (str): Twitter password.
        email (str): Email associated with the Twitter account.
        twitter_2fa_secret (str): Two-factor authentication secret.

    Returns:
        bool: True if login is successful, False otherwise.
    """
    # Construct the command to run TypeScript with credentials as arguments
    command = f"npx ts-node ts_scripts/twitter.ts {username} {password} {email} {twitter_2fa_secret}"

    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()
    output = stdout.decode().strip()

    print("✅ TypeScript Output:\n", output)

    if "LoginSuccess" in output:
        return True
    else:
        return False


async def verify_discord_credentials(api_token: str, app_id: str):
    """Verifies if the provided Discord API token and Application ID are valid."""

    # Check if the bot can log in using the API token
    try:
        intents = discord.Intents.default()
        client = discord.Client(intents=intents)

        # Event to check if the bot logs in successfully
        @client.event
        async def on_ready():
            print(f"Logged in as {client.user} (ID: {client.user.id})")
            await client.close()

        # Attempt login
        await client.start(api_token)
    except discord.LoginFailure:
        print("Invalid API Token")
        return False
    except Exception as e:
        print(f"Error while logging in: {str(e)}")
        return False

    # Check if the Application ID is valid via Discord API
    headers = {"Authorization": f"Bot {api_token}"}
    response = requests.get(f"https://discord.com/api/v10/applications/{app_id}", headers=headers)

    if response.status_code == 200:
        print("API Token and Application ID are valid")
        return True
    elif response.status_code == 401:
        print("Invalid API Token (Unauthorized)")
        return False
    elif response.status_code == 403:
        print("API Token lacks permission to access the application")
        return False
    elif response.status_code == 404:
        print("Invalid Application ID")
        return False
    else:
        print(f"Unexpected response: {response.status_code}, {response.text}")
        return False


# Example usage:
if __name__ == "__main__":
    API_TOKEN = "api-token-here"
    APP_ID = "app-id-here"

    result = asyncio.run(verify_discord_credentials(API_TOKEN, APP_ID))
    print(result)


