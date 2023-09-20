import requests
import os

def create_directory(dirname):
	#Creates a new directory if a directory with dirname does not exist

	try:
		os.stat(dirname)
	except:
		os.mkdir(dirname)

def show(obj):
	#Displays the items in the obj

	for i in range(len(obj)):
		print(str(i)+': '+str(obj[i]))

def auth():
	#Asks for the user details

	ask_auth = input("Do you want to download gists from your account
							? Type 'yes' or 'no': ")
	if(ask_auth=="yes"):
		user = input("Enter your username: ")
		password = input("Enter your password: ")
		request = requests.get('https://api.github.com/users/'+user+'/gists'
											, auth=(user, password))
	elif(ask_auth=="no"):
		user = input("Enter username: ")
		request = requests.get('https://api.github.com/users/'
													+user+'/gists')
	return [ask_auth, user, request]

def load(request):
#Loads the files and the gist urls

output = request.text.split(",")
gist_urls = []
files = []
for item in output:
	if "raw_url" in item:
		gist_urls.append(str(item[11:-1]))
	if "filename" in item:
		files.append(str(item.split(":")[1][2:-1]))
return [gist_urls, files]

def write_gist(filename, text):
	#Writes text(gist) to filename

	fp = open(filename, 'w')
	fp.write(text)
	fp.close()

def download(permission, user, request, fileno):
	#Loads and writes all the gists to <em>dirname</em>

	if(permission == "yes" or permission == "no"):
		gist_urls, files = load(request)
		dirname = user+"'s_gists/"
		create_directory(dirname)
		if(fileno[1] == "all"):
			for i in range(len(gist_urls)):
				gist = requests.get(gist_urls[i])
				write_gist(dirname+files[i], gist.text)
		else:
			for i in range(1,len(fileno)):
				gist = requests.get(gist_urls[int(fileno[i])])
				write_gist(dirname+files[int(fileno[i])], gist.text)

def detailed(urls, pos):
	#Prints out the contents of a file

	gist = requests.get(urls[int(pos)])
	print(gist.text)

def main():
	#Authenticates and downloads gists according to user's choice
	#Commands:
	#show: To show all the available gists with their assigned gistno
	#download all: To download all the available gists
	#download gistno(s): To download gist(s) assigned to gistno(s)
	#detailed gistno: To print content of gist assigned to gistno
	#exit: To exit the script

	ask_auth, user, request = auth()
	urls, files = load(request)
	try:
		while(1):
			command = input("Enter your command: ")
			if("download" in command):
				download(ask_auth, user, request, command.split(" "))
			elif("detailed" in command):
				detailed(urls, command.split(" ")[1])
			elif(command == "show"):
				show(files)
			elif(command == "exit"):
				return
	except:
		pass

if(__name__ == '__main__'):
	main()
