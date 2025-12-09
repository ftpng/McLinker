# McLinker – Minecraft ↔ Discord Account Linking System

MCLINKER links a player's Minecraft account to their Discord account using a secure 6-digit verification code.  
The system is made of two parts:

- A **Minecraft plugin** (example code included)
- A **Discord bot** (fully functional)


## Plugin

- When a player joins the server, they are **immediately kicked** with a message containing a **6-digit verification code**.
- That code is saved into the **codes database**, along with:
  - Minecraft username
  - Minecraft UUID
  - Timestamp (`created_at`)

- ⚠️ The `/plugin` folder contains **only Java source code**.  It is **not a packaged plugin**. If you want to use it, you must turn it into a proper plugin yourself.


## Discord Bot
- `/link` Sends the user an ephemeral message with a button. The button opens a modal where they enter the 6-digit code from Minecraft.

- The bot checks:
  - If the code exists  
  - If the code is valid  
  - If the code is expired (expiration is handled **in Python**, not the plugin)
  - If the code belongs to a user currently linking

- If valid:
  - The Discord user is linked to the Minecraft UUID
  - The bot stores:
    - Discord user ID  
    - Minecraft UUID  
    - `linked_at` (Unix timestamp)
  - The code is deleted from the database

- `/unlink` Removes the link between a Discord user and their Minecraft account.
- `/who` Shows an embed with the linked Minecraft user's information.
- The bot also runs a scheduled cleanup task:
  - Every 60 seconds, expired codes (older than 5 minutes) are removed.


## Environment Variables

Copy `.env.example` → `.env` and fill in your values:

```env
TOKEN=BOT_TOKEN

CODES_DBUSER=db_user
CODES_DBPASS=db_pass
CODES_DBNAME=db_name
CODES_DBENDPOINT=db_host

DISCORD_DBUSER=db_user
DISCORD_DBPASS=db_pass
DISCORD_DBNAME=db_name
DISCORD_DBENDPOINT=db_host
```


## Databases

Why Two Databases?
- Codes database → Stores temporary verification codes
- Discord database → Stores permanent linked user records

This keeps temporary data separate and makes scaling or expanding the system easier.


## Support
If you run into any issues, bugs, or have other questions, feel free to DM me on Discord @ventros. thanks!