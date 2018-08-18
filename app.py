import os, sys
from flask import Flask, request
from pymessenger import Bot
from utils import wit_response

VERIFY_TOKEN = "botchat"

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAEgZC2rkEq0BAHZCM9RWb3zdCXyDKLv2eBDu3BZC8mWSexpHUHZAaE09bZAY43ErD9njtqSYZAFiQ0ZCZAFxYhHpDJt8pvbpqcBG3Pnu7V4aZCXskjXFKE9yrSQb8bsx3QfKThXuPevMgswr9n2fe6HIEj5UADUQKtweI7H7nZAUe93LBmFYmrQ5Y"

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route("/", methods=["GET"])

def verify_token():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismach", 403
        return request.args["hub.challenge"], 200
    return "Hello World", 200


@app.route("/", methods=["POST"])

def webhook():
    data = request.get_json()
    log(data)
    
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                
                #ID
                sender_id = messaging_event["sender"]["id"]
                recipient_id = messaging_event["recipient"]["id"]
                
                if messaging_event.get("message"):
                    #extract message
                    if "text" in messaging_event["message"]:
                        messaging_text = messaging_event["message"]["text"]
                    else:
                        messaging_text = "no text"
                  
                    response = None
                    entity, value = wit_response(messaging_text)
                    
                    #quadros
                    if entity == "quadros":
                        response = "Temos os seguintes modelos de quadros:%s" % entity
                        
                    #saudação    
                    if entity == "bom_dia":
                        response = "Olá, bom dia! :D, com o que posso ajudar ?%s" % entity
                        
                    #comprar    
                    if entity == "comprar":
                        response = "fico muito feliz em saber que você tem interesse em nossos quadros, entre em contato com a gente pelo nosso Whats App 12 99193-6303 ou só aguardar que entraremos em contato o quanto antes <3 :D %s" % entity
                    
                    #preço
                    if entity == "preco":
                        response = "Os valores dos nossos quadros vão de 39,99 o tamanho A4 e 49,99 o tamanho A3 %s" % entity
                    
                    if response == None:
                        response = "Desculpe, não entendi :/%s" % entity
                        
                    bot.send_text_message(sender_id, response)

    return "ok", 200

def log(message):
    print (message)
    sys.stdout.flush()
    
    
if __name__ == "__main__":
    app.run(debug=False, port=80)
