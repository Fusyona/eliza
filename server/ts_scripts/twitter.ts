import { Scraper } from "agent-twitter-client";

// Get credentials from command-line arguments
const args = process.argv.slice(2);
if (args.length < 4) {
    console.error("❌ Error: Missing arguments. Usage: npx ts-node twitter.ts <username> <password> <email> <2fa_secret>");
    process.exit(1);
}

const [username, password, email, twitter2faSecret] = args;

var twitterClient = new Scraper();

async function main() {

    var retries = 5;
    while (retries > 0) {
        try {
            if (await twitterClient.isLoggedIn()) {
                console.log("Already logged in!");
                console.log("LoginSuccess");
                process.exit(0);
            } else {
                await twitterClient.login(username, password, email, twitter2faSecret);
                if (await twitterClient.isLoggedIn()) {
                    console.log("Logged successfully!");
                    console.log("LoginSuccess");
                    process.exit(0);
                }
            }
        } catch (error) {
            console.log(`Login attempt failed: ${error.message}`);
        }
        retries--;
    }
    console.log("LoginFailure"); // ❌ Failure message
    process.exit(1);
}

main().catch((err) => {
    console.error("Unexpected error:", err);
    console.log("LoginFailure");
    process.exit(1);
});
