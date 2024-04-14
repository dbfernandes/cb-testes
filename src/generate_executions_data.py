import os
from datetime import datetime
import csv
import sys
import time

class Execution:
  def __init__(self, classNumber, student, type, datetime):
    self.classNumber = classNumber
    self.student = student
    self.type = type
    self.execDatetime = datetime

ExecutionArray = [] #empty array    

if len(sys.argv) != 2:
    print("python3 aval_codeplay.py <ano>")
    quit()

ano = sys.argv[1]

for semestre in ["01", "02"]:

  dataset_path = f"../dataset/{ano}_{semestre}"

  print("Dataset path:",dataset_path)

  if not os.path.exists(dataset_path):
    raise Exception("Folder does not exist")

  for turma in os.listdir(dataset_path):
    # print("Turma:",turma)

    for aluno in os.listdir(f"{dataset_path}/{turma}/users"):
      print("Aluno:",aluno)

      for subdir, dirs, files in os.walk(f"{dataset_path}/{turma}/users/{aluno}/executions"):
        for filename in files:             
          ##### ARQUIVO: arquivos com logs de execução de códigos #####
          if subdir.endswith(f"{turma}/users/{aluno}/executions") and filename.endswith(".log"):
            # print("Arquivo:",filename)
            execution_file = open(subdir + "/" + filename, 'r')
            execution_data = execution_file.readlines()

            for execution in execution_data:
              if "== TEST" in execution or "== SUBMITION" in execution:
                execution = execution.replace("== ", "")
                type = execution.split(" (")[0]
                execDatetime = execution.split(" (")[1]
                execDatetime = execDatetime.replace(") \n", "")
                #datetime = time.strptime(datetime, "%Y-%m-%d %H:%M:%S")
                ExecutionArray.append(Execution(turma, aluno, type, execDatetime))

SortedExecutionArray = sorted(
  ExecutionArray,
  key=lambda x: datetime.strptime(x.execDatetime, "%Y-%m-%d %H:%M:%S"), reverse=False
)

for exec in range(len(SortedExecutionArray)):              
  print(SortedExecutionArray[exec].classNumber, SortedExecutionArray[exec].student, SortedExecutionArray[exec].type, SortedExecutionArray[exec].execDatetime, sep="\t")

