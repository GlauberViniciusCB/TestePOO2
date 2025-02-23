```python
class Factory:
    @staticmethod
    def criar_veterinario(nome, crmv):
        return Veterinario(nome, crmv)

    @staticmethod
    def criar_cliente(nome, telefone):
        return Cliente(nome, telefone)

    @staticmethod
    def criar_paciente(nome, especie, raca, idade, dono):
        return Paciente(nome, especie, raca, idade, dono)

    @staticmethod
    def criar_consulta(data, horario, veterinario, paciente):
        return Consulta(data, horario, veterinario, paciente)
```

## vet.py
```python
class Veterinario:
    def __init__(self, nome, crmv):
        self.nome = nome
        self.crmv = crmv
        self.clientes = []

    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)
```

## cli.py
```python
class Cliente:
    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone
        self.pacientes = []

    def adicionar_paciente(self, paciente):
        self.pacientes.append(paciente)
```

## pac.py
```python
class Paciente:
    def __init__(self, nome, especie, raca, idade, dono):
        self.nome = nome
        self.especie = especie
        self.raca = raca
        self.idade = idade
        self.dono = dono
```

## cons.py
```python
class Consulta:
    def __init__(self, data, horario, veterinario, paciente):
        self.data = data
        self.horario = horario
        self.veterinario = veterinario
        self.paciente = paciente
```

## main.py
```python
from factory import Factory

# cria todas as entidades
veterinario = Factory.criar_veterinario("Dr. Glauber", "CRMV1234")


cliente = Factory.criar_cliente("Annah Louise", "(31) 99999-9999")
veterinario.adicionar_cliente(cliente)


paciente = Factory.criar_paciente("Percy", "Cachorro", "American Bully", 3, cliente)
cliente.adicionar_paciente(paciente)


consulta = Factory.criar_consulta("01/01/2025", "14:00", veterinario, paciente)

# print info
print(f"Veterinário: {veterinario.nome}, CRMV: {veterinario.crmv}")
print(f"Cliente: {cliente.nome}, Telefone: {cliente.telefone}")
print(f"Paciente: {paciente.nome}, Espécie: {paciente.especie}, Raça: {paciente.raca}, Idade: {paciente.idade}")
print(f"Consulta marcada para {consulta.data} às {consulta.horario} com {consulta.veterinario.nome} para o paciente {consulta.paciente.nome}")
```
