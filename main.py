from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from logic import *

bot = TeleBot(API_TOKEN)


statlist = "Winrate, KDA, Role, Class, Style, Difficulty, DamageType, Damage, Sturdiness, Crowd\\_control, Mobility"
champstatslist = "Class, Role, WR%, Pickrate, Banrate, KDA"

@bot.message_handler(commands=['info', 'start'])
def info(message):
    bot.send_message(message.chat.id, "Hello, I am a simple bot to provide you with stats for League of Legends champions! \n\n*Currently using last seasons' stats")


#make the keyboard to pick the stat
def make_stats_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    stats = champstatslist.split(", ")
    for stat in stats:
        button = InlineKeyboardButton(text=stat, callback_data=stat.lower())
        keyboard.add(button)
    return keyboard



#get the stats of a champion from their name
@bot.message_handler(commands=['finder'])
def find_champion(message):
    arguments = message.text.split()
    try:
        stat_name = arguments[1].lower()
        stat_value = arguments[2]
        
        #find the names of the champs off their values
        champions = manager.get_champion_off_stat(stat_name, stat_value)
        
        if champions:
            bot.reply_to(message, f"Here are all the champions that have {stat_value} as their {stat_name}: " + ", ".join(champions))
    
    except IndexError:
        bot.reply_to(
        message,
        (
            "The correct usage of `/find_champion` is:\n"
            "`/find_champion <stat_name> <stat_value>`\n"
            "For example: `/find_champion winrate 50`\n"
            f"The only acceptable stats are: {statlist}"
        ),
    parse_mode="MarkdownV2"
        )

@bot.message_handler(commands=['statinfo'])
def statinfo(message):
    arguments = message.text.split()
    try:
        stat = arguments[1]
        #im just gonna make answers a dictionary
        stats_explanations = {
        "winrate": "Winrate refers to the percentage of games in which a champion wins. It's calculated as the number of wins divided by the total number of games played with that champion.",
        "kda": "KDA stands for Kills, Deaths, and Assists. It's a ratio that measures a champion's performance in terms of kills and assists relative to their deaths. A high KDA generally suggests a strong champion.",
        "role": "Role refers to the primary position or function a champion is typically played in the game. Common roles are Top, Jungle, Mid, ADC (Attack Damage Carry), and Support.",
        "class": "Class refers to the champion's general archetype or category, which typically influences their playstyle. For example, a champion can be a Fighter, Mage, Assassin, Tank, or Marksman.",
        "style": "Style refers to whether a champion is mostly played with autoattacks or abilities. A rating of 1 means the champion is autoattack-oriented, while a rating of 10 means they are abilities-focused.",
        "difficulty": "Difficulty measures how hard it is to play a champion effectively. It generally considers the complexity of their abilities and the skill required to perform well with them.",
        "damagetype": "Damage type indicates the primary form of damage a champion deals. Common types are Physical, Magic, and True Damage.",
        "damage": "Damage refers to the total amount of damage a champion deals in a match. It can be measured in terms of their abilities, basic attacks, and other sources of damage output.",
        "sturdiness": "Sturdiness refers to a champion's ability to survive and endure damage. It often correlates with a champion's health, armor, and magic resistances.",
        "crowd_control": "Crowd Control (CC) refers to abilities that can disable or limit enemy champions, such as stuns, slows, snares, silences, etc.",
        "mobility": "Mobility refers to a champion's ability to move around the map quickly. Champions with high mobility can dodge attacks, engage/disengage, and maneuver through fights more effectively.",
        
        # From champstatslist
        "wr%": "WR% (Winrate Percentage) represents the percentage of games the champion wins. Higher winrates indicate champions that perform better in games.",
        "pickrate": "Pickrate refers to how often a champion is selected by players. A high pickrate indicates a champion is popular.",
        "banrate": "Banrate refers to the percentage of games where the champion is banned by players. Higher banrates suggest that a champion is perceived as strong or annoying.",
        "kda": "KDA (Kills, Deaths, Assists) is a measure of how well a champion performs in terms of their kills, assists, and deaths. A higher KDA indicates better performance."
        }
        bot.reply_to(message, stats_explanations[stat])
        
    except ValueError:
        bot.reply_to(message, f"The stat \"{stat}\" seems to not be one of the available stats. Here's a list of the stats that are supported:\n{statlist}")
    except IndexError:
        bot.reply_to(message, "You haven't included a stat you'd like to know about. The command goes:\n`/statinfo <statname>`", parse_mode="Markdown")    

