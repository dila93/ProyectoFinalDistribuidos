# -*- coding: utf-8 -*-

#Version 0.1 del proyecto sistemas distribuidos
#Sebastian Ardila
#Cristian Ciro
#Esta parte del proyecto Sincronizara relojes y ofrecera servicios a multiples clientes.

import socket
import SocketServer
import threading
import time
import xmlrpclib
import InvertirMatrices
import numpy as np
from xmlrpclib import *

#Esta clase contendra el menu y los llamados a los servicios para los clientes.
class MiTcpHandler(SocketServer.BaseRequestHandler):
    clientes = []
    puertosClientes = []
    print clientes
    def handle(self):
        self.clientes.append(self.client_address[0])
        self.puertosClientes.append(self.client_address[1])
        #clientes.append(self.client_address[0])
        #print clientes
        print self.clientes
        print self.client_address[1]
        #print self.request
        #inicia el algoritmo de Berkeley
        #Berkeley(self.clientes, self.puertosClientes, self.request)
        #print horasClientes

        while True:
            try:
                datosRecibidos = self.request.recv(1024) #recibe parametros
                print datosRecibidos

                cadena = datosRecibidos.split(' ') #los convierte a una cadena de tipo [opcion, valor1, valor2, ...]
                print "cadena -> " + str(cadena)
                opcion = cadena[0] #toma el primer valor de la cadena como la opcion
                #print opcion + str(type(opcion))

                del cadena[0] #borra el primer elemento de la cadena para trabajar con los valores unicamente
                #print "nueva cadena -> "+ str(cadena)

                #print "escogiste la opcion "+opcion

                #--------------------------------------------------
                #Factorial
                if opcion == '1':
					mensaje = ''.join(cadena) #convierte la lista 'cadena' en String
					#print "mensaje "+mensaje
					resultado = factorial_remoto(int(mensaje)) #guarda el factorial en resultado / envia el mensaje casteado a entero a la funcion factorial
					self.request.send(str(resultado)) #retorna el valor resultado a el cliente (valor en factorial)

                #--------------------------------------------------
                #Potencia
                if opcion == '2':
                    #print cadena
                    resultado = potencia_remoto(int(cadena[0]), int(cadena[1])) #guarda la potencia en resultado / envia dos parametros de cadena casteados a entero a la funcion potencia
                    self.request.send(str(resultado)) #retorna el valor resultado a el cliente (valor en potencia)

                #--------------------------------------------------
                #Invertir Matriz
                if opcion == '3':
                    #lista = cadena
                    mensaje = ' '.join(cadena) #convierte la lista 'cadena' en String
                    print mensaje
                    resultado = invertirMatriz_remoto(str(mensaje), str(self.client_address)) #guarda la matriz invertida en resultado / envia el 'mensaje' casteado a String a la funcion invertirMatriz
                    self.request.send(resultado) #retorna el valor resultado a el cliente (matriz invertida)
                    docRestauracionOriginal(str(mensaje) ,str(self.client_address))


                #--------------------------------------------------
                #ver hora del servidor
                if opcion == '4':
                    resultado = copiaRestauracion(str(self.client_address[0]))

                    if resultado == NULL:
                        pass
                    else:
                        self.request.send(resultado) #retorna el valor de la matriz original
                if opcion == '5':
                    pass

            except:
               print "el cliente se desconecto o hubo un error"
               break

        return resultado


#Esta parte implementara el algoritmo de Berkeley
#Aqui pondria el codigo, ¡SI TAN SOLO TUVIERA UNO!
def Berkeley(clientes, puertos, request):
    horaClientes = getHoraClientes(clientes, puertos, request)

# Funcion que obtiene la hora de los clientes
def getHoraClientes(clientes, puertos, request):
    #sock = socket.socket()
    horasClientes = []
    count = 0
    #while count < len(clientes):
    #    message = 'True'
    #    print count
    #    #sock.connect((str(clientes[count]),int(puertos[count])))
    #    sock.sendto(message,(str(clientes[count]), int(puertos[count])))
    #    hora = sock.recv(1024)
    #    horasClientes.append(hora)
    #return horasClientes
    pass



