"""
O cliente fará o papel de interface homem-máquina (IHM)]
cliente.write_register(endereco,valoralvo)
escrita nos endereços da tabela das Bobinas com o método write_coil()
limite de 248 bytes por solicitação
requisicao = cliente.write_coils(endereco,[0]*quantidade)
codigo = requisicao.exception_code
ModbusExceptions.decode(codigo)
somente as tabelas Bobinas e Registros de Retenção são permitidas as funções de escrita
read_discrete_inputs(0, unit=0x00)
"""

# client.py

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.pdu import ModbusExceptions

PORT1 = 5020
SLAVE_ADDRESSES = [0, 0]  # endereço para leitura
SERVER_ADDRESS = ("localhost", PORT1)

client = ModbusTcpClient(SERVER_ADDRESS[0], SERVER_ADDRESS[1])
client.connect()

# Solicitação de leitura
print("Enderços para solicitação de leitura: ", SLAVE_ADDRESSES)
read_value1 = client.read_input_registers(SLAVE_ADDRESSES[0], unit=0x00)
print("Valor lido para slave 1: " + str(read_value1.registers))
read_value2 = client.read_input_registers(SLAVE_ADDRESSES[1], unit=0x01)
print("Valor lido para slave 2: " + str(read_value2.registers))

