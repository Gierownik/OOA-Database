# Out of Action Augments Discord Bot

## Changes Log

### 🔄 Added `/update-augments` Command

I've enhanced the Discord bot with a new command that allows administrators to update the augments database directly from Discord:

1. **Added new slash command:** `/update-augments` - Fetches the latest augments data from the wiki and updates the bot's database
2. **Security:** Command restricted to server administrators using Discord's permission system
3. **Feedback:** The bot provides detailed success/error messages with data about the update

### 🛠️ Technical Implementation

1. Modified `discord-bot.js`:
   - Added PermissionFlagsBits import for permission handling
   - Changed augments from const to let to allow reloading
   - Added new slash command definition with admin permissions
   - Implemented command handler with proper error handling

2. Enhanced `enhanced-scraper.js`:
   - Made the scraper module properly exportable
   - Added return value to the main function
   - Made the script conditionally run only when directly executed

## Usage Instructions

### Regular Augment Lookup
- Use `/augment name:<augment name>` to look up information about a specific augment
- The bot will find the closest match and display its effects

### Updating the Augments Database (Admin Only)
- Use `/update-augments` to trigger a fresh scrape of the wiki
- The bot will:
  - Scrape the latest augment data from the wiki
  - Update the augments.json file
  - Reload the data into memory
  - Display a success message with the number of augments updated

## Development Next Steps

Potential improvements for future development:
- Add cooldown to prevent abuse of the update command
- Implement logging for update operations
- Add status tracking for long-running updates
- Create a backup system for the augments data

## Setup and Testing Instructions

### Setting Up the .env File
1. Create a `.env` file in the root directory of the project
2. Add the following environment variables:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   CLIENT_ID=your_discord_application_client_id
   ```
3. Replace placeholders with your actual Discord bot credentials:
   - `your_discord_bot_token`: The token from your Discord bot's settings
   - `your_discord_application_client_id`: The application ID from Discord Developer Portal

### Getting Discord Bot Credentials
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application or select an existing one
3. Go to the "Bot" tab and click "Reset Token" to get your bot token
4. Copy your Application ID from the "General Information" tab

### Testing the Bot Locally
1. Install dependencies if not already installed:
   ```
   npm install
   ```
2. Make sure you have the `augments.json` file in your project root
3. Start the bot:
   ```
   node discord-bot.js
   ```
4. You should see "Logged in as [your bot name]!" in the console
5. The bot will also register/update the slash command
6. Invite the bot to your Discord server using the OAuth2 URL generator:
   - Go to OAuth2 > URL Generator
   - Select scopes: `bot` and `applications.commands`
   - Select permissions: `Send Messages`, `Embed Links`, etc.
   - Use the generated URL to add the bot to your server

### Using the Bot in Discord
- Use the `/augment name:[augment name]` command to search for augments
- The bot will find and display information about the closest matching augment 

## Required Bot Permissions

The bot requires the following permissions to function properly:

### Bot Intents (Set in Discord Developer Portal)
- SERVER MEMBERS INTENT (Guilds)
- MESSAGE CONTENT INTENT
- SERVER MESSAGES INTENT (Guild Messages)

### Bot Permissions (When Adding to Server)
- **General Permissions:**
  - View Channels
  - Send Messages
  - Embed Links
  - Read Message History
  - Use Slash Commands

### Configuring Bot Permissions
1. **Setting Intents:**
   - In the Discord Developer Portal, navigate to your application
   - Go to the "Bot" tab
   - Under "Privileged Gateway Intents", enable:
     - SERVER MEMBERS INTENT
     - MESSAGE CONTENT INTENT
     - SERVER MESSAGES INTENT

2. **When Inviting the Bot:**
   - In the OAuth2 URL Generator, select:
     - Scopes: `bot` and `applications.commands`
     - Bot Permissions: 
       - Read Messages/View Channels
       - Send Messages
       - Embed Links
       - Read Message History
       - Use Application Commands

These permissions match the intents defined in the code:
```javascript
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});
``` 