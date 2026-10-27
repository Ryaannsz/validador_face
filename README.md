# Validador facial por imagens

Projeto Python que usa DeepFace (Facenet512) para reconhecer rostos e OpenCV para ler, detectar e desenhar nas imagens. Processa todos os rostos de cada foto separadamente.

## Estrutura

```text
validador_face/
├── reconhecer.py          # Ponto de entrada da aplicação.
├── validador/             # Código organizado por responsabilidade.
│   ├── __init__.py
│   ├── __main__.py        # Execução com uv run python -m validador.
│   ├── cli.py             # Argumentos, validações e execução em lote.
│   ├── config.py          # Caminhos, modelo, extensões e cores.
│   ├── arquivos.py        # Leitura de imagens e gravação de JPEG/JSON.
│   ├── cadastro.py        # Carregamento das pessoas autorizadas.
│   ├── reconhecimento.py  # Extração e comparação facial com DeepFace.
│   ├── anotacao.py        # Bounding boxes, textos e visualização.
│   └── processamento.py   # Coordenação da análise de uma imagem.
├── pyproject.toml        # Dependências e configuração do projeto uv.
├── uv.lock               # Versões exatas das dependências.
├── .python-version       # Python 3.11.
├── .venv/                # Ambiente virtual gerenciado pelo uv.
├── pessoas_autorizadas/
│   ├── Angelina_Jolie/    # Referência da pessoa autorizada na demonstração.
│   └── pessoa_exemplo/    # Coloque aqui fotos de UMA pessoa autorizada.
├── fotos_teste/
│   └── famosos/          # Fotos de demonstração e fontes.json.
├── resultados/           # Imagens marcadas e relatórios JSON gerados.
└── modelos/              # Pesos baixados automaticamente na primeira análise.
```

`reconhecer.py` chama a interface de linha de comando em `validador/cli.py`. O processamento usa os módulos de cadastro, reconhecimento, arquivos e anotação. Os caminhos padrão são calculados a partir da raiz do projeto, independentemente da pasta de onde o comando é executado.

O projeto inclui fotos de famosos para demonstração. Para cadastrar suas próprias pessoas, crie uma subpasta para cada pessoa autorizada, usando o nome dela: `pessoas_autorizadas/ana/foto1.jpg`, por exemplo. É possível colocar várias fotos da mesma pessoa. Cada foto de cadastro precisa ter exatamente um rosto; imagens sem rosto ou com várias pessoas são ignoradas com aviso. Fotos colocadas diretamente na pasta de autorizados usam o nome do arquivo como identificação.

Em `fotos_teste`, adicione fotos diferentes das usadas no cadastro, incluindo pessoas autorizadas, desconhecidas e, se desejar, várias pessoas na mesma foto. São aceitos JPG, JPEG, PNG, BMP e WEBP. As fotos originais são preservadas.

## Fotos de demonstração

Somente Angelina Jolie está cadastrada em `pessoas_autorizadas/Angelina_Jolie/referencia.jpg`. A foto usada para testá-la é diferente da referência.

| Foto em `fotos_teste/famosos/` | Pessoa | Resultado esperado |
| --- | --- | --- |
| `angelina_jolie.jpg` | Angelina Jolie | `ACESSO LIBERADO` |
| `jennifer_aniston.jpg` | Jennifer Aniston | `ACESSO NEGADO` |
| `scarlett_johansson.jpg` | Scarlett Johansson | `ACESSO NEGADO` |
| `katy_perry.jpg` | Katy Perry | `ACESSO NEGADO` |

As fotos vêm do [conjunto de testes do DeepFace](https://github.com/serengil/deepface/tree/master/tests/unit/dataset). Os rótulos seguem os exemplos do autor: [identidades do conjunto](https://sefiks.com/2020/05/22/fine-tuning-the-threshold-in-face-recognition/) e [fotos de referência por pessoa](https://sefiks.com/2021/03/02/deep-face-recognition-with-redis/). `fotos_teste/famosos/fontes.json` registra a URL de cada foto, o commit de origem, o hash SHA-256 e o resultado esperado.

Execute `uv run python reconhecer.py` para analisar todas as fotos. Os resultados desta demonstração ficam em `resultados/famosos/`. Para abrir somente a foto autorizada marcada, execute:

```bash
uv run python reconhecer.py --imagem fotos_teste/famosos/angelina_jolie.jpg --mostrar
```

As permissões deste exemplo são definidas pela presença das fotos no cadastro; os nomes dos arquivos de teste não determinam o resultado. Para retirar Angelina da lista de autorizados, remova sua foto de `pessoas_autorizadas/`.

## Instalação

O projeto usa [uv](https://docs.astral.sh/uv/) para gerenciar Python 3.11, o ambiente virtual e as dependências. Se precisar instalar o uv no macOS com Homebrew, execute `brew install uv`.

Prepare o ambiente na raiz do projeto:

```bash
cd /Users/ryanbernardo/Documents/Faculdade/MachineLearning/validador_face
uv sync --locked
```

O uv seleciona a versão de Python indicada em `.python-version` e cria ou atualiza `.venv/` usando as versões de `uv.lock`. Caso Python 3.11 não esteja instalado, o uv pode baixá-lo automaticamente. Execute os comandos com `uv run` para usar esse ambiente sem precisar ativá-lo no terminal.

As dependências são declaradas em `pyproject.toml`. Para adicionar uma biblioteca, use `uv add nome-da-biblioteca`; para removê-la, use `uv remove nome-da-biblioteca`. Essas operações atualizam a configuração, o lockfile e o ambiente. Mantenha `pyproject.toml`, `uv.lock` e `.python-version` no controle de versão. A pasta `.venv/` já está no `.gitignore`.

## Uso

Analisar todas as fotos de teste:

```bash
uv run python reconhecer.py
```

Também pode executar `uv run python -m validador` na raiz do projeto, com os mesmos argumentos.

Analisar uma foto e abrir o resultado:

```bash
uv run python reconhecer.py --imagem fotos_teste/minha_foto.jpg --mostrar
```

Pressione qualquer tecla para fechar a janela. Sem `--mostrar`, os resultados são apenas salvos.

Definir um limite de comparação personalizado:

```bash
uv run python reconhecer.py --limiar 0.25
```

Sem esse argumento, é usado o limite do DeepFace para Facenet512 e distância cosseno. Um limite menor exige maior semelhança; o valor deve ser ajustado com suas fotos de teste.

## Resultado visual

- A bounding box é **verde** para acesso liberado e **vermelha** para acesso negado, conforme o enunciado do professor.
- Pessoa reconhecida: texto **verde** `ACESSO LIBERADO`.
- Pessoa desconhecida: texto **vermelho** `ACESSO NEGADO`.
- Nenhum rosto: mensagem vermelha `ACESSO NEGADO - nenhum rosto detectado`, sem inventar uma caixa de rosto.
- Cadastro vazio: todos os rostos recebem `ACESSO NEGADO`.

As imagens marcadas e os relatórios JSON são gravados em `resultados/`. Cada relatório contém as caixas e, quando reconhecida, a pessoa, a referência, a distância e o limite de comparação. Não contém os vetores faciais.

O primeiro processamento precisa de internet para baixar os pesos em `modelos/.deepface/weights/`. O cadastro é carregado uma vez por execução; adicionar ou excluir fotos é refletido na próxima execução. O projeto compara fotografias e não verifica presença física ou vivacidade.

Referência da API utilizada: [documentação oficial do DeepFace](https://github.com/serengil/deepface).
