
# client.py

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.pdu import ModbusExceptions
import asyncio
from threading import Lock

PORT1 = 5020
SLAVE_ADDRESSES = [0, 0]  # endereço para leitura
SERVER_ADDRESS = ("localhost", PORT1)
TIME_CONST = 5

global _CONTINUAR
_CONTINUAR = True
lock = Lock()
client = ModbusTcpClient(SERVER_ADDRESS[0], SERVER_ADDRESS[1])
client.connect()

print("Endereços para solicitação de leitura: ", SLAVE_ADDRESSES)

async def update_processing():
    # Solicitação de leitura
    input_regs1 = client.read_input_registers(SLAVE_ADDRESSES[0], unit=0x00)
    print("Registros de entrada lidos do slave 1: " + str(input_regs1.registers))
    discrete_inputs1 = client.read_discrete_inputs(SLAVE_ADDRESSES[0], unit=0x00)
    print("Entradas discretas lidas do slave 1: " + str(discrete_inputs1.bits))

    input_regs2 = client.read_input_registers(SLAVE_ADDRESSES[1], unit=0x01)
    print("Registros de entrada lidos do slave 2: " + str(input_regs2.registers))
    discrete_inputs2 = client.read_discrete_inputs(SLAVE_ADDRESSES[1], unit=0x01)
    print("Entradas discretas lidas do slave 2: " + str(discrete_inputs2.bits))

async def timer():
    await asyncio.sleep(TIME_CONST)

async def run_processing():
  while _CONTINUAR:
    await asyncio.gather(
      update_processing(),
      timer()
    )

asyncio.run(run_processing())