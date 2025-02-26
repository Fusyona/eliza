import { Scraper } from "agent-twitter-client";

var twitterClient = new Scraper();
var username = "AnitaTentation";
var password = "nonlucrativeaccount123*";
var email = "dbytestingemail@gmail.com";
var twitter2faSecret = "DCQA23ESULMED5ZT";

async function main() {

        console.log("Hello, TypeScript!");
        var retries = 5;
        while (retries > 0) {
            try {
            if (await twitterClient.isLoggedIn()) {
                console.log("Already logged in!");
                console.log("LoginSuccess");
                process.exit(0);
                break;
            } else {
                await twitterClient.login(
                    username,
                    password,
                    email,
                    twitter2faSecret
                    );
                    if (await twitterClient.isLoggedIn()) {  
                        console.log("Logged successfully!");
                        console.log("LoginSuccess");
                        process.exit(0);
                    }
                }
            } catch (error) {
                console.log(`Login attempt failed: ${error.message}`)
                
            }
            retries--;
        }
        console.log("LoginFailure"); // ❌ Failure message
        process.exit(1);
    }
    main().catch((err) => {
        console.error("Unexpected error:", err);
        console.log("LoginFailure"); // Ensure Python gets a failure message
        process.exit(1);
    });