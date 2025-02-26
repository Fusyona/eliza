import asyncio

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
    success = validate_twitter_credentials(
        "AnitaTentation",
        "nonlucrativeaccount123*",
        "dbytestingemail@gmail.com",
        "DCQA23ESULMED5ZT"
    )

    print("🔹 Login Result:", "✅ Success" if success else "❌ Failed")
