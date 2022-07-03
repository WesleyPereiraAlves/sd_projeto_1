from concurrent import futures
import grpc
import projeto_pb2
import projeto_pb2_grpc
import time

import threading
import ast
import logging
import RWLock
lock = RWLock.RWLock()
dicionario = {}

#-----------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------IO MODULE----------------------------------------------------------

class ThreadRead (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)

   def run(self):
      print ("Starting ThreadRead")
      read_db()
      print ("Exiting ThreadRead")

class ThreadWrite(threading.Thread):
    def __init__(self,counter):
        threading.Thread.__init__(self)
        self.counter = counter
    def run(self):
        print('Starting ThreadWrite')
        write_db(self.counter)
        print('Exiting ThreadWrite')

def read_db():
    lock.writer_acquire
    try:
        f = open('backup.txt','r')
        global dicionario
        dicionario = ast.literal_eval(f.read())
        
    finally:
        lock.writer_release

def write_db(t):
    while True:
        lock.writer_acquire()
        try:
            f = open('backup.txt','w')
            f.write(str(dicionario))
            f.close()
            
        finally:
            lock.writer_release()


class Greeter(projeto_pb2_grpc.GreeterServicer):

    #Servidor
    def inserirCliente(client_id, dados_cliente):

        print("#############State server: ##############")
        lock.writer_acquire()

        try: 
            if client_id.cid_id in dicionario:
                return projeto_pb2.HelloReply(dados_client='ERROR',
                cid_id = dicionario[client_id.cid_id])
            else:
                dicionario[client_id.cid_id] = dados_cliente.dados_client
                print(dicionario)

                return projeto_pb2.HelloReply(dados_client='SUCCESS')
        finally:
            lock.writer_release()

    def recuperarCliente(client_id):

        thread_read = ThreadRead()
        #thread_read.setDaemon(True)
        print("-----", dicionario)
        thread_read.start()

        print("Buscando dados do Cliente, Aguarde")
        try:
            if client_id.cid_id in dicionario:
                valor = dicionario.get(client_id.cid_id)
                if(valor == ''):
                    print('Não existe o CID: ', {client_id.cid_id})
                    return projeto_pb2.HelloReply(dados_client='ERROR')
                else:
                    print('O valor do CID é: ', {client_id.cid_id}, 'Dados do Cliente:', {valor})

        finally:
            lock.reader_release()

    def modificarCliente(self, request, context):
        print("Atualizando a Tarefa, no ambiente do Cliente")
        return projeto_pb2.HelloReply(e="Cliente atualizado com sucesso")
        


    def apagarCliente(self, request, context):
        print("Deletando a Tarefa, no ambiente do Cliente")
        return projeto_pb2.HelloReply(e="Cliente deletado com sucesso")


    #Tarefas Cliente
    def inserirTarefa(self, request, context):
                        
        print("#############State server: ##############")
        lock.writer_acquire()

        try: 
            if request.cid_id in dicionario:
                return projeto_pb2.HelloReply(e='ERROR',
                cid_id = dicionario[request.cid_id][0], title_task= dicionario[request.cid_id][1],
                desc_task=dicionario[request.cid_id][2])
            else:
                dicionario[request.cid_id] = (request.cid_id,request.title_task,request.desc_task)
                print(dicionario)

                return projeto_pb2.HelloReply(e='SUCCESS')
        finally:
            lock.writer_release()

    def atualizarTarefa(self, request, context):
        print("Atualizando a Tarefa, no ambiente do Cliente")
        return projeto_pb2.HelloReply(e="Tarefa atualizada com sucesso")
    def listarTarefa(self, request, context):
        print("Listando a Tarefa, no ambiente do Cliente")
        return projeto_pb2.HelloReply(e="Tarefa listada com sucesso")
    def deletarTarefa(self, request, context):
        print("Deletando a Tarefa, no ambiente do Cliente")
        return projeto_pb2.HelloReply(e="Tarefa deletada com sucesso")

#opções de inserção

def menu():
    while True:

        print("Digite insert - Para inserir a tarefa do cliente\n")
        print("Digite get    - Para listar a tarefa do cliente\n")
        #print("Digite update - Para atualizar a tarefa do cliente\n")
        #print("Digite delete - Para deletar a tarefa do cliente\n")
        #print("Digite exit   - Para sair do programa\n")
        opcao_selecionada = input("Digite a opção desejada: ")

        if opcao_selecionada.lower() == 'exit':
            break

        #Opção de Inserir a Tarefa
        elif opcao_selecionada.lower() == 'insert':
            #inserirTarefa(CID, "titulo da tarefa", "descrição da tarefa")
            
            
            print("Digite os parametros da tarefa: ")
            print("Digite o CID do cliente: ")
            cliente_id = input()
            print("\n")
            print("Digite a descrição do cliente: ")
            dados_client = input()
            response = Greeter.inserirCliente(projeto_pb2.HelloReply(cid_id = int(cliente_id)), projeto_pb2.HelloReply(dados_client = dados_client))

            thread_write = ThreadWrite(dicionario)
            #thread_read.start()
            thread_write.start()
        
        #Opção de Listar a Tarefa
        elif opcao_selecionada.lower() == 'get':
            #listarTarefas(CID)

            print("Digite o CID do cliente que deseja listar: ")
            cliente_id = input()

            response = Greeter.recuperarCliente(projeto_pb2.HelloReply(cid_id = int(cliente_id)))
            if(response == 'ERROR'):
                print('Não existe o CID: ' + response.client_id)
                break
            
            print("Listando a Tarefa, no ambiente do Cliente")
            #print("O resultado da listagem: " + response.cid_id + " - " + response.dados_client)
        

if __name__ == '__main__':
    menu()
    logging.basicConfig()

    #server()
    #option()