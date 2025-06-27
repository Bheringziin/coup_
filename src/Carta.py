class Carta:
  def __init__(self, nome: str, descricao: str):
    # Os atributos internos devem usar o prefixo `_` para
    # corresponder aos getters definidos abaixo.
    self._nome = nome
    self._virada = False
    self._descricao = descricao

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
    """Inverte o estado de `virada` da carta."""
    # Usamos o atributo protegido para evitar chamar o getter
    # recursivamente.
    self._virada = not self._virada

  #Metodo usado para depois usar print(carta) e termos uma representação formatada. Também é bom para debugar o código
  def __repr__(self):
    return f"Carta(nome={self._nome}, virada={self._virada})"
