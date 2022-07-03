# sd_projeto_1

#Para rodar o projeto, precisa antes das dependências do grpc instaladas, para isso rode os seguintes comandos:

pip install grpcio

pip install protobuf

#Logo após essa instalação, primeiro deve-se executar o arquivo do servidor, para isso digite:

py projeto_server.py

#Logo após aparecerá um menu, com as seguintes implementaçãoes abaixo, e em seguida só seguir o menu para fazer a operação deseja.

inserirCliente(CID, "dados do cliente")
modificarCliente(CID, "novos dados do cliente")
recuperarCliente(CID)
apagarCliente(CID)

#Para executar o lado do cliente, basta digitar o comando abaixo:

py projeto_cliente.py

#Logo em seguida aparecerá um menu, com as seguintes implementaçãoes abaixo, e em seguida só seguir o menu para fazer a operação deseja.

inserirTarefa(CID, "titulo da tarefa", "descrição da tarefa")
modificarTarefa(CID, "titulo da tarefa", "nova descrição da tarefa")
listarTarefas(CID)
apagarTarefas(CID)
apagarTarefa(CID, "titulo da tarefa")

