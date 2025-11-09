
#### Question B 

##### à faire
Analyse des données de santé :
- génération données patients avec erreurs/valeurs manquantes + colonnes calculées (imc)
- nettoyage du dataset (remplacement des valeurs manquantes par la médiane plutot que suppression car les autres données importantes)
- statistiques descriptives (moyenne, médiane, écart-type)
- autres analyses (repartition sexe, classement imc...)
- visualisations : distrib labels, scatterplot imc vs tension systolique, histo cholesterol par label, matrice corrélation, répartition risque par sexe
- rapport json avec stats

##### exécution du code

```bash
pip install -r requirements.txt
python exo4_b.py
```

Les données générées seront sauvegardées dans `donnees_patients.csv` et le rapport dans `rapport_analyse.json`.
Le dashboard de visualisations sera sauvegardé dans `analyse_patients.png`.