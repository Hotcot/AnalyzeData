import telepot
import time



class TelBot:
    
    __token = 'token your telegram bot' # telegram token
    __receiver_id = [id_channel_telegram] # https://api.telegram.org/bot<TOKEN>/getUpdates

    def __init__(self, current_data, result_theme):
        bot = telepot.Bot(self.__token)
        for item in range(len(current_data)):
            bot.sendMessage(self.__receiver_id, f"\nLink:\t\t\t{current_data['link'][item]}\n\nTheme:\t\t\t#{result_theme[item]}")
            time.sleep(3)

    
