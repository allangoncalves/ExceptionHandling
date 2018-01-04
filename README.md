# ExceptionHandling

1. Execute o **repos_by_watchers.py** para obter os 1000 repositórios com mais watchers do github
2. Insira seu Token da API do Github dentro dos arquivos **collect_tags.py** e **collect_releases.py**
3. Execute **collect_tags.py** ou **collect_releases.py** para baixar as versões do projeto
  * É possível baixar todas as versões de todos os projetos omitindo todos os parametros _python collect_tags.py_
  * Para baixar todas as versões de um único projeto você deve passar o nome do usuario e o nome do repositório _python collect_tags.py pandas-dev pandas_
  * Para baixar as ultimas N versões de um único projeto além do nome do usuário e do repositório, insira a quantidade de versões _python collect_tags.py pandas-dev pandas 10_
4. Execute o **calculate_metrics.py** e passe o caminho para o projeto que deseja realizar as analises _python calculate_metrics.py resultados/pandas/_
5. Após rodar o **calculate_metrics.py** para cada projeto a ser analisado, execute o **make_plots** para gerar as figuras com os gráficos _python make_plots.py_
