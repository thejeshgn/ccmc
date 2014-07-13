#https://pythonhosted.org/dbf/
import dbf
some_table = dbf.from_csv(csvfile='./export/csv/property_tax.csv', filename='./export/dbf/property_tax',field_names='zoneId,zone,wardNo,streetId,street,asstNo,nameAddr,category,hlfYrlyTax,penalty,total,typeOfBldg'.split(","), to_disk=True)