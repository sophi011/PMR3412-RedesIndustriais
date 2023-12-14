"""
O cliente fará o papel de interface homem-máquina (IHM)]
cliente.write_register(endereco,valoralvo)
escrita nos endereços da tabela das Bobinas com o método write_coil()
limite de 248 bytes por solicitação
requisicao = cliente.write_coils(endereco,[0]*quantidade)
codigo = requisicao.exception_code
ModbusExceptions.decode(codigo)
somente as tabelas Bobinas e Registros de Retenção são permitidas as funções de escrita
"""

# client.py

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.pdu import ModbusExceptions

PORT1 = 5020
SLAVE_ADDRESS = 0  # endereço
NUM_VAR = 2   # quantidade de variáveis
VALUE = [1, 1]  # valor a ser solicitado para escrita
SERVER_ADDRESS = ("localhost", PORT1)

client = ModbusTcpClient(SERVER_ADDRESS[0], SERVER_ADDRESS[1])
client.connect()

# Escritas inválidas
invalid_address = 5
invalid_value = ""
request1 = client.write_coils(invalid_address,[0]*NUM_VAR)
code1 = request1.exception_code
print("Parâmetro inválido para escrita solicitado (endereço): ", invalid_address)
print("Código de exceção: ", code1)
print("Código de exceção decodificado: ", ModbusExceptions.decode(code1))

request2 = client.write_coils(SLAVE_ADDRESS, invalid_value)
code2 = request2.exception_code
print("Parâmetro inválido para escrita solicitado (valor): ", invalid_value)
print("Código de exceção: ", code2)
print("Código de exceção decodificado: ", ModbusExceptions.decode(code2))

# Solicitação válida de escrita
valid_request = client.write_coils(SLAVE_ADDRESS,[VALUE]*NUM_VAR)
print("Parâmetro válido para escrita: ", VALUE)
print("Endereço válido das solicitações de leitura e escrita: ", SLAVE_ADDRESS)
print("Parâmetro de quantidade na solicitação válida de escrita: ", NUM_VAR)

# Solicitação de leitura
read_value = client.read_coils(SLAVE_ADDRESS, NUM_VAR)
print("Valor lido: " + str(read_value.bits))
