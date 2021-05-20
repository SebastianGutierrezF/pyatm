#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Funciones de interacción con el usuario.
def bienvenida(loged,users):
    input('Presiona enter para continuar ->')
    guardar(users)
    clear()
    if loged[0] == '':
        print('Operaciones disponibles:\nAcceder\nAbrir cuenta\nSalir')
        selec = input('Escribe la operación que desees realizar: ')
        try:
            fDict[selec.lower()]
        except KeyError:
            print('Esa operación no existe. Por favor intenta de nuevo.')
            bienvenida(loged,users)
        else:
            fDict[selec.lower()](loged,users)
            
    elif not (loged[0] == ''):
        lName = users[loged[0]]['nombre'].split()
        print(f'¡Hola, {lName[0]}!')
        print('Operaciones disponibles:\nSaldo\nRetirar\nServicios\nDepositar\nTransferir\nEliminar cuenta\nSalir')
        selec = input('Escribe la operación que desees realizar: ')
        try:
            fDict[selec.lower()]
        except KeyError:
            print('Esa operación no existe. Por favor intenta de nuevo.')
            bienvenida(loged,users)
        else:
            fDict[selec.lower()](loged,users)
        fDict[selec.lower()](loged,users)


# In[ ]:


#Función de inicio de sesión
def acceder(loged,users):
    mat = input('Matrícula: ')
    nip = input('NIP: ')
    try:
        users[mat.upper()]
    except (KeyError, TypeError):
        print(f'La matrícula {mat} no está registrada en 4Bank. Crea una cuenta o intenta con otro número.')
    else:
        if nip != users[mat.upper()]['nip']:
            print('NIP incorrecto. Intenta de nuevo por favor.')
        else:
            loged[0] = mat.upper()
    bienvenida(loged,users)


# In[ ]:


def verEdo(loged, users):
    print(f'Nombre: {users[loged[0]]["nombre"]}')
    print(f'Matrícula institucional: {loged[0]}')
    print(f'Dinero: ${users[loged[0]]["cash"]} pesos mexicanos.')
    print(f'Número de cuenta clabe: {users[loged[0]]["clabe"]}')
    bienvenida(loged,users)


# In[ ]:


def salir(loged,users):
    loged = ['']
    guardar(users)
    sys.exit()


# In[ ]:


def abrirCuenta(loged,users):
    mat = input('Matrícula institucional: ').upper()
    nom = input('Nombre completo: ')
    n = input('NIP deseado: ')
    try:
        din = float(input('Saldo inicial: '))
        if din <= 0:
            print('El monto ingresado debe ser mayor a cero. Intenta de nuevo por favor.')
            return bienvenida(loged,users)
    except ValueError:
        print('Ingresa únicamente números para el saldo inicial. Vuelve a intentarlo por favor.')
    else:
        for matricula in users.keys():
            if mat == matricula:
                print('Esta matricula ya está registrada. Elije la opción de acceder para iniciar sesión.')
                return bienvenida(loged,users)
        users[mat] = {'nombre':nom,'cash':din,'nip':n}
        sid = '4'+str((id(users[mat])))
        users[mat]['clabe'] = sid
        print(f'¡Felicidades! Tu cuenta ha sido creada.\nTu número de cuenta clabe es: {users[mat]["clabe"]}')
    bienvenida(loged,users)


# In[ ]:


def eliminarCuenta(loged,users):
    selec = input("Teclea enter para eliminar tu cuenta o escribe no para cancelar. ")
    if selec.lower() == 'no':
        return bienvenida(loged,users)
    i = 1
    nip = input('NIP: ')
    while nip != users[loged[0]]['nip']:
        if i == 3:
            print('Demasiados intentos. Vuelve a intentarlo por favor.')
            return bienvenida(loged,users)
        nip = input('NIP incorrecto. Tienes {0} oportunidades más -> '.format((3-i)))
        i+=1
        
    #Genera un número de token aleatorio para completar la operación.
    tkn = token()
    i = 1
    print('Tu número de token es: {0}'.format(tkn))
    utkn = input('Ingresa el número de token para terminar la operación: ')
    while utkn != tkn:
        if i == 3:
            print('Demasiados intentos. Vuelve a intentarlo por favor.')
            return bienvenida(loged,users)
        utkn = input('Token erroneo. Tienes {0} oportunidades más -> '.format((3-i)))
        i+=1
    users.pop(loged[0])
    loged = ['']
    print("Ejecucion exitosa, gracias por su confiaza en 4Bank, vuelva pronto")
    bienvenida(loged,users)


# In[ ]:


def retirar(loged,users):
    print("Saldo actual:",users[loged[0]]['cash'])
    try:
        ret=float(input("Dijite la cantidad de dinero a retirar: "))
        if ret <= 0:
            print('El monto ingresado debe ser mayor a cero. Intenta de nuevo por favor.')
            return bienvenida(loged,users)
        if users[loged[0]]['cash']-ret < 0:
            print('No cuentas con el saldo suficiente para realizar el retiro.')
        else:
            users[loged[0]]['cash']-=ret
            print("Retiro realizado con exito")
            print("Saldo actual:",users[loged[0]]['cash'])
    except ValueError:
        print('¡Ups! Parece que ocurrio un error. Intenta de nuevo por favor.')
    bienvenida(loged,users)


