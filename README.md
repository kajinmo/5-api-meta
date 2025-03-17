# 5-api-meta


- objetos (campanha)
- conectores
- parâmetros


astro dev init
astro dev start
astro dev restart

projeto/
├── dags/
│   └── minha_dag.py
├── include/
│   ├── db.py
│   ├── models.py - define como os dados são armazenados, organizados e relacionados entre si
│   ├── schema.py - usado para validação, definindo como os dados devem ser estruturados ao serem recebidos por uma API 
│   ├── extract.py - contém apenas a lógica de extração de dados da API
│   ├── controller.py # contém a lógica de negócio e a interação com o banco de dados
│   └── utils.py  # Funções auxiliares
└── .env


parei em controller
tentei testar no controller.ipynb
começou a dar uns erros mutcho louco, melhor continuar outro dia

no final, tirar o ipykernel do uv

  File "/usr/local/airflow/include/controller.py", line 1, in <module>
    from .models import Campaign, Ads  # Importe seus Models
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ImportError: cannot import name 'Ads' from 'include.models' (/usr/local/airflow/include/models.py)