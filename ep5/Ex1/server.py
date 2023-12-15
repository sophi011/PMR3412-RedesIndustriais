"""
O servidor fará o papel de cada sensor da planta
Entradas discretas - booleano
Bobinas - booleano
Registros de entrada - valores numéricos como palavras de 16 bits
from threading import Thread
t = Thread(target=atualizar_processo, args=(contexto,))
t.start()
global _CONTINUAR
try:
  rodar_servidor()
finally:
  CONTINUAR = False
  t.join()
while _CONTINUAR:
  atualizar_contexto()
ModbusSlaveContext.getValues(registrador, endereco) 
ModbusSlaveContext.setValues(registrador, endereco, valores) 
registrador -> (fx=1,co), (fx=2,di), (fx=3,hr) e (fx=4,ir)
"""

# server.py
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock
from threading import Thread
import time

INITIAL_VALUES = [0, 1]
TIME_CONST = 1
TIME_RATE = 5
IR_BLOCK1 = ModbusSequentialDataBlock(0, INITIAL_VALUES[0])  
IR_BLOCK2 = ModbusSequentialDataBlock(0, INITIAL_VALUES[1])
print("Valores inicializados:", INITIAL_VALUES)

global _CONTINUAR
_CONTINUAR = True

PORT1 = 5020

slaves = {
   0x00: ModbusSlaveContext(ir=IR_BLOCK1),
   0x01: ModbusSlaveContext(ir=IR_BLOCK2),
}

context = ModbusServerContext(slaves=slaves, single=False)

def update_process(context):
    slave1 = context[0x00]
    slave2 = context[0x01]
    slave1.setValues(4, 0, [0])
    slave2.setValues(4, 0, [1])

def start_server(context, port):
    StartTcpServer(context, address=("localhost", PORT1))

thread1 = Thread(target=start_server, args=(context, PORT1))
thread2 = Thread(target=update_process, args=(context,))

try:
  thread1.start()
  time.sleep(TIME_CONST)
  thread2.start()
  update_process(context)
  while _CONTINUAR:
    update_process(context)
    time.sleep(TIME_RATE)
    print("Valores para slave 1: " + str(slaves[0].getValues(4, 0)))
    print("Valores para slave 2: " + str(slaves[1].getValues(4, 0)))
finally:
  CONTINUAR = False
  thread2.join()

  

  





