# Control System Software
# Documentation pour le site web des systèmes de contrôle

## Aperçu
Ce site est conçu pour les ingénieurs, chercheurs et étudiants travaillant sur les systèmes de contrôle. Il fournit une plateforme pour analyser et simuler des modèles de systèmes de contrôle. Les utilisateurs peuvent saisir des modèles de systèmes dans deux formats :

1. **Fonction de transfert**
2. **Représentation en espace d'états**

Après avoir saisi le modèle du système, les utilisateurs peuvent choisir parmi une variété d'options d'analyse et de visualisation.

---

## Fonctionnalités principales

### 1. **Saisir le modèle du système**
Les utilisateurs peuvent définir leur système dans l'un des formats suivants :

- **Fonction de transfert** : Spécifiez les polynômes du numérateur et du dénominateur.
- **Représentation en espace d'états** : Fournissez les matrices A, B, C et D pour définir le modèle en espace d'états.

### 2. **Options d'analyse**
Une fois le modèle du système défini, les utilisateurs peuvent sélectionner une ou plusieurs options d'analyse parmi la liste suivante :

#### a. **Réponse indicielle**
- Affiche la réponse du système à une entrée en échelon unité.
- Visualisée sous forme de graphique temporel.

#### b. **Réponse impulsionnelle**
- Affiche la réponse du système à une entrée en impulsion unité.
- Utile pour comprendre le comportement transitoire.

#### c. **Réponse à une rampe**
- Simule la réponse du système à une entrée en rampe.
- Fournit des informations sur le comportement en régime permanent.

#### d. **Diagramme de Bode**
- Analyse en fréquence montrant les graphiques d'amplitude et de phase.
- Utile pour analyser la stabilité et la réponse en fréquence.

#### e. **Diagramme de Nyquist**
- Trace la réponse en fréquence complexe.
- Aide à évaluer la stabilité à l'aide du critère de Nyquist.

#### f. **Carte pôles-zéros**
- Visualise les pôles et les zéros du système.
- Aide à comprendre la stabilité et la dynamique du système.

### 3. **Conversions de modèles**
Les utilisateurs peuvent effectuer des conversions entre différentes représentations et configurations :

#### a. **Boucle ouverte vers boucle fermée**
- Convertit le système en boucle ouverte en une configuration en boucle fermée.
- Nécessite de spécifier le type de rétroaction (unité ou personnalisée).

#### b. **Espace d'états vers fonction de transfert**
- Convertit le modèle en espace d'états en sa fonction de transfert équivalente.

#### c. **Fonction de transfert vers espace d'états**
- Convertit la fonction de transfert en sa représentation équivalente en espace d'états.

---

## Guide d'utilisation

### 1. **Saisir les données du système**
- Accédez à la section de saisie.
- Choisissez entre **Fonction de transfert** ou **Espace d'états**.
- Entrez les données requises dans les champs prévus.

### 2. **Sélectionner les options d'analyse**
- Après avoir saisi le modèle du système, une liste des analyses disponibles s'affichera.
- Sélectionnez les options d'analyse souhaitées.
- Cliquez sur le bouton **Exécuter l'analyse** pour générer les résultats.

### 3. **Visualiser les résultats**
- Les résultats seront affichés sous forme de graphiques ou de valeurs numériques, selon l'analyse.
- Les utilisateurs peuvent télécharger les graphiques ou exporter les données pour une utilisation ultérieure.

### 4. **Effectuer des conversions**
- Accédez à la section **Conversions de modèles**.
- Sélectionnez le type de conversion.
- Fournissez les données nécessaires (par ex. gain de rétroaction pour les conversions en boucle fermée).
- Visualisez le modèle converti dans le format souhaité.

---

## Améliorations futures
- **Prise en charge des systèmes à temps discret**
- **L'ajout des algorithmes d'optimisation** : Pour aide aux calcules des coefficients de PID
- **Signaux d'entrée personnalisés** : Permettre aux utilisateurs de définir des signaux d'entrée arbitraires.
- **Analyse avancée des contrôles** : Inclure des diagrammes du lieu des racines, une analyse de contrôlabilité et d'observabilité.
- **Application de Schema Bloc** : Pour une etude plus claire et plus flexible
---

## Lien Supplementaires
### Website Live: [ici](https://control-system-software-frontend-v816-5ewq8fqkw.vercel.app/)
### Depos Frontend: [ici](https://github.com/wadoud1234/control_system_software_frontend)

### Contact:
Pour des retours ou un support, veuillez nous contacter [ici](mailto:wadoudazer1234@gmail.com).

