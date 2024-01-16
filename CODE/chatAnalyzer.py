from  collections import Counter
import re
MESSAGE_LIST_BY_USER = []

RAW_DATA_FOLDER = "../DATA/Raw/"
CLEAN_DATA_FOLDER = "../DATA/Clean"
RAW_DATA_NAME = "_chat.txt"
CLEAN_DATA_NAME = "cleanChat.txt"



def main():
    print("---------------------------")
    print("-- WHATSPP CHAT ANALYZER --")
    print("---------------------------")
    trasforma_file()
    displayChatInfo()
   
#STEP 1 clean the raw chat data removing date, :  final result will be name message
def trasforma_file():
    with open(RAW_DATA_FOLDER+RAW_DATA_NAME, 'r', encoding='utf-8') as file_input, open(CLEAN_DATA_FOLDER+CLEAN_DATA_NAME, 'w', encoding='utf-8') as file_output:
        for linea in file_input:
            # Estrai utente e messaggio utilizzando espressioni regolari
            match = re.match(r"\[\d{2}/\d{2}/\d{2}, \d{2}:\d{2}:\d{2}\] (.+?): (.+)", linea)
            if match:
                utente = match.group(1)
                messaggio = match.group(2).lower()
                
                # Scrivi utente e messaggio nel file di output
                file_output.write(f"{utente} \t {messaggio}\n")    
                            

class Messaggio:
    def __init__(self, nome, messaggio):
        self.nome = nome
        self.messaggi = [messaggio]

#STEP 2 create a list of user and their messages
def groupMembersChat():
    result = []

    with open(CLEAN_DATA_FOLDER+CLEAN_DATA_NAME, 'r', encoding='utf-8') as file:
        rows = file.readlines()

        for row in rows:
            parts = row.strip().split('\t')
            
            if len(parts) == 2:
                user, message = parts
                user = user.strip()
                message = message.strip()

                existingMessage = False
                for oggetto in result:
                    if oggetto.nome == user:
                        oggetto.messaggi.append(message)
                        existingMessage = True
                        break

                if not existingMessage:
                    result.append(Messaggio(user, message))
    return result
                        

def getTotalMessSent(dataSet):
    total = 0
    for element in dataSet:
        total += len(element.messaggi)
            
    return total

#STEP 3 calculating all statistics 
def getStats(dataSet, word):
    totale = getTotalMessSent(dataSet)
    userStats = [] 
        
    for oggetto in dataSet:
        all_words = [sub.split() for sub in oggetto.messaggi]
        word_counts = Counter(word for sublist in all_words for word in sublist)
        mostSentWord = Counter(word_counts).most_common(1)[0][0]
        
        howManyTimesUsedTheWord = 0
        messaggi_unificati = ' '.join(oggetto.messaggi)
        parole = messaggi_unificati.split()
        howManyTimesUsedTheWord = parole.count(word)
        
        parole_uniche = set(parole)
        uniqueWordByUser = list(parole_uniche)[:5]

        words = Counter(word_counts).most_common(5)
        fiveMostSentWords = [parola for parola, _ in words]
        
        memberInfo = {
            "totalMessageSent": len(oggetto.messaggi),
            "avgMessageSent": (len(oggetto.messaggi)/totale)*100,
            "mostSentWord": mostSentWord,
            "5mostSentWord":fiveMostSentWords,
            "howManyTimes":howManyTimesUsedTheWord,
            "uniqueWords":uniqueWordByUser
        }
            
        userStats.append({oggetto.nome:memberInfo}) 
        
    
    return userStats
      

#STEP 4 printing all stats 
def displayChatInfo():
    word = "ok" #insert the word you want search
    dataSet = groupMembersChat() 
    totale = getTotalMessSent(dataSet)
    userStats = getStats(dataSet, word)
    
    for el in userStats:
        for user, stats in el.items():
            print("statistiche di ", user)
            print("Numero di Messaggi inviati: ", stats['totalMessageSent'])
            print("Media dei Messaggi: ", stats['avgMessageSent'])
            print("Parola + usata: ", stats['mostSentWord'])
            print(f"Quante Volte ha detto {word}:", stats['howManyTimes'])
            print("Parole uniche: ", stats['uniqueWords'])
            print("Le 5 parole piu usate: ", stats['5mostSentWord'])
            
            print("----------------------")

    print("Numero di messaggi inviato: ", totale)
    

if  __name__ == "__main__":
    main()
    