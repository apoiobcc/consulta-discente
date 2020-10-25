# Extrator de resultados da consulta discente

Este diretório contem todos os arquivos e scripts utilizados para a extração e analise do resultado da consulta discente. Em particular, temos como entrada o arquivo `.csv` gerado pelo google forms, que fica em `resultado.csv`.

Para gerar os gráficos e extrair os comentários de cada sessão execute
```bash
python3 processa.py
```

Para gerar os PDF's com os gráficos e comentários execute
```bash
bash gera_pdf.sh
```

Os relatórios finais ficam na pasta `relatorios/`.

## Como funciona

Quando executamos o programa `processa.py` o arquivo `resultado.csv` é aberto como um _DataFrame_. O utilitário cria então, uma pasta para cada disciplina dentro do diretório `disciplinas/`, essa pasta sera utilizada para armazenar os gráficos e comentários extraídos das respostas daquela disciplina.
- Os gráficos são gravados como arquivos `.png`
- Os comentários de cada sessão são salvos em diferentes arquivos `.md`

Em seguida, o _script_ `gera_pdf` itera sobre todas as pastas criadas para disciplinas, trazendo também os moldes da pasta `templates/`, com isso, é feito um merge dos _templates_ com os comentários extraídos para compor um único arquivo `.md` que constituirá o relatório daquela disciplina. Finalmente, usamos o _Pandoc_ para converter o arquivo `.md` em um `.pdf` que fica salvo na pasta `relatorios/` e tem como nome o titulo e atributos do oferecimento.

A estrutura do relatório é ditada pelos moldes em `tamplates/`, isto é, toda a divisão de sessões e a seleção de quais gráficos serão apresentados é feita aqui.

Além disso, pode ser necessário uma limpeza no arquivo `resultado.csv` para eliminar as quebras de linhas provenientes de comentários.

Finalmente, caso seja necessário o _polimento_ de algum comentário feito, basta editar o respectivo _.md_ na pasta da disciplina e executar novamente o script para geração dos PDF's. 