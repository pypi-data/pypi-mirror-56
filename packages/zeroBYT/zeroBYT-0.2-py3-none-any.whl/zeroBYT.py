import os, time, numpy as np
from cryptography.fernet import Fernet
import matplotlib.pyplot as plt

vBin = ['544', '432', '252', '541', '441', '414', '555', '513', '322', '242',
        '152', '132', '342', '455', '253', '512', '531', '155', '352', '241',
        '532', '112', '344', '234', '412', '511', '141', '353', '521', '323',
        '153', '142', '453', '535', '345', '452', '121', '543', '552', '214',
        '231', '553', '534', '114', '522', '135', '424', '154', '354', '111',
        '244', '113', '331', '444', '215', '134', '355', '434', '133', '212',
        '251', '523', '451', '334', '144', '514', '411', '341', '324', '545',
        '124', '413', '255', '533', '145', '315', '313', '123', '213', '515',
        '211', '311', '122', '554', '314', '222', '332', '243', '321', '232',
        '542', '454', '223', '425', '351', '131', '443', '423', '125', '254',
        '335', '245', '221', '235', '325', '415', '435', '442', '225', '343',
        '233', '312', '525', '551', '431', '224', '433', '445', '151', '143',
        '333', '115', '422', '421', '524', '100','001', '010']
vChar = ['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07',
         '\x08', '\t', '\n', '\x0b', '\x0c', '\r', '\x0e', '\x0f', '\x10',
         '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', 
         '\x19', '\x1a', '\x1b', '\x1c', '\x1d', '\x1e', '\x1f', ' ', '!',
         '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', 
         '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', 
         '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 
         'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 
         'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 
         'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
         'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', 
         '}', '~', '\x80']

keyPath = ''
#Voltize the Encrypted Value
def toVolt(encrypted):
    en = ''
    try :
        encrypted = encrypted.decode()
    except : pass
    for i in encrypted:
        for j in range(len(vChar)):
            if i == vChar[j]:
                en += vBin[j]
    return en

#Unvoltize the Voltized Value and return the Encrypted value
def toUnvolt(volt):
    de = ''
    volt = [(volt[i:i+3]) for i in range(0, len(volt), 3)] 
    for i in volt:
        for j in range(len(vBin)):
            if i == vBin[j]:
                de += vChar[j]
    return de
    
#Convert String to Binary including Special CHaracters
def toBinary(word):
    try:
        binary = ''.join([format(ord(i),'08b') for i in word])
        return binary
    except:
        print("toBinary Error : Check the Input")

#Convert Binary to String including Special CHaracters
def toString(binary,n):
    try:
        binary = [(binary[i:i+n]) for i in range(0, len(binary), n)] 
       # word = ''.join([chr(i) for i in binary])
        return binary
    except:
        print("toString Error : Check the Input")
        
#Encrypt String to Bytes and save the Key in Key.txt
def toEncrypt(value):
    try:
        Key = Fernet.generate_key()
        with open('Key.txt', 'w') as f:
            f.write(Key.decode())
    except:
        with open('Key.txt', 'rb') as f:
            key = f.read()
            Key = key.encode()
    fernet = Fernet(Key)
    encrypted = fernet.encrypt(value.encode())
    return(encrypted)
        
#To Decrypt Bytes to String and uses the Key in Key.txt
def toDecrypt(encrypted):
    #Check for Key File Exists
    try:
        with open('Key.txt', 'r') as f:
            key = f.read()
            Key = key.encode()
        fernet = Fernet(Key)
        try :
            encrypted = encrypted.encode()
        except : pass
        decrypted = fernet.decrypt(encrypted)
        return(decrypted)
    #Print Error if the Key File doesn't Exists  
    except:
        print("toDecrypt Error : Key File is Missing")

#Returns the Words with Count for a File in Location
def countFile(fileLocation):
    #Check for File Exists
    if os.path.exists(fileLocation):
        ind_word = []
        count    = []
        with open(fileLocation, 'r') as f:
            message = f.read()
        message = message.lower()
        message = message.split()
        [ind_word.append(i) for i in message if not i in ind_word]
        ind_word.sort()
        [count.append(message.count(i)) for i in ind_word]
        #Returns the Individual_Words, Counts respectively
        return ind_word, count
    #Print Error if the File doesn't Exists            
    else:
        print("countFile Error : Check File Location")
        
#Returns the Words with Count for Multiple in Location
def countFolder(folderLocation):
    #Check for Folder Exists
    try:
        name  = []
        word  = [] 
        count = []
        files = os.scandir(folderLocation)
        files = [f.name for f in files if f.is_file()]
        for i in range(len(files)):
            w, c = countFile(folderLocation + files[i])
            name.append(files[i])
            word.append(w)
            count.append(c)
        #Returns the File_Name, Words, Counts respectively
        return name, word, count
    #Print Error if the Folder doesn't Exists
    except:
        print("countFile Error : Check Folder Location")
        
