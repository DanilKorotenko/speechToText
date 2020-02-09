#!/usr/bin/python
import os, getopt, sys, json

def main(argv):
    updateStorage = False
    doRecognition = False
    try:
        opts, args = getopt.getopt(argv,"hur",["update","recognize"])
    except getopt.GetoptError:
        print 'speechToText.py -u -r'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'speechToText.py -u -r'
            sys.exit()
        elif opt in ("-u", "--update"):
            updateStorage = True
        elif opt in ("-r", "--recognize"):
            doRecognition = True

    if updateStorage:
        print "Updating storage..."
        os.system('for i in ~/Documents/ViberDownloads/PTT/*.m4a; do baseFilename=`basename "${i}" .m4a` && afconvert -f flac  -d flac "${i}" "${baseFilename}.flac"; done')

        os.system('gsutil cp ~/*.flac gs://optimum-habitat-169407/')

#         os.system('rm ~/Documents/ViberDownloads/PTT/*.m4a')

#         os.system('*.flac')

        sys.exit()

    if doRecognition:
        print "Do recognition"
        ##os.system('gsutil ls -r gs://optimum-habitat-169407/**')

#        responseJson = "{ \"results\": [ { \"alternatives\": [ { \"confidence\": 0.9527583, \"transcript\": \"\u041d\u0443 \u044f \u0445\u043e\u0447\u0443 \u0442\u0435\u0431\u0435 \u0441\u043a\u0430\u0437\u0430\u0442\u044c \u0447\u0442\u043e\" } ] } ] }"

#        response = json.loads(responseJson)

        listOfFiles = os.popen('gsutil ls -r gs://optimum-habitat-169407/**').read().split('\n')

        for c in listOfFiles:
            if not c:
                continue
            recognitionCommand = "gcloud ml speech recognize %s --language-code='ru'" % (c)
            responseJson = os.popen(recognitionCommand).read()
            response = json.loads(responseJson)
            print "File ", (c)
            print response['results'][0]['alternatives'][0]['transcript']
            print "********"
#            break

if __name__ == "__main__":
    main(sys.argv[1:])


