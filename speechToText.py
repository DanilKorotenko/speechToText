#!/usr/bin/python

import os, getopt, sys, json
import ntpath
import subprocess
import codecs
import base64

#return string
def encode_audio(audioFilePath):
	audioFile = open(audioFilePath, "r")
	audio_content = audioFile.read()
	audioFile.close();
	return base64.b64encode(audio_content)

def recogniseFile(audioFilePath, api_key, languageCode, verbose):
	print "Processing file: ", audioFilePath;
# 	print "Convert to flac";
	flacPath = audioFilePath + '.flac';
# 	print "flacPath: ", flacPath;
	cmd = 'afconvert -f flac  -d flac "' + audioFilePath + '" "' + flacPath + '"';
	os.system(cmd);
	print "Do recognition";

	audioContent = encode_audio(flacPath);
	request = {
		"config": {
			"encoding":"FLAC",
			"languageCode": languageCode,
		},
		"audio": {
			"content": audioContent
		}
	};

	jsonFile = open("request.json", "w");

	json.dump(request, jsonFile);

	jsonFile.close();

	recognitionCommand = 'curl -s -X POST -H "Content-Type: application/json" --data-binary @request.json "https://speech.googleapis.com/v1/speech:recognize?key='+ api_key +'"';
# 	print "recognitionCommand: ", recognitionCommand;

	responseJson = os.popen(recognitionCommand).read();

	try:
		response = json.loads(responseJson);
		if verbose ==False:
			print response['results'][0]['alternatives'][0]['transcript'];
		else:
			print response;
	except ValueError:
		print responseJson;

	print "********";

def main(argv):
	doRecognition = False;
	verbose = False;
	fileProcess = '';
	api_key = '';
	languageCode="ru";

	try:
		opts, args = getopt.getopt(argv,"hrvl:f:a:",["help", "recognize", "verbose", "language", "file","api-key"]);
	except getopt.GetoptError:
		sys.exit(2);


	for opt, arg in opts:
		if opt == '-h':
			print 'speechToText.py -u -r -f <filepath>';
			sys.exit();

		if opt in ("-r", "--recognize"):
			doRecognition = True;

		if opt in ("-v", "--verbose"):
			verbose = True;

		if opt in ("-f", "--file"):
# 			print "File is specified: ", arg;
			doRecognition = False;
			fileProcess = arg;

		if opt in ("-a", "--api-key"):
# 			print "API key is specified: ", arg;
			api_key = arg;

		if opt in ("-l", "--language"):
			languageCode = arg;

	if api_key == '':
		print "No API key specified."
		sys.exit();

	if doRecognition:
		print "Do recognition";

		directory = "/Users/danilkorotenko/Documents/ViberDownloads/PTT/";
		for filename in os.listdir(directory):
			if filename.endswith(".m4a"):
				fullPath = os.path.join(directory, filename);
				recogniseFile(fullPath, api_key, languageCode, verbose);

	if fileProcess:
		recogniseFile(fileProcess, api_key, languageCode, verbose);

if __name__ == "__main__":
	main(sys.argv[1:]);