# In[ ]:


def pServicios(loged,users):
    serv = ['GASAN','MIGUELAGUA','TELALLENDE']
    selec = input('Servicios disponibles:\n{0}\n{1}\n{2}\nIngresa el nombre del servicio que desees pagar: '.format(serv[0],serv[1],serv[2]))
    
    try:
        serv.index(selec.upper())
    except ValueError:
        print('¡Ups! Esperamos tener ese servicio disponible muy pronto. Intenta de nuevo por favor.')
    else:
        pay = randint(200,600)
        selec = input('El monto adeudado es: {0}\nEscribe pagar para terminar: '.format(pay))

        while selec != 'pagar':
            selec = input('Intentalo de nuevo por favor.\nEscribe pagar para terminar: ')

        if users[loged[0]]['cash']-pay < 0:
            print('No cuentas con el saldo suficiente para realizar este pago.')
        else:
            users[loged[0]]['cash']-=pay
            print('El pago de servicio ha sido registrado con éxito.\nTu saldo es de: {0}'.format(users[loged[0]]['cash']))
    bienvenida(loged,users)


# In[ ]:


def depositar(loged,users):
    print("Saldo actual:",users[loged[0]]['cash'])
    try:
        dpo=float(input("Dijite la cantidad de dinero a depositar: "))
        if dpo <= 0:
            print('El monto ingresado debe ser mayor a cero. Intenta de nuevo por favor.')
            return bienvenida(loged,users)
        users[loged[0]]['cash']+=dpo
        print("Pago realizado con exito")
        print("Saldo actual:",users[loged[0]]['cash'])
    except ValueError:
        print('¡Ups! Asegurte de ingresar únicamente números para indicar el monto de la operación. Intenta de nuevo por favor.')
    bienvenida(loged,users)


# In[ ]:


def transfer(loged,users):
    print('Ingrese los datos requeridos para realizar la transferencia.')
    dest = input('Clabe de la cuenta de destino: ')
    try:
        qty = float(input('Cantidad: '))
        if qty <= 0:
            print('El monto ingresado debe ser mayor a cero. Intenta de nuevo por favor.')
            return bienvenida(loged,users)
    except ValueError:
        print('Sucedio un error. Asegurte de ingresar únicamente números para indicar el monto de la operación.')
    else:
        #Comprueba si el usuario origen cuenta con saldo suficiente y captura el error en caso que se genera.
        if qty > users[loged[0]]['cash']:
            print('No cuentas con el saldo suficiente para realizar esta tranferencia. Intentalo de nuevo por favor.')
        else:
            #Genera un número de token aleatorio. Si el usuario falla tres veces entonces tiene que repetir el proceso.
            tkn = token()
            i = 1
            print('Tu número de token es: {0}'.format(tkn))
            utkn = input('Ingresa el número para terminar la operación: ')
            while utkn != tkn:
                if i == 3:
                    print('Demasiados intentos. Vuelve a intentarlo con otro número de token.')
                    return bienvenida(loged,users)
                utkn = input('Token erroneo. Tienes {0} oportunidades más -> '.format((3-i)))
                i+=1
                
            #Operaciones en caso de transferencia exitosa.    
            #Verifica que el usuario de destino si exista en la base de clientes.  
            done = False
            for matricula in users.values():
                if dest == matricula['clabe']:
                    users[loged[0]]['cash']-=qty
                    matricula['cash']+=qty
                    done = True
                    break
            if done:
                print('La transferencia ha sido completada con éxito.\n Tu saldo actual es: {0}'.format(users[loged[0]]['cash']))
                done = False
            else:
                print('No existe ninguna cuenta vinculada a la clabe ingresada. Intenta de nuevo por favor.')
    bienvenida(loged,users)


# In[ ]:


#Funciones que no serán llamadas drectamente por las selecciones del usuario.

def guardar(users):
    with open('usuarios.txt','w') as fileID:
        fileID.write(str(users))

def cargar(users):
    try:
        with open('usuarios.txt','r') as fileID:
            fs = fileID.read()
            return eval(fs)
    except FileNotFoundError:
        newF = open('usuarios.txt','x')
        newF.write('{}')
        newF.close()
        newF = open('usuarios.txt','r')
        fs = newF.read()
        newF.close()    
        return eval(fs)
        
def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def token():
    return str(randint(111111,999999))


# In[ ]:


from random import randint
import os
import sys

#Celda de declaración de variables globales
#Diccionario de todos los clientes de 4 Bank
users = {}
users = cargar(users)

#Lista donde se almacenan los datos del usuario que esta logeado -> loged = [nombre, True]
#Basta con el nombre de usuario para obtener sus datos del diccionario users.
#Se escogió una lista porque es de tipo mutable y nos permite editar directamente la variable desde los metodos. 
loged = ['']

#Diccionario de todas las funciones internas para ser llamadas directamente con el input del usuario y evitar exceso de condiciones.
fDict = {'abrir cuenta':abrirCuenta,'acceder': acceder,
         'saldo': verEdo,'retirar': retirar,
         'servicios': pServicios,'depositar': depositar,
         'transferir': transfer,'salir':salir,
         'eliminar cuenta':eliminarCuenta}

print("Bienvenido a 4Bank.")
bienvenida(loged,users)

