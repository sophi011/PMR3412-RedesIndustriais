# O cliente fará o papel de interface homem-máquina (IHM)
# client.py

from pymodbus.client.sync import ModbusTcpClient

PORT1 = 5020
PORT2 = 5021
SLAVE_ADDRESSES = [0, 0]
SERVER_ADDRESSES = [("localhost", PORT1), ("localhost", PORT2)]

print("Endereços das solicitações de leitura: ", SLAVE_ADDRESSES)

# Server 1
client = ModbusTcpClient(SERVER_ADDRESSES[0][0], SERVER_ADDRESSES[0][1])
client.connect()
disc_inputs1 = client.read_discrete_inputs(SLAVE_ADDRESSES[0])
input_regs1 = client.read_input_registers(SLAVE_ADDRESSES[0])
print("Dados das entradas discretas do server com endereço " + str(SERVER_ADDRESSES[0][1]) + ": ", disc_inputs1)
print("Dados dos registros de entradado server com endereço " + str(SERVER_ADDRESSES[0][1]) + ": ", input_regs1)
client.close()

# Server 2
client2 = ModbusTcpClient(SERVER_ADDRESSES[1][0], SERVER_ADDRESSES[1][1])
client2.connect()
disc_inputs2 = client2.read_discrete_inputs(SLAVE_ADDRESSES[1])
input_regs2 = client2.read_input_registers(SLAVE_ADDRESSES[1])
print("Dados das entradas discretas do server com endereço " + str(SERVER_ADDRESSES[1][1]) + ": ", disc_inputs2)
print("Dados dos registros de entradado server com endereço " + str(SERVER_ADDRESSES[1][1]) + ": ", input_regs2)

print("Endereços dos servidores: ", SERVER_ADDRESSES)


