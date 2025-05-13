 require('dotenv').config();
const { Client, GatewayIntentBits, EmbedBuilder, SlashCommandBuilder, REST, Routes } = require('discord.js');
const stringSimilarity = require('string-similarity');
const fs = require('fs');
// Initialize Discord client
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});
String.prototype.tagCheck = function(char) {
    if (this.length >= 3 && this.charAt(2) === char) {
      return true;  
    }
    return false;  
  };

// Load augments data
const augments = JSON.parse(fs.readFileSync('augments.json', 'utf8'));

/**
 * Find the closest matching augment name using fuzzy matching
 * @param {string} query - The search query
 * @returns {string} - The closest matching augment name
 */
function findClosestAugment(query) {
    const augmentNames = Object.keys(augments);
    const matches = stringSimilarity.findBestMatch(query.toLowerCase(), augmentNames.map(name => name.toLowerCase()));
    return augmentNames[matches.bestMatchIndex];
}

/**
 * Create a Discord embed for an augment
 * @param {string} augmentName - The name of the augment
 * @param {string[]} effects - The effects of the augment
 * @returns {EmbedBuilder} - The Discord embed
 */
function createAugmentEmbed(augmentName, effects) {
    const embed = new EmbedBuilder()
        .setColor('#0099ff')
        .setTitle(augmentName)
        .setDescription('Effects:')
        .setTimestamp();

    // Split effects into positive and negative based on prefix
    const positiveEffects = effects.filter(effect => 
        effect.tagCheck('^')
    );
    const negativeEffects = effects.filter(effect => 
        effect.tagCheck('@')
    );
    const foundation = effects.filter(effect => 
        effect.startsWith('&')
    );

    const neutralEffects = effects.filter(effect => 
        !positiveEffects.includes(effect) && 
        !negativeEffects.includes(effect) &&
        !foundation.includes(effect)
    );
    

    // Add fields for different types of effects
    if (positiveEffects.length > 0) {
        embed.addFields({
            name: '✅ Positive Effects',
            value: positiveEffects.map(effect => effect).join('\n')
        });
    }
    if (negativeEffects.length > 0) {
        embed.addFields({
            name: '❌ Negative Effects',
            value: negativeEffects.map(effect => effect).join('\n')
        });
    }

    if (neutralEffects.length > 0) {
        embed.addFields({
            name: '📝 Other Effects',
            value: neutralEffects.map(effect => effect).join('\n')
        });
    }
    
    if (foundation.length > 0) {
        embed.addFields({
            name: '⚙ Foundations',
            value: foundation.map(effect => effect).join('\n')
        });
    }

    return embed;
}

// Define the slash command
const augmentCommand = new SlashCommandBuilder()
    .setName('augment')
    .setDescription('Get information about an augment')
    .addStringOption(option =>
        option.setName('name')
            .setDescription('The name of the augment')
            .setRequired(true));

// Register slash commands
const rest = new REST({ version: '10' }).setToken(process.env.DISCORD_TOKEN);

(async () => {
    try {
        console.log('Started refreshing application (/) commands.');

        await rest.put(
            Routes.applicationCommands(process.env.CLIENT_ID),
            { body: [augmentCommand.toJSON()] },
        );

        console.log('Successfully reloaded application (/) commands.');
    } catch (error) {
        console.error(error);
    }
})();

// Handle slash command interactions
client.on('interactionCreate', async interaction => {
    if (!interaction.isChatInputCommand()) return;
    if (interaction.commandName !== 'augment') return;

    const query = interaction.options.getString('name');
    const closestMatch = findClosestAugment(query);
    const effects = augments[closestMatch];

    if (!effects) {
        await interaction.reply('No augment found matching your query.');
        return;
    }

    const embed = createAugmentEmbed(closestMatch, effects);
    await interaction.reply({ embeds: [embed] });
});

// Handle ready event
client.once('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
});

// Login to Discord
client.login(process.env.DISCORD_TOKEN);