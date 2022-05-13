import csv 
row = ['David', 'MCE', '3', '7.8'] 
row1 = ['Lisa', 'PIE', '3', '9.1'] 
row2 = ['Raymond', 'ECE', '2', '8.5'] 

with open('university_records.csv', 'a') as csv_file:
    writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL) 
    writer.writerow(row) 
    writer.writerow(row1) 
    writer.writerow(row2)