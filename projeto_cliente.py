from concurrent import futures
import grpc
import projeto_pb2
import projeto_pb2_grpc
import time
import logging
import threading
import ast
import RWLock
lock = RWLock.RWLock()

def menu():
  chave = 0
  channel = grpc.insecure_channel('localhost:50051')
  stub = projeto_pb2_grpc.GreeterStub(channel)

  while True:

    print("Digite insert - Para inserir a tarefa do cliente\n")
    print("Digite get    - Para listar a tarefa do cliente\n")
    print("Digite update - Para atualizar a tarefa do cliente\n")
    print("Digite delete - Para deletar a tarefa do cliente\n")
    print("Digite exit   - Para sair do programa\n")
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
      print("Digite o nome da tarefa: ")
      titulo_tarefa = input()
      print("\n")
      print("Digite o título da tarefa: ")
      descricao_tarefa = input()
      print("\n")
      
      if titulo_tarefa == '' or descricao_tarefa == '':
        print("Os campos do Título da tarefa ou Descrição da Tarefa, não foram preenchidos")
        break

      par = validaParametroClient_id(cliente_id) #Valida se o cliente_id digitado é um inteiro
      
      #hello_request = stub.recuperarCliente(projeto_pb2.HelloRequest(cid_id=par)) #Checar se o cliente existe
      
      #if(hello_request != 'SUCCESS'):
      #  print("O CID do cliente informado não existe, favor informar o CID de um cliente já cadastrado")
      #  break

      response = stub.inserirTarefa(projeto_pb2.HelloRequest(cid_id=int(cliente_id), title_task=titulo_tarefa, desc_task=descricao_tarefa))
      print("Inserindo a Tarefa, no ambiente do Cliente")
      print("O resultado da inserção: " + response.e)

      thread_read = ThreadRead()
      thread_write = ThreadWrite(thread_read)
      thread_read.start()
      thread_write.start()

    #Opção de Listar a Tarefa
    elif opcao_selecionada.lower() == 'get':
      #listarTarefas(CID)
      response = stub.listarTarefas(projeto_pb2.HelloRequest())
      print("Listando a Tarefa, no ambiente do Cliente")
      print("O resultado da listagem: " + response.e)

    #Opção de Atualizar a Tarefa
    elif opcao_selecionada.lower() == 'update':
      #modificarTarefa(CID, "titulo da tarefa", "nova descrição da tarefa")
      print("Digite os parametros da tarefa: ")
      print("Digite o CID do cliente: ")
      cliente_id = int(input())
      print("\n")
      print("Digite o nome da tarefa: ")
      titulo_tarefa = input()
      print("\n")
      print("Digite o título da tarefa: ")
      descricao_tarefa = input()
      print("\n")
  
      hello_request = stub.recuperarCliente(cliente_id) #Checar se o cliente existe

      if(hello_request == ''):
        print("O CID do cliente informado não existe, favor informar o CID de um cliente já cadastrado")
        break
      response = stub.modificarTarefa(projeto_pb2.HelloRequest())
      print("Atualizando a Tarefa, no ambiente do Cliente")
      print("O resultado da update: " + response.e)

    #Opção de Deletar a Tarefa
    elif opcao_selecionada.lower() == 'delete':
      #apagarTarefas(CID)
      response = stub.apagarTarefas(projeto_pb2.HelloRequest())
      print("Deletando a Tarefa, no ambiente do Cliente")
      print("O resultado do Delete : " + response.e)

    else:    
      print("A Opção digita é inválida, por favor digite uma opção válida!")

    #Valida se no insert, o Id do cliente é um inteiro
def validaParametroClient_id(client_id):
  while True:
    try:
      chave = int(client_id)
      break
    except:
      print("O CID do cliente deve ser um número inteiro, favor informar um CID válido")
    return chave
    


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
        time.sleep(t)
        lock.writer_acquire()
        try:
            f = open('backup.txt','w')
            f.write(str(dicionario))
            f.close()
            
        finally:
            lock.writer_release()

if __name__ == '__main__':
  logging.basicConfig()
  menu()
  