# Funcion que calcula el factorial de un numero
def factorial_remoto(a):
	aux = a-1
	limit = a
	count = 1
	while(count < (limit-1)):
		a = a*aux
		aux = aux-1
		count = count +1
	print a
	return a

#Funcion que calcula la pontencia de un numero elevado a la potencia
def potencia_remoto(numero,potencia):
    return pow(numero,potencia)

#Funcion que invierte una matriz.
def invertirMatriz_remoto(lista, address):
    print "LISTA: \n" +str(lista)
    cadena = lista.split(' ')

    #convierte la cadena a enteros si no son enteros
    cadenaInt = []
    for i in cadena:
        cadenaInt.append(int(i))

    cadenita = cadenaInt
    #del cadenita[-1]

    print "cadenita"+ str(cadenita)
    del cadenita[-1]
    print "cadenaInt[-0]: "+str(cadenaInt[-1])

    #crea la matriz separada en vectores
    matrizCadena = []
    j = 0
    k = 0
    l = 0
    while j < int(cadenaInt[-1]):
        cadenaAux = []
        k=0
        while k < int(cadenaInt[-1]):
            cadenaAux.append(cadenita[l])
            l+=1
            k+=1
        matrizCadena.append(cadenaAux)
        j+=1

    print "matrizCadena"+ str(matrizCadena)

    #cadenaRestauracion = matrizCadena

    #restauracion = docRestauracionOriginal(cadenaRestauracion, address)
    #print restauracion

    inversa = np.linalg.inv(matrizCadena)
    print "inversa: "+ str(inversa)

    #print listaInvertida
    return str(inversa)

def docRestauracionOriginal(matrizOriginal, address):

    print "LISTA: \n" +str(matrizOriginal)
    cadena = matrizOriginal.split(' ')

    #convierte la cadena a enteros si no son enteros
    cadenaInt = []
    for i in cadena:
        cadenaInt.append(int(i))

    cadenita = cadenaInt
    #del cadenita[-1]

    print "cadenita"+ str(cadenita)
    del cadenita[-1]
    print "cadenaInt[-0]: "+str(cadenaInt[-1])

    #crea la matriz separada en vectores
    matrizCadena = []
    j = 0
    k = 0
    l = 0
    while j < int(cadenaInt[-1]):
        cadenaAux = []
        k=0
        while k < int(cadenaInt[-1]):
            cadenaAux.append(cadenita[l])
            l+=1
            k+=1
        matrizCadena.append(cadenaAux)
        j+=1

    doc=open(str(address)+'-matrizOriginal.txt','w')
    doc.write(str(matrizCadena))
    doc.close()

    copiaRestauracion(address)

def copiaRestauracion(address):

    print "ingresa copia de restauracion"
    documento= open(str(address)+'-matrizOriginal.txt','r')
    matriz = document.readlines()
    documento.close()
    print "cierra el documento"
    print "matriz: "+ str(matriz)

    return matriz

def docRestauracionInvertida(matrizInvertida, address):
    doc=open(str(address)+'-matrizInvertida.txt','w')
    doc.write(str(matrizInvertida))
    doc.close()

    doc=open(str(address)+'-matrizInvertida.txt','r')
    matriz = doc.readlines()
    doc.close()

    return matriz

#Ahora creamos lo que permitira que varios clientes se puedan conectar.
class ThreadServer(SocketServer.ThreadingMixIn, SocketServer.ForkingTCPServer):
	pass
#Ahora creamos la funcion que llamara a nuestro servidor.

def main():
    host="192.168.9.30"
    #host = "localhost"
    port= 4321
    server = ThreadServer((host,port),MiTcpHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    print "server corriendo..."

main()
