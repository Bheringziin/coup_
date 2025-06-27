class Carta:
  def __init__(self, nome:str, descricao:str):
    self.nome = nome
    self.virada = False
    self.descricao = descricao

#Vamos usar getters(com o @property), aplicando assim o principio do encapsulamento
#O _ antes dos atributos dentro dos getters serve pra indicar que são protegidos

  @property
  def nome(self):
    return self._nome

  @property
  def virada(self):
    return self._virada
  
  @property
  def descricao(self):
    return self._descricao

  def virar(self):
    self.virada = not self.virada

  #Metodo usado para depois usar print(carta) e termos uma representação formatada. Também é bom para debugar o código
  def __repr__(self):
    return f"Carta(nome={self._nome}, virada={self._virada})"





  
