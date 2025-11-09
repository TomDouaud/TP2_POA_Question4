
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

Aperçu des données :
```csv
  patientId   age sexe  poids  taille  tensionSystolique  tensionDiastolique  cholesterol  glucose  label    imc             catRisque
0     P0001  67.0    F   70.8   170.0              146.0                92.0        135.0     73.0    3.0  24.50  Hypertension stade 1
1     P0002  24.0    H    NaN   166.0              132.0                79.0        223.0    125.0    2.0    NaN       Préhypertension
2     P0003  45.0    F   80.4   158.0              117.0                73.0        224.0    120.0    1.0  32.21                Normal
3     P0004  74.0    H   47.1   170.0              123.0                93.0        246.0    111.0    2.0  16.30       Préhypertension
4     P0005  23.0    F   88.4   174.0              163.0                64.0        159.0    120.0    3.0  29.20  Hypertension stade 2
...
```

![dashboard](analyse_patients.png)

