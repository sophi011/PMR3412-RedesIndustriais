"""
Os Registros de entrada de cada escravo devem armazenar os valores referentes 
ao sensor de nível e as Entradas Discretas servirão para armazenar o estado da
botoeira ativação da válvula de fluxo.
"""

# server.py
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock
from threading import Thread, Lock
import time
#import asyncio

INITIAL_VALUES = [0, 1]
TIME_CONST = 2
CHANGE_RATE = 2
IR_BLOCK1 = ModbusSequentialDataBlock(0, INITIAL_VALUES[0])  
IR_BLOCK2 = ModbusSequentialDataBlock(0, INITIAL_VALUES[1])
DI_BLOCK1 = ModbusSequentialDataBlock(0, INITIAL_VALUES[0]*10)  
DI_BLOCK2 = ModbusSequentialDataBlock(0, INITIAL_VALUES[1]*10)

print("Valor inicializado para as entradas discretas do slave 1:", INITIAL_VALUES[0])
print("Valor inicializado para os registros de entradas do slave 1:", INITIAL_VALUES[0])
print("Valor inicializado para as entradas discretas do slave 2:", INITIAL_VALUES[1])
print("Valor inicializado para os registros de entradas do slave 2:", INITIAL_VALUES[1])

global _CONTINUAR
_CONTINUAR = True
lock = Lock()

PORT1 = 5020

slaves = {
   0x00: ModbusSlaveContext(ir=IR_BLOCK1, di=DI_BLOCK1, zero_mode=True),
   0x01: ModbusSlaveContext(ir=IR_BLOCK2, di=DI_BLOCK2, zero_mode=True),
}

context = ModbusServerContext(slaves=slaves, single=False)

def start_server(context, port):
    StartTcpServer(context, address=("localhost", PORT1))

def update_process(context):
    slave1 = context[0x00]
    slave2 = context[0x01]
    initial1 = slave1.getValues(4, 0)
    initial2 = slave2.getValues(4, 0)
    slave1.setValues(4, 0, [initial1[0]*CHANGE_RATE])
    slave2.setValues(4, 0, [initial2[0]*CHANGE_RATE])
    print("Valores de entradas discretas para slave 1: " + str(slave1.getValues(2, 0)))
    print("Valores de entradas discretas para slave 2: " + str(slave2.getValues(2, 0)))
    print("Valores de registros de entradas para slave 1: " + str(slave1.getValues(4, 0))) 
    print("Valores de registros de entradas para slave 2: " + str(slave2.getValues(4, 0)))
    time.sleep(TIME_CONST)

thread1 = Thread(target=start_server, args=(context, PORT1))

try:
  thread1.start()
  time.sleep(TIME_CONST)
  while _CONTINUAR:
    update_process(context)
    time.sleep(TIME_CONST)
   
finally:
  CONTINUAR = False
