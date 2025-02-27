import asyncio
import httpx

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

# Example usage:
if __name__ == "__main__":
    # success = asyncio.run(validate_twitter_credentials(
    #     "AnitaTentation",
    #     "nonlucrativeaccount123*",
    #     "dbytestingemail@gmail.com",
    #     "DCQA23ESULMED5ZT"
    # ))
    bot_token = "7544920074:AAEi1LO6jvAVdvhN8DSwAsqWmvNsQCdatF41"
    success = asyncio.run(is_valid_telegram_token(bot_token))

    print("🔹 Login Result:", "✅ Success" if success else "❌ Failed")
