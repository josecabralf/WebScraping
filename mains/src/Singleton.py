from abc import ABC

class Singleton(ABC):
  def __new__(cls):
      if not hasattr(cls, 'instance'): cls.instance = super(Singleton, cls).__new__(cls)
      return cls.instance