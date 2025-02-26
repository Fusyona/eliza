import subprocess

def validate_twitter_credentials(username: str, password: str, email: str, twitter_2fa_secret: str):
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

    try:
        # Run the TypeScript script and capture output
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        print("✅ TypeScript Output:\n", result.stdout)

        # Check if login was successful
        if "LoginSuccess" in result.stdout:
            print("✅ Login was successful!")
            return True
        else:
            print("❌ Login failed!")
            return False

    except subprocess.CalledProcessError as e:
        print("❌ Error running TypeScript file:", e.stderr)
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
