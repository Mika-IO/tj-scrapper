# TJ-Scrapper

Scrapper TJAL e TJCE

## Execute o projeto localmente

É necessário ter o Docker e o Python3 instalado.

### Dependências

    Python3
    Docker

### Executar testes unitários

    make run-tests

### Comandos para executar o projeto

    make install
    make run

### API Docs

    http://localhost/docs

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
    "process_number": "0710802-55.2018.8.02.0001"
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
    "report": {
        "process_number": "0710802-55.2018.8.02.0001",
        "status": "complete",
        "created_at": "2023-08-02T01:41:57.257020",
        "updated_at": "2023-08-02T01:41:57.260956",
        "first_level": {
            "process_number": "0710802-55.2018.8.02.0001",
            "process_class": "Procedimento Comum Cível",
            "process_area": "Cível",
            "process_subject": "Dano Material",
            "process_date": "02/05/2018",
            "process_judge": "José Cícero Alves da Silva",
            "process_value": "R$ 281.178,42",
            "process_parts": [
                {
                    "part": "Autor",
                    "name": "José Carlos Cerqueira Souza FilhoAdvogado:Vinicius Faria de Cerqueira",
                    "lawyers": [
                        "Vinicius Faria de Cerqueira"
                    ]
                },
                {
                    "part": "Ré",
                    "name": "Cony Engenharia Ltda.Advogado:Carlos Henrique de Mendonça BrandãoAdvogado:Guilherme Freire FurtadoAdvogada:Maria Eugênia Barreiros de MelloAdvogado:Vítor Reis de Araujo Carvalho",
                    "lawyers": [
                        "Carlos Henrique de Mendonça Brandão",
                        "Guilherme Freire Furtado",
                        "Maria Eugênia Barreiros de Mello",
                        "Vítor Reis de Araujo Carvalho"
                    ]
                }
            ],
            "process_moves": [
                {
                    "date": "21/07/2023",
                    "description": "Ato Publicado Relação: 0450/2023 Data da Publicação: 24/07/2023 Número do Diário: 3349"
                },
                {
                    "date": "20/07/2023",
                    "description": "Ato ordinatório praticado Autos n°: 0710802-55.2018.8.02.0001 Ação: Procedimento Comum Cível Autor: José Carlos Cerqueira Souza Filho e outro Réu: Cony Engenharia Ltda. e outro ATO ORDINATÓRIO Em cumprimento ao disposto no Provimento nº 15/2019, da Corregedoria Geral da Justiça do Estado de Alagoas, fica(m) a(s) parte(s) ré intimada(s), na pessoa do seu advogado, para, no prazo de 15 (quinze) dias, providenciar(em) o recolhimento das custas processuais, sob pena de expedição de certidão ao FUNJURIS (Resolução TJ/AL nº 19/2007) para inscrição na divida ativa estadual, após o que será arquivado o processo. Ocorrendo o pagamento, devidamente atualizado, após a emissão da supracitada certidão de débito, deverá o interessado entregar a ficha de compensação bancária quitada na sede do FUNJURIS, que se responsabilizará pela devida baixa, além de oficiar à secretaria de onde se originou o débito acerca do referido pagamento (Resolução nº 19/2007, art. 33, § 6º). Maceió, 20 de julho de 2023 Marcelo Rodrigo Falcão Vieira Analista(escrivão substituto)Vencimento: 10/08/2023"
                }
            ]
        }
    }
}
```

## TODO

- [X] Planning Solution
- [X] Scrapper Pages
- [X] Database
- [+-] Unittests
- [-] Refactoring
- [+-] Observability