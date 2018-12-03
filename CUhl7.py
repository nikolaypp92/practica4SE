#Practica 4 Salud Electronica
#Autores: NIkolay Petkov Petkov, Alexander Aldoshin Tropeiko

import hl7
import os
import pydicom
from shutil import copyfile



while True :
    fileName = input("Introduce el nombre del archivo con mensajes HL7:")
   
    try:
        archivo = open(fileName, 'r').read()
        break
    except:
        print('El archivo: '+fileName+' no fue encontrado!')
while True :
    try:
        pathDicom = input("Introduce el nombre del directorio con imagenes medicas DICOM:")
        carpeta = os.listdir(pathDicom)
        break
    except:
        print('El directorio con nombre: '+pathDicom+' no fue encontrado!')
    
archivo = archivo.replace("\n", "\r")

mensajes =[]
c1 = -1
try:
    for i in archivo.split("\r"):
        
        
        if len(i) > 0:
            if i[0:3] == 'MSH':
                c1 +=1
                mensajes.append(i)
            mensajes[c1] = mensajes[c1]+i+'\r'
            

    parsedMensajes = []

    for i in mensajes:
        
        parsedMensajes.append(hl7.parse(i))

    for i in parsedMensajes:
        if str(i.segments('MSH')[0][3]) == 'IMAGE_PROC_V56':
            name = str(i.segments('PID')[0][5])
            numImagenes = 0
            for filename in carpeta:
                dicom = pydicom.dcmread(pathDicom+'\\'+filename)
                if name == str(dicom.PatientName):
                    if os.path.exists(name) == False:
                        os.mkdir(name)
                    copyfile(pathDicom+'\\'+filename,os.getcwd()+'\\'+name+'\\'+filename)
                    numImagenes += 1
        print('********************************')           
        print('INFORME:')
        print('Procedencia mensajes: '+str(i.segments('MSH')[0][3]))
        print('Nombre paciente: '+str(i.segments('PID')[0][5]))
        if str(i.segments('MSH')[0][3]) == 'IMAGE_PROC_V56':
            print('Numero de imagenes: '+str(numImagenes))
            if numImagenes > 0 :
                print('Dirección carpeta: '+os.getcwd()+'\\'+name)
except:
    print('Los mensajes hl7 contenidos en el archivo no son validos!')
                

