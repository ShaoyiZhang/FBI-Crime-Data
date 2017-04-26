file_object = open('citylist2.txt')
list_all_city = file_object.readlines()
http = "https://en.wikipedia.org/wiki/"
for i in range(0,len(list_all_city)):
	list_all_city[i]=list_all_city[i].rstrip()
	list_all_city[i]=list_all_city[i].replace(' ','_')
	list_all_city[i]=http+list_all_city[i]

print(list_all_city)