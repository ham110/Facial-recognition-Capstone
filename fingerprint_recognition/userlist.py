import csv
#def removestatus(id):
#    with open('names.csv','r') as userfile:
#        reader = csv.DictReader(userfile)
#        data = list(reader)
#    with open('names.csv','w') as userfile:
#        writer = csv.DictWriter(userfile, ['rfid','part','status'])
#        writer.writeheader()
#        for row in data:
#            if row['rfid'] == str(id):
#                tempdict = {'rfid' : row['rfid'],'part' : row['part'],'status' : 'Rented Out'}
#                writer.writerow(tempdict)
#            else:
#                writer.writerow(row)
#    return
            
def returnuser(id, name):
    isavail = False
    with open('names.csv','r') as userfile:
        reader = csv.DictReader(userfile)
        data = list(reader)
    with open('names.csv','w') as userfile:
        writer = csv.DictWriter(userfile, ['rfid','name'])
        writer.writeheader()
        for row in data:
            if row['rfid'] == str(id) and row['name'] == str(name):
                isavail = True
            writer.writerow(row)
    return isavail

def adduser(id,name):
    with open('names.csv','a') as userfile:
        writer = csv.DictWriter(userfile, ['rfid','name'])
        tempdict = {'rfid' : str(id),'name' : str(name)}
        writer.writerow(tempdict)
    return

#def removestatus(id):
#    with open('names.csv','r') as userfile:
#        reader = csv.DictReader(userfile)
#        data = list(reader)
#    with open('names.csv','w') as userfile:
#        writer = csv.DictWriter(userfile, ['rfid','part','status'])
#        writer.writeheader()
#        for row in data:
#            if not row['rfid'] == str(id):
#                writer.writerow(row)
#    return
