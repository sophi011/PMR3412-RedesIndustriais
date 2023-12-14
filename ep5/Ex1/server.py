# O servidor fará o papel de cada sensor da planta
# Entradas discretas - booleano
# Registros de entrada - valores numéricos como palavras de 16 bits
# server.py
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock
import threading

DI_BLOCK1 = ModbusSequentialDataBlock(0, [0])  
IR_BLOCK1 = ModbusSequentialDataBlock(0, [0])  
DI_BLOCK2 = ModbusSequentialDataBlock(0, [0])  
IR_BLOCK2 = ModbusSequentialDataBlock(0, [0])  
print("Entrada discreta do server1:", DI_BLOCK1)
print("Registros de entrada do server1:", IR_BLOCK1)
print("Entrada discreta do server2:", DI_BLOCK2)
print("Registros de entrada do server2:", IR_BLOCK2)

PORT1 = 5020
PORT2 = 5021
slave1 = ModbusSlaveContext(di=DI_BLOCK1, ir=IR_BLOCK1, zero_mode=True)
slave2 = ModbusSlaveContext(di=DI_BLOCK2, ir=IR_BLOCK2, zero_mode=True)

context1 = ModbusServerContext(slaves=slave1, single=True)
context2 = ModbusServerContext(slaves=slave2, single=True)

def start_server(context, port):
    StartTcpServer(context, address=("localhost", port))

thread1 = threading.Thread(target=start_server, args=(context1, PORT1))
thread2 = threading.Thread(target=start_server, args=(context2, PORT2))


thread2.start()
thread1.start()


#StartTcpServer(context1, address=("localhost", PORT1))
#StartTcpServer(context2, address=("localhost", PORT2))



