import re
import pandas as pd
def startsWithDateTime(s):
    pattern = '^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}), ([0-9][0-9]):([0-9][0-9]) ([\w]+) -'
    result = re.match(pattern, s)
    # print(result)
    if result:
        # print("hehe")
        return True
    # print('haha')
    return False


def startsWithAuthor(s):
    patterns = [
'([\w]+):','([\w]+[\s]+[\w]+):','([\w]+[\s]+[\w]+[\s]+[\w]+):','([+]\d{2} \d{5} \d{5}):','([+]\d{2} \d{3} \d{3} \d{4}):','([+]\d{2} \d{4} \d{7})']
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, s)
    if result:
        return True
    return False

def getDataPoint(line):
    # line = 18/06/17, 22:47 - Loki: Why do you have 2 numbers, Banner?
    
    splitLine = line.split(' - ') # splitLine = ['18/06/17, 22:47', 'Loki: Why do you have 2 numbers, Banner?']
    
    dateTime = splitLine[0] # dateTime = '18/06/17, 22:47'
    
    date, time = dateTime.split(', ') # date = '18/06/17'; time = '22:47'
    
    message = ' '.join(splitLine[1:]) # message = 'Loki: Why do you have 2 numbers, Banner?'
    
    if startsWithAuthor(message): # True
        splitMessage = message.split(': ') # splitMessage = ['Loki', 'Why do you have 2 numbers, Banner?']
        author = splitMessage[0] # author = 'Loki'
        message = ' '.join(splitMessage[1:]) # message = 'Why do you have 2 numbers, Banner?'
    else:
        author = None
    return date, time, author, message



parsedData = [] # List to keep track of data so it can be used by a Pandas dataframe
#conversationPath = './whatsappcollection/whatsapp_avengers.txt'
conversationPath = './testfile.txt'
with open(conversationPath, encoding="utf-8") as fp:
    fp.readline() # Skipping first line of the file (usually contains information about end-to-end encryption)
        
    messageBuffer = [] # Buffer to capture intermediate output for multi-line messages
    date, time, author = None, None, None # Intermediate variables to keep track of the current message being processed
    
    while True:
        line = fp.readline()
        # print(line) 
        if not line: # Stop reading further if end of file has been reached
            # print('Not line')
            break
        line = line.strip() # Guarding against erroneous leading and trailing whitespaces
        # print(line)
        if startsWithDateTime(line): # If a line starts with a Date Time pattern, then this indicates the beginning of a new message
            # print("Entered")
            if len(messageBuffer) > 0: # Check if the message buffer contains characters from previous iterations
                parsedData.append([date, time, author, ' '.join(messageBuffer)]) # Save the tokens from the previous message in parsedData
                # print("Entered")
            messageBuffer.clear() # Clear the message buffer so that it can be used for the next message
            date, time, author, message = getDataPoint(line) # Identify and extract tokens from the line
            messageBuffer.append(message) # Append message to buffer
        else:
            messageBuffer.append(line) # If a line doesn't start with a Date Time pattern, then it is part of a multi-line message. So, just append to buffer

#using pandas
df = pd.DataFrame(parsedData, columns=['Date', 'Time', 'Author', 'Message']) 
df.head(5)
# print(df)
