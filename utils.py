from wit import Wit

access_token = "WSHEZ4HUV4LDDBHNQU6FKGBCJCXFFB6D"

client = Wit(access_token= access_token)

def wit_response(message_text): 
    resp = client.message(message_text)
    entity = None
    value = None
    
    try:
        entity = list(resp["entities"])[0]
        value = resp["entities"][entity][0]["values"]
    except:
        pass
    return (entity,value)
    
    
    
#print (wit_response("Quais quadros voc�s tem disponivel ?"))