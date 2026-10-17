const { Client, GatewayIntentBits } = require('discord.js');
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });

client.on('ready', () => {
  console.log(`BOT MVR-BOT ONLINE bos! ${client.user.tag}`);
});

client.on('messageCreate', (message) => {
  if (message.content === '!ping') message.reply('PONG! Bot MVR online bos! 🔥');
  if (message.content === '!bantuan') message.reply('Halo bos MVR! Bot udah online 24 jam!');
});

client.login(process.env.TOKEN);
