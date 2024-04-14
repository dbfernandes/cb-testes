import os
from datetime import datetime
import csv
import sys
import time

class Keystroke:
  def __init__(self, classNumber, student, keyDatetime):
    self.classNumber = classNumber
    self.student = student
    self.keyDatetime = keyDatetime

KeystrokesArray = [] #empty array    

if len(sys.argv) != 2:
    print("python3 aval_codeplay.py <ano>")
    quit()

ano = sys.argv[1]

for semestre in ["01"]:

  dataset_path = f"../dataset/{ano}_{semestre}"

  # print("Dataset path:",dataset_path)

  if not os.path.exists(dataset_path):
    raise Exception("Folder does not exist")

  for turma in ["438"]:
    # print("Turma:",turma)

    for aluno in os.listdir(f"{dataset_path}/{turma}/users"):
      # print("Aluno:",aluno)

      for subdir, dirs, files in os.walk(f"{dataset_path}/{turma}/users/{aluno}/codemirror"):
        for filename in files:             
          ##### ARQUIVO: arquivos com logs de execução de códigos #####
          if subdir.endswith(f"{turma}/users/{aluno}/codemirror") and filename.endswith(".log"):
            keystoke_file = open(subdir + "/" + filename, 'r')
            keystoke_data = keystoke_file.readlines()

            for keystoke in keystoke_data:
              if keystoke.startswith("202") and "#" in keystoke:
                keyDatetime = keystoke.split("#")[0]
                try:
                  keyDatetimeConverted = datetime.strptime(keyDatetime, "%Y-%m-%d %H:%M:%S.%f")
                  if (keyDatetimeConverted):
                    KeystrokesArray.append(Keystroke(turma, aluno, keyDatetime))
                except Exception:
                  pass


SortedKeystrokesArray = sorted(
  KeystrokesArray,
  key=lambda x: datetime.strptime(x.keyDatetime, "%Y-%m-%d %H:%M:%S.%f"), reverse=False
)


for exec in range(len(SortedKeystrokesArray)):              
  print(SortedKeystrokesArray[exec].classNumber, SortedKeystrokesArray[exec].student, SortedKeystrokesArray[exec].keyDatetime, sep="\t")

