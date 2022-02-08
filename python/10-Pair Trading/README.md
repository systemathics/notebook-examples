# Pair-Trading

## Objectif du projet (attendu final)

L’objectif de ce PI2 est de développer une stratégie de trading et d'exécution algorithmique pour Systemathics. Avec une équipe constituée de 4 étudiants data scientist et analyst de l'ESILV nous seront conduits à mener une recherche quantitative dans l'objectif d'implémenter à bien une stratégie de **"Pair Trading"** en utilisant des **données statistiques** et des concepts d'**intelligence artificielle** dont le but sera aussi d’affirmer si celle-ci apporte une plus-value à nos résultats ou non.

Par définition, le pair trading (ou investissement par paire) est une méthode de gestion alternative, indifférente aux conditions et fluctuations du marché. Elle débute par une analyse statistique des ratios de convergence et de divergence entre deux valeurs fortement corrélées, devises, actions, ou options. Selon les opportunités qui s’offrirons à nous, nous allons nous porter acheteur d'une valeur pour un montant donné et vendeur d'une autre valeur pour ce même montant.

Une intelligence artificielle peut éventuellement être implémenté lors du choix des actifs corrélés ou bien lors de la gestion des paramètres d’entrées et sorties de positions dans un objectif d’optimiser les résultats si possibles.

Finalement, nous aurons alors à gérer tous les aspects d'un processus de R&D et travailler sur tous les cycles nécessaire au développement d'une stratégie en ayant recours aux services technologiques de Ganymede :

* Ganymede : https://ganymede.cloud/
* Données de marchés: professionnel et sources de données de confiance

Responsabilités :

* Rechercher et implémenter diverses approches de stratégies de trading quantitative basés sur du machine learning
* Optimiser la génération des signaux et l'exécution des ordres
* Collaborer avec des membres de l'équipe interne afin d'améliorer la conception de la stratégie
* Ecrire du code propre et scalable avec Python
* Tester et déployer l'application
* Compléter la documentation, les recherches papiers et articles

## Décomposition en tâches et sous tâches

Le but de ce projet est de proposer une stratégie complète de trading autour du concept de pair trading.

- La première étape est peut être de se renseigner sur les stratégies de trading et notamment le pair trading. Connaître la gestion de risque et de portfolio managment.

Pour pouvoir réaliser une stratégie complète de pair trading il y a 2 étapes majoritaire.

- La première est la sélection de la pair. Pour ça plusieurs modèle sont possible, il faut trouver des pair corréler sur lesquelles on va appliquer la stratégie. Il faut également concevoir un modèle qui actualisera cette sélection tous les x temps. On doit également être capable de dire lorsqu'une paire n'est plus valable pour cette stratégie.
- La deuxième étape et la construction de la stratégie pour une paire. Pour ça le plus important est la réalisation de backtest. La première chose à faire est donc de tester plein de stratégie différents en adaptant les signaux d'achat, de vente mais aussi le place de stop loss ou take profit mais également comment rentrer est sortir d'une position ce qu'on appelle le sizing. Il faut ensuite pouvoir tester ces stratégies sur le passé afin de savoir comment se seraient elles comportées si on les avait lancer dans le passé afin de faire un choix entre plusieurs stratégie

Ces deux étapes sont notre principal objectif pour le projet qui se clôture assez tôt. Si le temps nous le permet nous passerons ensuite à la construction d'une stratégie complète. Pour ça il y a de nombreux points à prendre en compte :

- Le modèle de choix des paires
- Les stratégies à adopter en fonction des paires
- Le portfolio management
- La gestion de risque

Si on devait décomposer en tâche on aurait donc :

1. Se renseigner sur les meilleurs pratique dans les stratégies de pair trading
2. Construire un modèle de sélection de paire
3. Construire une stratégie de pair trading pour chaque paire
4. Construire une gestion complète d'un capital en gérant le risque et les allocations sur chaque stratégies.

