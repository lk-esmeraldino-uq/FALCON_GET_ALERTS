# requisitos

- python 3.11 ou 3.12

# antes de começar

- Verifique o .env
- O .env deverá estar com o client id e secret da api do falcon
- Para mudar o tempo de coleta, mude a variavel TIME_RANGE_IN_DAYS dentro de .env
- o .env_sample é apenas um exemplo para outros ambientes

# passo 1 - criar virtual enviroment python

```
    python -m venv .venv
```

# passo 2 - referenciar virual enviroment

```
    source .venv/Scripts/activate
```

ou

```
    source .venv/Scripts/activate.bat
```

# passo 3 - instalar requisitos

```
    pip install -r requirements.txt
```

# passo 4 - executar script

```
    python main.py
```

## os exports deverão estar na pasta Export