@bot.message_handler(commands=['stats'])
def get_stats(message):
    arguments = message.text.split()
    try:
        champion_name = arguments[1]
        if manager.get_champion_stats(champion_name) != []:
            #make a button of multiple choices, aka what stat the user wants to see
            bot.champ = champion_name #i kinda cheat to store the name of the champion if the command goes through
            bot.reply_to(message, f"Which stat for {champion_name} would you like to know?", reply_markup=make_stats_keyboard()) #the 'stats' is supposed to be the stat picked, because the function returns multiple different stats in the same callback
        else:
            bot.reply_to(message, f"The champion \"{champion_name}\" isn't found in the database. Are you sure you've spelled their name correctly?\nThe first letter must be capital, and champions like Vel'Koz require the appostrophe!")
    except IndexError:
        bot.reply_to(message, "You've provided insufficent arguments. The correct usage of `/stats` is supposed to be:\n`/stats <champion_name>`", parse_mode="Markdown")    

@bot.message_handler(commands=['roles', 'role'])
def roles(message):
    try:
        arguments = message.text.split()
        role = arguments[1].upper()
        champions = manager.get_champion_off_role(role)
        role = [', '.join(tup) for tup in champions]
        role = ', '.join(role)

        if role != []:
            bot.reply_to(message, f"Here's a list of all the champs that go into that role: {role}")
        else:
            raise ValueError
    except:
        bot.reply_to(message, "The role you've written either doesn't exist, or you've spelt it wrong. Try again? Roles are top, jungle, mid, adc, and support, if you need to know.")



@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id, "Processing your request...")
    if call.data == "winrate":
        bot.send_message(call.message.chat.id, f"Let's see if they're actually good...\nThe champions' winrate is {manager.get_champion_stats(bot.champ)[0][6]}")
    elif call.data == "pickrate":
        bot.send_message(call.message.chat.id, f"Are they actually that popular? I guess their pickrate is {manager.get_champion_stats(bot.champ)[0][8]}")
    elif call.data == "kda":
        bot.send_message(call.message.chat.id, f"{bot.champ} sounds like an inter champ, let's check out their KDA... It's {manager.get_champion_stats(bot.champ)[0][10]}")
    elif call.data == "role":
        bot.send_message(call.message.chat.id, f"What role do you think they have in the game? I know it's {manager.get_champion_stats(bot.champ)[0][2]} though.")
    elif call.data == "banrate":
        bot.send_message(call.message.chat.id, f"Ugh, {bot.champ} seems annoying. Let's check if the people think the same. Their banrate is {manager.get_champion_stats(bot.champ)[0][9]}")
    elif call.data == "class":
        bot.send_message(call.message.chat.id, f"You think they have their niche? I mean, they are a {manager.get_champion_stats(bot.champ)[0][1]} afterall...")
    else:
        bot.send_message(call.message.chat.id, f"Hey, that's not in the options! Did you missclick?")




#i got lazy and asked chatGPT to make the help command.
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "Here are the available commands to help you navigate the bot:\n\n"
        "<b>/info</b> or <b>/start</b> - Shows basic information about the bot and what it does.\n"
        "<b>/finder</b> <i>stat_name</i> <i>stat_value</i> - Find champions based on a specific stat and value. For example: <code>/find_champion winrate 50</code>.\n"
        "<b>/statinfo</b> <i>stat_name</i> - Get detailed information on a specific stat (e.g., Winrate, KDA, etc.).\n"
        "<b>/stats</b> <i>champion_name</i> - Get stats for a specific champion and choose which stat to explore. You'll be prompted to choose between stats like Winrate, KDA, etc.\n"
        "<b>/roles</b> or <b>/role</b> <i>role</i> - Find champions based on a given role (e.g., Top, Jungle, Mid, ADC, Support).\n\n"
        "For more information, simply use the <b>/statinfo</b> command followed by a stat name (e.g., <code>/statinfo winrate</code>) to get a list of available stats."
    )
    bot.reply_to(message, help_text, parse_mode="HTML")



if __name__ == '__main__':
    manager = DBManager(DATABASE)
    bot.infinity_polling()
    