Pour chaque point on peut partir soit sur un modèle de type statistique soit un modèle de type machine learning ou deep learning. L'idée de ce projet est également de tester ces différentes options afin de voir si en fonction de chaque point un type de modèle est plus efficace et si il faut les utiliser
## Proposition de planning

Afin d’assurer un bon fonctionnement de ce projet de 4 mois, nous devons nous organiser de manière adaptée en mettant en place des objectifs raisonnables.

Pour cela, notre planning se basera sur les 4 tâches précédemment présentées. 

D’une manière générale, nous organisons des meetings hebdomadaires avec nos partenaires entreprises tous les lundis matin sur le créneau dédié pour le projet PI2, ces meetings permettent à nos partenaires de suivre l’avancement du projet ; de nous guider et de nous aider sur les éventuelles difficultés rencontrées.

De la même manière, nous effectuons aussi des meetings hebdomadaires tous les jeudis, cette fois au sein de notre équipe de projet, dans le but de communiquer et d’échanger les travaux effectués par chaque membre de l’équipe.

Nous fixons souvent des objectifs de court terme à atteindre lors de la réunion de lundi matin, puis nous profitons du meeting de jeudi pour pouvoir faire un point sur l’avancement de chacun.

Nous travaillons de manière assez flexible, nous avons choisi par exemple de travailler en parallèle sur deux parties de pair trading simultanément (sélection de pair et choix de la stratégie) par équipe de deux personnes, les tâches sont attribuées en fonction des compétences techniques et softskills de chacun. Malgré le fait que chaque binôme réalise une tâche différente, mais grâce aux réunions de chaque jeudi, nous participons tous dans la partie d’un autre binôme en suivant leur avancement et en donnant notre avis.

Actuellement nous travaillons sur la première approche de pair trading, et notre organisation variera en adaptant aux objectifs éventuels.
## Risk Management

1) Se documenter sur les meilleures pratiques pour le Pair Trading

Notre tuteur nous ayant fourni deux documents complets sur la stratégie de Pair Trading que nous devons mettre en place ainsi que les bonnes pratiques quant à mise en place d’une stratégie, nous disposons déjà d’une partie de la documentation nécessaire au bon déroulement de ce projet. Il nous faudra tout de même effectuer des recherches complémentaires. Dans le cas où nous n’arriverions pas à obtenir de renseignements pertinents, nous pourrions nous tourner vers des professionnels et demander de l’aide par exemple auprès de professeurs de la majeure IF.

2) Construire un modèle de sélection de paire

Il est difficile d’envisager un échec sur cet objectif étant donné qu’il est primordial quant à la réussite du projet. Cependant, dans le cas où nous échouerions, la stratégie sera mise en place sur des paires d’actions du même secteur dont la corrélation observée sur les dernières années est élevée. Nous disposons déjà de paires répondant à ces critères.

3) Construire une stratégie de Pair Trading sur chaque paire 

De même que pour l’objectif précédent, il est difficile d’envisager un échec pour cette partie. C’est un objectif primordial que d’arriver à construire une stratégie fiable, qui illustrera nos travaux sur l’ensemble de ce semestre. Echouer sur cet objectif reviendrait plus globalement à échouer sur le projet. Dans ce cas l’entreprise devra recruter de la main d’œuvre pour reprendre la où nous aurions échoué. Dans le cas où nous n’aurions rempli complètement cet objectif, l’entreprise devra également recruter de la main d’œuvre pour reprendre nous travaux.

4) Construire une gestion complète d’un capital

Cet objectif a été défini comme secondaire et constituera la dernière étape de ce projet. Dans le cas où nous n’aurions pas le temps d’implémenter un algorithme répondant à cet enjeu, nous devrons nous tourner vers des solutions déjà existantes et compatible avec notre stratégie, ou proposer à l’entreprise d’engager un groupe l’année prochaine pour travailler dessus.
