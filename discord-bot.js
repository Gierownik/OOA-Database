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
const weapons = JSON.parse(fs.readFileSync('weapons.json', 'utf8'));

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
function findClosestWeapon(query) {
    const weaponNames = Object.keys(weapons);
    const Gmatches = stringSimilarity.findBestMatch(query.toLowerCase(), weaponNames.map(name => name.toLowerCase()));
    return weaponNames[Gmatches.bestMatchIndex];
}

/**
 * Create a Discord embed for an augment
 * @param {string} augmentName - The name of the augment
 * @param {string[]} effects
 * @param {string} weaponName 
 * @param {string[]} stats 
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
    const additionalEffects = effects.filter(effect => 
        effect.tagCheck('$')
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
    
    const cleanEffect = line => line.tagCheck('^') || line.tagCheck('@') || line.tagCheck('$')
    ? line.slice(0, 2) + line.slice(3)
    : line.startsWith('&')
    ? line.slice(1)
    : line;
    

    // Add fields for different types of effects
    if (positiveEffects.length > 0) {
        embed.addFields({
            name: '✅ Positive Effects',
            value: positiveEffects.map(cleanEffect).join('\n')
        });
    }
    if (additionalEffects.length > 0) {
        embed.addFields({
            name: '🔧 Additional Mechanics',
            value: additionalEffects.map(cleanEffect).join('\n')
        });
    }
    if (negativeEffects.length > 0) {
        embed.addFields({
            name: '❌ Negative Effects',
            value: negativeEffects.map(cleanEffect).join('\n')
        });
    }

    if (neutralEffects.length > 0) {
        embed.addFields({
            name: '📝 Other Effects',
            value: neutralEffects.map(cleanEffect).join('\n')
        });
    }
    
    if (foundation.length > 0) {
        embed.addFields({
            name: '⚙ Foundations',
            value: foundation.map(cleanEffect).join('\n')
        });
    }

    return embed;
}
function createGunEmbed(weaponName, stats) {
    const embed = new EmbedBuilder()
        .setColor('#db463b')
        .setTitle(weaponName)
        .setTimestamp();
        const Loadoutstats = stats.filter(stats => 
            stats.tagCheck('^')
        );
        const Mainstats = stats.filter(stats => 
            stats.tagCheck('@')
        );
        const cleanStat = line => line.tagCheck('^') || line.tagCheck('@')
        ? line.slice(0, 2) + line.slice(3)
        : line;
        
        
        if (Loadoutstats.length > 0) {
            embed.addFields({
                name: '⚙  Loadout',
                value: Loadoutstats.map(cleanStat).join('\n')
            });
        }
        if (Mainstats.length > 0) {
            embed.addFields({
                name: '🔧 Stats',
                value: Mainstats.map(cleanStat).join('\n')
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
const augallCommand = new SlashCommandBuilder()
    .setName('aug-all')
    .setDescription('Get information about all augments, split into pages')
    .addIntegerOption(option =>
        option.setName('page')
            .setDescription('Page number')
            .setRequired(true)
            .setMinValue(1)
            .setMaxValue(7) );
const weaponCommand = new SlashCommandBuilder()          
    .setName('weapon')
    .setDescription('Get information about a weapon')
    .addStringOption(option =>
        option.setName('name')
            .setDescription('The name of the weapon')
            .setRequired(true));

// Register slash commands
const rest = new REST({ version: '10' }).setToken(process.env.DISCORD_TOKEN);

(async () => {
    try {
        console.log('Started refreshing application (/) commands.');

        await rest.put(
            Routes.applicationCommands(process.env.CLIENT_ID),
            { body: [augmentCommand.toJSON(), augallCommand.toJSON(), weaponCommand.toJSON()] },
        );

        console.log('Successfully reloaded application (/) commands.');
    } catch (error) {
        console.error(error);
    }
})();

// Handle slash command interactions
client.on('interactionCreate', async interaction => {
    if (!interaction.isChatInputCommand()) return;

    if (interaction.commandName === 'augment') {
        const query = interaction.options.getString('name');
        const closestMatch = findClosestAugment(query);
        const effects = augments[closestMatch];

        if (!effects) {
            await interaction.reply('No augment found matching your query.');
            return;
        }

        const embed = createAugmentEmbed(closestMatch, effects);
        await interaction.reply({ embeds: [embed] });
    }

    else if (interaction.commandName === 'aug-all') {
        const page = interaction.options.getInteger('page');
        const perPage = 10;
        const allAugments = Object.entries(augments)
        const start = (page - 1) * perPage;
        const pageItems = allAugments.slice(start, start + perPage);
        const embeds = pageItems.map(([name, effects]) =>
            createAugmentEmbed(name, effects)
        );
    
        await interaction.reply({ embeds });
    }
    if (interaction.commandName === 'weapon') { 
        const queryGun = interaction.options.getString('name');
        const closestMatchGun = findClosestWeapon(queryGun);
        const stats = weapons[closestMatchGun];

        if (!stats) {
            await interaction.reply('No gun found matching your query.');
            return;
        }

        const embed = createGunEmbed(closestMatchGun, stats);
        await interaction.reply({ embeds: [embed] });
    }
});

// Handle ready event
client.once('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
});

// Login to Discord
client.login(process.env.DISCORD_TOKEN);