from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.update import Update
import time, sys, logging

from project.classifier.datatool import preprocess
sys.path.append("project/classifier/")
from project.controller import Controller
from project.classifier import datatool

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

"""
python-telegram-bot==12.0.0で動作確認済み
"""
class MMIBot:
    def __init__(self):
        self.user_context = {}
        # アクセストークン
        self.token = "2061219908:AAFqA7nZQnfGhyw2lt1DBiMolcsPySVVI94"
        # 1対話の長さ(ユーザの発話回数)．ここは固定とする
        self.dialogue_length = 15
        # システムからの最初の発話
        self.init_utt = "湯川先輩お疲れ様です! 今お時間いいですか?"
        self.rule_path = "./project/rule/"
        # self.controller = Controller(self.rule_path)
        self.user_controller = {}

    def start(self, bot, update):
        # 対話ログと発話回数を初期化
        self.user_context[update.message.from_user.id] = {"context": [], "count": 0}
        self.user_controller[update.message.from_user.id] = Controller(self.rule_path)
        update.message.reply_text(self.init_utt)


    def message(self, bot, update):
        if update.message.from_user.id not in self.user_context:
            self.user_context[update.message.from_user.id] = {"context": [], "count": 0}

        # ユーザ発話の回数を更新
        self.user_context[update.message.from_user.id]["count"] += 1

        # ユーザ発話をcontextに追加
        self.user_context[update.message.from_user.id]["context"].append(update.message.text)

        # controllerのreplyメソッドによりcontextから発話を生成
        send_message = self.user_controller[update.message.from_user.id].reply(self.user_context[update.message.from_user.id]["context"])

        # 送信する発話をcontextに追加
        self.user_context[update.message.from_user.id]["context"].append(send_message)

        # 発話を送信
        update.message.reply_text(send_message)

        if self.user_context[update.message.from_user.id]["count"] >= self.dialogue_length:
            # 対話IDは unixtime:user_id:bot_username
            unique_id = str(int(time.mktime(update.message["date"].timetuple()))) + u":" + str(update.message.from_user.id) + u":" + bot.username

            update.message.reply_text(u"_FINISHED_:" + unique_id)
            update.message.reply_text(u"対話終了です．エクスポートした「messages.html」ファイルを，フォームからアップロードしてください．")


    def run(self):
        updater = Updater(self.token)

        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start", self.start))

        dp.add_handler(MessageHandler(Filters.text, self.message))

        updater.start_polling()

        updater.idle()

if __name__ == '__main__':
    mybot = MMIBot()
    mybot.run()

