# O servidor fará o papel de cada sensor da planta
# Entradas discretas - booleano
# Bobinas - booleano
# Registros de entrada - valores numéricos como palavras de 16 bits

# server.py
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock

INITIAL_VALUES = [0, 0]
CO_BLOCK = ModbusSequentialDataBlock(0, INITIAL_VALUES)  
print("Valores inicializados para bobina:", INITIAL_VALUES)

PORT1 = 5020
slave = ModbusSlaveContext(co=CO_BLOCK, zero_mode=True)

context = ModbusServerContext(slaves=slave, single=True)

StartTcpServer(context, address=("localhost", PORT1))



