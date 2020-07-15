#Pip search выдает несколько библиотек для перевода, выбрал эту
import googletrans,json

#функция для выполнения перевода
def trans (fC = "Ok", src="en", dest = "ru", translator = googletrans.Translator()):
    """fC - строка для перевода
    src = "en" - язык источника 
    dest = "ru" - язык назначения
    translator = googletrans.Translator() - объект библиотеки переводчика
    
    """
    isMistake = False
    translation ="n/a"
    mistakeValue = [""]
    notTranslated = ""
    tr = translator.translate(fC, src="en", dest = dest)
    if tr.extra_data["possible-mistakes"] != None:
        isMistake = True
        mistakeValue = tr.extra_data
    elif tr.origin == tr.text:
        if tr.extra_data["all-translations"] != None:
            #Библиотека не смогла определиться с вариантом перевода, берем первый из предложенных
            translation = tr.extra_data["all-translations"][0][1][0] +" <-> "+tr.origin+"\n"
        else:
            #Здесь какая-то фича библиотеки. То что вываливается здесь, вполне корректно переводится, если лежит в урезанном файле. Отправляем на доработку
            notTranslated = fC
    else:
        #Все перевелось без ошибок
        translation = tr.origin + " <-> " + tr.text + "\n"
    
    return isMistake, translation, notTranslated, mistakeValue

#Имя файда для перевода (предполагается, что всегда в корне со скриптом)
importFileName="aecc0f7831e69e86.txt"

#Языки, перечисленные в сопроводительном письме
langs=['Spanish','Russian','German','Finnish','French','Italian','Japanese','Dutch','Portuguese','Turckish','Chinese']

#Ограничение на количество строк для перевода
lenFileContent = 1000

okTranslator,okFile = False,False

try:
    translator = googletrans.Translator()
    tr = translator.translate("Allow to translate", src="en", dest = "ru")
    okTranslator = True
except:
    print("Переводчик недоступен")

try:
    with open(importFileName,'r',encoding='utf-8') as linesToTranslate:
        fileContent = linesToTranslate.readlines()
        okFile = True
except:
    print("Нет файла для обработки")
    
if okTranslator == True and okFile==True:
    
    if len(fileContent) > 0 and len(fileContent) < 1000:
        lenFileContent = len(fileContent)
    elif len(fileContent) == 0:
        lenFileContent = 0
    
    fileContentToProcess = []
    for i in fileContent[0:lenFileContent+1]:
        #не совсем понятно, что делать со строками, которые больше тысячи. Принято решение отбросить
        if len(i) < 1000:
            fileContentToProcess.append(i.replace("\n",""))
    
    if len(fileContentToProcess) > 0:
        #Смотрим все доступные ключи dest языков в библиотеке
        for dest in googletrans.LANGUAGES.keys():
            #Смотрим те языки, на которые нужно перевести
            for lang in langs:
                #если значение языка в библиотеке и требуемое значение языка совпадают, забираем ключ (i) и переводим
                if lang.lower() == googletrans.LANGUAGES[dest]:
                    exportList = []
                    possibleMistakes = []
                    possibleMistakesCounter = 0
                    translatedFileName = 'translated_to_'+googletrans.LANGUAGES[dest]+'.txt'
                    possibleMistakesFileName = 'possible_mistakes_'+googletrans.LANGUAGES[dest]+'.txt'
                   
                    with open(translatedFileName,"w",encoding='utf-8') as fileToWrite:
                        print("Файл " + translatedFileName + " перезаписан")
                    with open(possibleMistakesFileName,"w",encoding='utf-8') as fileToWrite:
                        print("Файл " + possibleMistakesFileName + " перезаписан")

                    eqOriginText = []
                    for fC in fileContentToProcess:
                        isMistake, translation, notTranslated, mistakeValue = trans (fC = fC, src="en", dest = dest, translator = translator)
                        
                        if isMistake == True:
                            possibleMistakes.append(mistakeValue)
                            possibleMistakesCounter = possibleMistakesCounter + 1
                        elif len(notTranslated) > 0:
                            eqOriginText.append(notTranslated)
                        else:
                            exportList.append(translation)

                    for i in eqOriginText:
                        """если в продакшен, то по идее, вместо for нужен while до тех пор пока все не переведет,
                        и если останутся непереводимые, то с какой-то реакцией, 
                        например, ручной разбор или на мыло лингвисту и т.п.
                        Лингвисту писать лениво :), ограничусь одним перебором
                        
                        """
                        
                        isMistake, translation, notTranslated, mistakeValue = trans (fC = i, src="en", dest = dest, translator = translator)
                        if isMistake == False and translation == "n/a":
                            exportList.append(notTranslated +" <!> "+notTranslated+"\n")
                        elif isMistake == False and translation != "n/a": 
                            exportList.append(translation)
                        elif isMistake == True:
                            possibleMistakes.append(mistakeValue)
                            possibleMistakesCounter = possibleMistakesCounter + 1
                  
                    with open(translatedFileName,"a",encoding='utf-8') as fileToWrite:
                        for i in exportList:
                            fileToWrite.write(i)
                    print("Перевод на язык "+lang+" завершен")
                    
                    with open(possibleMistakesFileName,"a",encoding='utf-8') as fileToWrite:
                        json.dump(possibleMistakes,fileToWrite) 
                     
                    print("При переводе на "+lang+" зафиксировано "+str(possibleMistakesCounter)+" ошибок")
    else:
        print("Не оказалось строк в файле для обработки")
        

