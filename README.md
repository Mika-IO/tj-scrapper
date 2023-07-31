# tj-scrapper

Scrapper TJAL e TJCE

## Execute o projeto localmente

É necessário ter o docker instalado.

### Comandos

    make run

or

    docker build -t app-image .
    docker run --name app -p 80:80 app-image

    # to stop container

    docker stop app || true
	docker rm app || true

## Desafio

Criar uma API que busque dados de um processo em todos os graus dos Tribunais de Justiça de Alagoas (TJAL) e do Ceará (TJCE). Geralmente o processo começa no primeiro grau e pode subir para o segundo. Você deve buscar o processo em todos os graus e retornar suas informações.


## Exemplos de processos

### TJAL

    1º grau - https://www2.tjal.jus.br/cpopg/open.do
    2º grau - https://www2.tjal.jus.br/cposg5/open.do

0710802-55.2018.8.02.0001 - para mais números de processos: https://www.jusbrasil.com.br/diarios/DJAL/

#### TJCE

    1º grau - https://esaj.tjce.jus.br/cpopg/open.do
    2º grau - https://esaj.tjce.jus.br/cposg5/open.do

0070337-91.2008.8.06.0001 - para mais números de processo: https://www.jusbrasil.com.br/diarios/DJCE/

## APIs

### POST report/

input:


```json
{
    "process_id": "0710802-55.2018.8.02.0001"
}
```

output:
```json
{
    "report_id":"879358de-413a-4248-8dcf-6614cd1febc1",
    "process_number":"0710802-55.2018.8.02.0001"
}
```


### GET report/

input:
```json
    report/879358de-413a-4248-8dcf-6614cd1febc1
```
output

```json
{
    "report_id": "0710802-55.2018.8.02.0001",
    "created_at": "2023-07-28T11:22:31Z",
    "updated_at": "2023-07-28T12:34:56Z",
    "status": "processed",
    "report": {
        "level_one": {            
            "process_number": "",
            "class": "Ação Civil Pública",
            "area": "Direito Ambiental",
            "subject": "Desmatamento ilegal",
            "distribution_date": "2023-07-28",
            "judge": "Dr. João da Silva",
            "value": 100000.00,
            "parts": {
                "author": "",
                "defendant": ""
            },
            "moves": [
                {
                    "date": "2023-07-28",
                    "move": "Alguma coisa"
                }
            ]
        },
        "level_one": {            
            "process_number": "",
            "class": "",
            "area": "",
            "subject": "",
            "distribution_date": "",
            "judge": "",
            "value": null,
            "parts": {
                "author": "",
                "defendant": ""
            },
            "moves": []
        },
        ""
    }

}

```