#Retrns and Print the Summary of the File
def summaryFile(fileLocation):
    wBin  = []
    summ  = ''
    try:
        #Call the countFile function
        w, c = countFile(fileLocation)
        #sMax for the Maximum Word display width 
        sMax = len(max(w, key=len)) + 4
        #Print the Summary of All Files
        summ += ("\nSummary : \n{x:<{x_w}}{y:<{y_w}}{z}".format(
                x=' Word', x_w = sMax, y = "Count", y_w = 3,z=' Binary'))
        for l in range(len(w)):
            bin = toBinary(w[l])
            summ += ("\n{x:<{x_w}}""{y:<{y_w}}{z}".format(x = w[l], x_w= sMax,
                  y = " " + str(c[l]), y_w = 5,z = "  " + str(bin)))
            wBin.append(str(bin))
        summ += ("\n-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")
        print( summ )
        #Returns the Words, Counts, Binary Values respectively
        return w, c, wBin, summ
    except : 
        print("summaryFile Error : Check File Location")
        
#Retrns and Print the Summary of the All Files in the Folder
def summaryFolder(folderLocation):
    wBin  = []
    word  = [] 
    count = []
    summ  = ''
    try:
        #Get the Names of the All Files
        n, _, _ = countFolder(folderLocation)
        #Print the Summary of All Files
        for i in n:
            summ += ("\nFile : " +  i)
            print("\nFile : " +  i)
            w, c, b, s = summaryFile(folderLocation + i)
            wBin.append(b)
            word.append(w)
            count.append(c)  
            summ += s
        #Returns the File_Name, Words, Counts, Binary Values respectively
        return n, word, count, wBin, summ
    except:
        print("summaryFolder Error : Check Folder Location")

#Returns the Both X and Y Axis Values for the Graph
def graph(volt):
    x_axis = []
    y_axis = []
    for i in range(len(volt)):
        x_axis.append(i)
        y_axis.append(volt[i])
    return x_axis, y_axis

#To Set the Path of the Key.txt
def setKeyPath(path):
    global keyPath
    keyPath = path
            
#To Convert Binary to Bipolar
def toBipolar(binary):
    bp = []
    for i in binary:
        if i == '0' :
            bp.append('-1')
        else:
            bp.append('1')
    return bp

#To form Square and Sine Wave and returns Coordinates
def squareSine(word, graph):
    xQ, yQ = squareWave(word, 0)
    xS, yS = sineWave(word, 0)
    #Plot the Graph if Graph is HIGH
    while graph:
        yQ = yQ[1:]+yQ[1:2]
        yS = yS[10:]+yS[:10]
        plt.plot(xS, yS, color='b')
        plt.step(xQ, yQ, color='r', where='post') 
        plt.axhline(0.5, color='g')
        plt.xlabel('Time') 
        plt.ylabel('Analog & Digital Values') 
        plt.title('Square & Sine Wave') 
        plt.show() 
        time.sleep(0.5)
    return xQ, yQ, xS, yS

#To form Sine Wave and returns Coordinates
def sineWave(word, graph):
    binary  = toBinary(word)
    xNew = []
    yNew = []
    xT   = []
    yT   = []
    direction   = -1
    #Loop to find the Zero Crossing Points on X-Axis
    s = int(not(binary[0]))
    for i in range(len(binary)):
        if s!=binary[i]:
            s=binary[i]
            xT.append(i)
            yT.append(binary[i])
    xT.append(len(binary)-1)
    yT.append(binary[-1])
    #Loop to find the Sine Wave Coordinates
    for i in range(len(xT)-1):
        d = (xT[i+1] - xT[i]) #Difference btw Two Zero Crossing Points - X
        for j in range(d*10):
            xNew.append(xT[i]+(j/10))
            if s:
                yNew.append((direction*np.sin(22/7*j/10/d)+1.0)/2.0)
            else:
                yNew.append((direction*np.sin(22/7*j/10/d)+1.0)/2.0)
        if direction == 1 :
            direction = -1
        else:
            direction = 1
    #Plot the Graph if Graph is HIGH
    while graph:
        yNew = yNew[1:]+yNew[1:2]
        plt.plot(xNew, yNew) 
        plt.axhline(0.5, color='g')
        plt.xlabel('Time') 
        plt.ylabel('Analog Representation') 
        plt.title('Sine Wave') 
        plt.show() 
        time.sleep(0.05)
    return xNew, yNew

#To plot the Square Wave Graph with Word
def squareWave(word, graph):
    binary  = toBinary(word)
    y = m = [int(i) for i in binary] 
    x = n = [i for i in range(len(y))]
    #Plot the Graph if Graph is HIGH
    while graph:
        tmp = y[0]
        for i in range(len(y)-1):
            y[i] = y[i+1]
        y[-1] = tmp
        plt.step(x, y, where='post') 
        plt.axhline(0.5, color='g')
        plt.xlabel('Time') 
        plt.ylabel('Digital Representation') 
        plt.title('Square Wave') 
        plt.show()
        time.sleep(0.5)
    return n, m   
    