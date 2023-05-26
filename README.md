# CMR API - Projeto PortalCMR2 (back-end)

API de comunicação do Centro de Monitoramento Remoto da Funai.

- Para visualizar o homologação clique [aqui](https://homolog-cmr-app-oq5garjiiq-uc.a.run.app/pt-br/catalog)

# Arquitetura e Stack

Este serviço faz parte de um conjunto de serviços estruturados em uma arquitetura de microserviços, o CMR2 foi pensado para ser uma evolução do [CMR](https://cmr.funai.gov.br/).

### Detalhes da stack e integrações (back end):

- A implementação é feita em [python3](https://www.python.org/downloads/)
- Uso do framework [django rest framework](https://www.django-rest-framework.org/)
- Persistência de dados é feita em um banco [PostgreSql](https://www.postgresql.org/)
- Utilização de [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/) para implementação da infraestrutura
- Consumo de dados geoespaciais utilizando [geoserver](https://geoserver.org/)

### Detalhes da stack e integrações (front end):

- A implementação é feita em [javascript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript)
- Uso do framework [Vue](https://vuejs.org/) e [vuetify](https://vuetifyjs.com/)
- Contém um sistema de mapa interativo construido utilizando [leaflet](https://leafletjs.com/)

# Execução do código

- Execute docker-compose up --build dev para executar o sistema em modo desenvolvimento.

# Detalhes sobre Autenticação e Autorização

No backend são tratadas as regras de negócio e autenticação do PortalCMR2.
Da APP são esperados os dados do usuário autenticado (usuário e senha), como retorno é encaminhado um token de autenticação possibilitando consumo de todos os acessos e permissões concedidas aos usuários conforme definido pelo administrador do sistema.

### Autenticação

Para este projeto foi adotada o método de autenticação JWT(Json Web Token). Aplicada em servidores com protocolo HTTPS, essa metodologia realiza a autenticação por tokens.
Esse token é gerado quando o usuário entra na aplicação, por meio de seu usuário e senha encaminhados pela APP,
é gerado uma string de caracteres codificada utilizada para validação do acesso e contendo outros parametros implemetados pelo pacote python SimpleJWT.

### Autorização (Acessos e Permissões)

As permissões ao sistema aqui utilizadas são as do framework Django REST Framework do pacote django.contrib.auth.
Foram adotadas as DjangoModelPermissions, ou seja, o maior grau de granularidade aplicado a esse projeto é a nível de model(tabela).
Obs.: Para o cenário desenhado, ainda não foi necessário a aplicação de permissões a nível de objeto (DjangoObjectPermissions)

    Todas as permissões são concedidas aos usuário apenas por Grupos,
    não é concedida nenhuma permissão diretamente a um usuário específico,
    visando uma melhor gestão sobre o PortalCMR2.

    As permissões ao consumo do BackEnd foram divididas em dois níves:
        Nível 01 --> Acesso aos módulos do PortalCMR2;
        Nível 02 --> Consumo e iteração dos dados persistidos em banco de dados pelo usuário.
    Obs.: Para evitar o erro de exeção de "Permissão Negada", é necessário que o usuário tenha acesso ao dado (Nível 01) e permissão ao dado (Nível 02).

    As permissões default do sistema possuir 5 ações implementadas:
        "view_" --> consultar, leitura e/ou visualização os dados;
        "add_" --> cadastrar, adicionar e/ou criar informações e dados;
        "change_" --> atualização do dado (update), permite editá-los;
        "delete_" --> remover e/ou apagar dados e registros da base;
        "access_" --> informa se o usuário logado pode consumir e/ou acesso o dado.
    Obs.: Caso necessário, para atendimento da regra de négocio instituida, é possível adicionar permissões customizadas a cada model individualmente.

    Nível 01 - Camada de acesso
        Cada Módulo do CMR2 é composto por um ou mais conjuntos de dados.
        Objetivando atender uma demanda específica, cada MóduloCMR2 é uma especificidade do projeto, onde juntos compõem o PortalCMR2.
        Na implementação de cada MóduloCMR2 é possível listar as models que compõe os conjuntos de dados utilizados por cada MóduloCMR2.
        Para acessar a cada um desses MóduloCMR2, é criada uma permissão de acesso default chamada "access_",
        adicionada automaticamente as models dos APPs listados no setting.INSTALLED_APPS.
        Esse acesso tem por finalidade agrupar as models que cada um dos módulos do PortalCMR2 fazem uso,
        dessa forma cada MóduloCMR2 só é possível ser acessado pelo usuário que tiver atrelado ao seu perfil a ação "access_" da model requisitada conforme definido pela equipe de negocio e gestão.

    Nível 02 - Camada de permissões
        Fazendo uso do pacote django.contrib.auth, por padrão, é criado automaticamente 4 ações de permissões nas models dos APPs listados no setting.INSTALLED_APPS.
        Esses 4 parâmetros de permissões correspondem as operações básicas de CRUD (Create - "add_", Read - "view_", Update - "change_" e Delete - "delete_")
        foram incorporados a funcionalidade dos sistemas para definição dos papeis dos grupos de usuários no manuseio dos dados existentes no ProjetoCMR.
