Le `Service` est une class python pour regrouper la logique de backend , dans ce projet est responsable d'analyser et visualiser les caractéristiques dynamiques de systèmes linéaires, tels que des fonctions de transfert ou des représentations d'espace d'état. Elle utilise la bibliothèque `control` pour les calculs et `matplotlib` pour les visualisations. Voici une explication détaillée :

---

### Importations et initialisation
- **Modules utilisés :**
  - `control` : Pour les calculs des systèmes linéaires (pôles, zéros, réponses, etc.).
  - `matplotlib` et `io` : Pour générer et enregistrer des graphiques comme des fichiers image (SVG).
  - `numpy` : Pour les calculs numériques.
  - `Pillow` : Pour compresser et manipuler les images.
  - `flask` : Pour servir des fichiers (comme des images générées) via une API , dans ce cas la il est le coeur de ce project backend.
  - `helpers.plotter` : Un module personnalisé pour gérer la création des graphiques.
  - `helpers.sanitize_data` : Une fonction utilitaire pour nettoyer ou valider les données .

- **Initialisation :**
  - La classe `Service` hérite de `BaseService` et utilise un objet `Plotter` pour simplifier la création des graphiques.
  - La classe `Plotter` est une class creer pour regrouper la logique de visualisation en applicant le principe de L'Encapsulation `Encapsulation`.
  - La classe `BaseService` est creet pour regrouper les fonctions et attribus communes entre les services de ce projet.
---

### Méthodes principales

#### 1. **`pole_zero`** :
- Génére un diagramme des pôles et zéros d'un système.
- Utilise `ctrl.pzmap` pour identifier les pôles et zéros.
- Le graphique est sauvegardé en SVG et renvoyé comme réponse HTTP via `send_file`.

---

#### 2. **Réponses temporelles :**
- Méthodes : `step`, `impulse`, `ramp`.
- **`step` :** Génère la réponse indicielle (step response).
- **`impulse` :** Génère la réponse impulsionnelle.
- **`ramp` :** Génère la réponse à une entrée en rampe.
- Processus commun :
  1. Calcul du vecteur de temps avec `generate_time` en donnant le t_max.
  2. Calcul de la réponse temporelle via `ctrl.step_response`, `ctrl.impulse_response`, ou `ctrl.forced_response`.
  3. Utilisation de `plotter.plot` pour créer un graphique.
  4. Retourne l'image au format SVG.

---

#### 3. **`bode` :**
- Génère un diagramme de Bode pour analyser la réponse fréquentielle.
- **`bode`** génère un graphique avec les courbes de magnitude et de phase.

---

#### 4. **Stabilité et performance :**
- **`bode_performance` :** Retourne les marges de stabilité (gain, phase, fréquence, etc.) en JSON.
- **`performance` :** Calcule les métriques de performance dynamique :
  - Valeur finale
  - Overshoot (dépassement)
  - Temps de pic
  - Amplitude de pic
  - Temps de montée
  - Temps de stabilisation
- Ces données sont renvoyées sous forme de JSON.

---

#### 5. **Nyquist :**
- La méthode `nyquist` génère un diagramme de Nyquist pour analyser la stabilité du système.
- Les fréquences sont échantillonnées logarithmiquement pour couvrir une large plage.

---

#### 6. **Conversion entre modèles :**
- **`convert_tf_to_ss`** : Convertit une fonction de transfert (TF) en espace d'état (SS).
- **`convert_ss_to_tf`** : Convertit un modèle d'espace d'état (SS) en fonction de transfert (TF).

---

#### 7. **Boucle fermée :**
- **`closed_loop` :** Crée une boucle fermée avec une rétroaction unitaire (feedback).
- Retourne le nouveau système en boucle fermée.

---

### Calculs auxiliaires
- Méthodes comme `calculate_overshoot`, `calculate_peak`, `calculate_rise_time`, etc., sont utilisées pour extraire des métriques spécifiques des réponses temporelles.
- Par exemple :
  - **Temps de montée (`rise_time`)** : Temps nécessaire pour que la réponse passe de 10 % à 90 % de la valeur finale.
  - **Temps de stabilisation (`settling`)** : Temps pour lequel la réponse reste dans une bande de tolérance autour de la valeur finale.

---

### Retour des résultats
- Les résultats (graphiques ou données) sont renvoyés sous forme de fichiers SVG ou de réponses JSON.
- Les images SVG permettent un rendu vectoriel haute qualité dans les applications web.

---

### Points clés :
1. Le service est conçu pour une API Flask où chaque méthode produit un résultat visualisable (diagramme) ou des métriques utiles.
2. Le code est modulaire avec un mélange de calculs analytiques (`control`) et de présentation graphique (`matplotlib`).
3. La structure facilite l'analyse des systèmes dynamiques dans des applications web ou des outils d'apprentissage.