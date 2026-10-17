const { Client, GatewayIntentBits, EmbedBuilder } = require('discord.js');
const { joinVoiceChannel, createAudioPlayer, createAudioResource, AudioPlayerStatus, getVoiceConnection } = require('@discordjs/voice');
const play = require('play-dl');

const client = new Client({
  intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent, GatewayIntentBits.GuildVoiceStates]
});

const queues = new Map();

client.on('ready', () => {
  console.log(`JOCKIE MVR ONLINE BOS! ${client.user.tag}`);
  client.user.setActivity('!help | Jockie MVR', { type: 2 });
});

async function playSong(guildId) {
  const queue = queues.get(guildId);
  if (!queue || queue.songs.length === 0) {
    queues.delete(guildId);
    queue.connection.destroy();
    return;
  }
  const song = queue.songs[0];
  const stream = await play.stream(song.url);
  const resource = createAudioResource(stream.stream, { inputType: stream.type });
  queue.player.play(resource);
  
  const embed = new EmbedBuilder()
    .setColor('#FF0000')
    .setTitle('🎶 Now Playing - Jockie MVR')
    .setDescription(`**[${song.title}](${song.url})**\nRequest by: <@${song.requester}>`)
    .setThumbnail(song.thumbnail)
  queue.textChannel.send({ embeds: [embed] });
}

client.on('messageCreate', async (message) => {
  if (message.author.bot) return;
  const args = message.content.split(' ');
  const command = args[0].toLowerCase();

  if (command === '!play' || command === '!p') {
    const query = args.slice(1).join(' ');
    if (!query) return message.reply('**Usage:** `!play <judul lagu / link>`\nContoh: `!play dj tiktok viral`');
    
    const vc = message.member.voice.channel;
    if (!vc) return message.reply('❌ Masuk VC dulu bos!');

    let songInfo = await play.search(query, { limit: 1 });
    if (songInfo.length === 0) return message.reply('❌ Lagu gak ketemu bos!');
    songInfo = songInfo[0];

    const song = {
      title: songInfo.title,
      url: songInfo.url,
      thumbnail: songInfo.thumbnails[0]?.url,
      requester: message.author.id
    };

    let queue = queues.get(message.guild.id);
    if (!queue) {
      const connection = joinVoiceChannel({ channelId: vc.id, guildId: message.guild.id, adapterCreator: message.guild.voiceAdapterCreator });
      const player = createAudioPlayer();
      connection.subscribe(player);
      player.on(AudioPlayerStatus.Idle, () => {
        queue.songs.shift();
        playSong(message.guild.id);
      });
      queue = { textChannel: message.channel, connection, player, songs: [] };
      queues.set(message.guild.id, queue);
    }

    queue.songs.push(song);
    if (queue.songs.length === 1) {
      message.reply(`✅ **Ditambahkan ke antrian:** ${song.title}`);
      playSong(message.guild.id);
    } else {
      message.reply(`✅ **Antrian #${queue.songs.length}:** ${song.title}`);
    }
  }

  if (command === '!skip' || command === '!next' || command === '!s') {
    const queue = queues.get(message.guild.id);
    if (!queue) return message.reply('❌ Gak ada lagu bos!');
    queue.player.stop();
    message.reply('⏭️ Skip bos!');
  }
  if (command === '!stop' || command === '!leave' || command === '!dc') {
    const queue = queues.get(message.guild.id);
    if (!queue) return message.reply('❌ Bot gak di VC bos!');
    queue.songs = [];
    queue.player.stop();
    message.reply('⏹️ Bye bye bos!');
  }
  if (command === '!queue' || command === '!q') {
    const queue = queues.get(message.guild.id);
    if (!queue || queue.songs.length === 0) return message.reply('❌ Antrian kosong bos!');
    const list = queue.songs.map((s, i) => `${i === 0 ? '🎶 **Now:**' : `${i}.`} ${s.title}`).join('\n').slice(0, 1900);
    message.reply(`**Antrian Jockie MVR:**\n${list}`);
  }
  if (command === '!help') {
    message.reply(`**JOCKIE MVR - COMMAND LIST BOS:**
\`!play / !p\` - Play lagu
\`!skip / !s\` - Skip
\`!queue / !q\` - List antrian
\`!stop / !leave\` - Stop & leave
\`!pause / !resume\` - Pause / resume

**Mirip Jockie Music bos!**`);
  }
});

client.login(process.env.TOKEN);
