Nesta entrega duas aplicações serão desenvolvidas para simular os dispositivos da nossa rede industrial usando o protocolo MODBUS sobre TCP/IP. Para cada aplicação serão implementados dois tipos de dispositivos sendo um para representar o mestre e a outro para representar os escravos. O mestre como sendo um monitor ou processador de dados e os escravos como sendo sensores e atuadores da planta industrial. Seguem as etapas comuns para o desenvolvimento dessas aplicações.

No primeiro exercício desta entrega será implementado um monitor de sensores instalados em um conjunto de tanques de armazenamento de óleo. O dispositivo mestre deverá implementar um monitor de variáveis como sendo o cliente. Os escravos serão os sensores de transbordo e de temperatura de cada tanque como sendo o servidor.

No segundo exercício desta entrega será implementado um controlador de nível de um conjunto de tanques de armazenamento de óleo. O dispositivo mestre deverá implementar um processador de dados como sendo o cliente. Os escravos serão os sensores de nível e válvula de fluxo de cada tanque como sendo o servidor.

