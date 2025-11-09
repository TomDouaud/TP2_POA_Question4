import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import json

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class AnalyseurDonnees:
    
    def __init__(self):
        self.donnees = None
        self.donnees_nettoyees = None

    def generer_donnees_exemple(self, n_patients: int = 100) -> pd.DataFrame:
        np.random.seed(7)
        
        data = {
            'patientId': [f'P{i:04d}' for i in range(1, n_patients + 1)],
            'age': np.random.randint(20, 80, n_patients),
            'sexe': np.random.choice(['H', 'F'], n_patients),
            'poids': np.random.normal(70, 15, n_patients).round(1),
            'taille': np.random.normal(170, 10, n_patients).round(0),
            'tensionSystolique': np.random.normal(120, 20, n_patients).round(0),
            'tensionDiastolique': np.random.normal(80, 10, n_patients).round(0),
            'cholesterol': np.random.normal(200, 40, n_patients).round(0),
            'glucose': np.random.normal(100, 25, n_patients).round(0),
            'label': np.random.choice([1, 2, 3, 4, 5], n_patients,p=[0.3, 0.25, 0.2, 0.15, 0.1])
        }

        # création du dataframe (et ajout de valeurs manquantes.........)
        df  = pd.DataFrame(data)
        for col in df.columns[1:]:
            # environ 1% de valeurs manquantes par colonne*
            mask = np.random.rand(n_patients) < 0.01
            df.loc[mask, col] = np.nan

        # cacul imc et categorie de risque (https://fr.wikipedia.org/wiki/Hypertension_artérielle#Définition)
        df['imc'] = (df['poids'] / (df['taille'] / 100) ** 2).round(2)
        df['catRisque'] = pd.cut(
            df['tensionSystolique'], 
            bins=[0, 120, 140, 160, 300],
            labels=['Normal', 'Préhypertension', 'Hypertension stade 1', 'Hypertension stade 2']
        )

        self.donnees = df
        return df
    
    def sauvegarder_donness(self, path: str = 'donnees_patients.csv') -> None:
        if self.donnees is not None:
            self.donnees.to_csv(path, index=False)
            print(f'Données sauvegardées dans {path}')
            return True
        return False
    
    def charger_donnees(self, path: str = 'donnees_patients.csv') -> pd.DataFrame:
        try:
            self.donnees = pd.read_csv(path)
            print(f'{len(self.donnees)} patients chargé depuis {path}')
            return self.donnees
        except FileNotFoundError:
            print(f'{path} non trouvé.')
            return None
        
    def nettoyer_donnees(self) -> pd.DataFrame:
        if self.donnees is None:
            raise ValueError("Aucune donnée à nettoyer")

        df_nettoye = self.donnees.copy()

        valeurs_manquantes = df_nettoye.isnull().sum()
        print("Valeurs manquantes par colonne avant nettoyage :")
        for col, count in valeurs_manquantes[valeurs_manquantes > 0].items():
            print(f"\t{col}: {count} valeurs")

        colonnes_num = df_nettoye.select_dtypes(include=[np.number]).columns
        for col in colonnes_num:
            mediane = df_nettoye[col].median()
            df_nettoye[col] = df_nettoye[col].fillna(mediane)
            print(f"Valeurs manquantes dans '{col}' remplacées par la médiane: {mediane}")

        colonnes_cat = df_nettoye.select_dtypes(include=['object']).columns
        for col in colonnes_cat:
            mode = df_nettoye[col].mode()[0]
            df_nettoye[col] = df_nettoye[col].fillna(mode)
            print(f"Valeurs manquantes dans '{col}' remplacées par le mode: {mode}")

        self.donnees_nettoyees = df_nettoye
        print("Nettoyage des données terminé")
        return df_nettoye
    
    def analyser_patients(self, col: str, val: any) -> pd.DataFrame:
        if self.donnees_nettoyees is None:
            raise ValueError("Les données doivent être nettoyées avant l'analyse")

        patients_filtres = self.donnees_nettoyees[self.donnees_nettoyees[col] == val].copy()
        
        print(f"\nAnalyse des patients avec {col} = {val}")
        print("-"*30)
        print(f"Nombre de patients :\t{len(patients_filtres)}")
        print(f"Pourcentage du total :\t{(len(patients_filtres) / len(self.donnees_nettoyees) * 100):.1f}%")

        if len(patients_filtres) > 0:
            # stats descriptives
            print(f"\nStatistiques des patients '{col}={val}' :")
            stats_cols = ['age', 'poids', 'taille', 'imc',
                          'tensionSystolique', 'tensionDiastolique', 
                          'cholesterol', 'glucose']
            stats_resume = patients_filtres[stats_cols].describe()
            print(stats_resume.round(2))

            #  comparaison pop générale
            print(f"\nComparaison avec la population générale :")
            for col in ['age', 'imc', 'tensionSystolique']:
                moyenne_grp = patients_filtres[col].mean()
                moyenne_pop = self.donnees_nettoyees[col].mean()
                diff = ((moyenne_grp - moyenne_pop) / moyenne_pop) * 100
                print(f"\t{col}:\n\t   - Moyenne groupe = {moyenne_grp:.2f},\n\t   - Moyenne pop = {moyenne_pop:.2f},\n\t   - Diff = {diff:+.2f}%")

            # distribution par sexe 
            print(f"\nDistribution par sexe :")
            dist_sexe = patients_filtres['sexe'].value_counts()
            for sexe, count in dist_sexe.items():
                pourcentage = (count / len(patients_filtres)) * 100
                print(f"\t{sexe}: {count} patients ({pourcentage:.1f}%)")

            # patients avec le plus haut imc
            top_imc = patients_filtres.nlargest(5, 'imc')[['patientId', 'imc']]
            print(f"\nTop 5 patients avec le plus haut IMC :")
            print(top_imc.to_string(index=False))

        return patients_filtres


    def display_donnees(self, show_plot: bool = True) -> None:
        if self.donnees is None:
            self.generer_donnees_exemple()

        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Analyse des données de patients', fontsize=16, fontweight='bold')
        
        # distrib labels
        ax1 = axes[0, 0]
        label_counts = self.donnees['label'].value_counts().sort_index()
        colors = ['#FF6B6B', "#CD4EAF", "#45D147", '#FFA07A', "#7DE3CD"]
        bars = ax1.bar(label_counts.index, label_counts.values, color=colors)
        ax1.set_xlabel('Label')
        ax1.set_ylabel('Nombre patients')
        ax1.set_title('Distribution labels')
        ax1.set_xticks(label_counts.index)
        bars[3].set_edgecolor('red') # highlight label 4
        bars[3].set_linewidth(3)
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
            
        # distrib age par label
        ax2 = axes[0, 1]
        for label in sorted(self.donnees['label'].unique()):
            ages = self.donnees[self.donnees['label'] == label]['age']
            ax2.hist(ages, alpha=0.5, label=f'Label {label}', bins=15)
        ax2.set_xlabel('age')
        ax2.set_ylabel('Frequence')
        ax2.set_title('Distribution age par label')
        ax2.legend()

        # imc vs tension pour les patients du label 4
        ax3 = axes[0, 2]
        label_4 = self.donnees[self.donnees['label'] == 4]
        autres = self.donnees[self.donnees['label'] != 4]
        ax3.scatter(autres['imc'], autres['tensionSystolique'], 
                   alpha=0.3, label='Autres labels', s=30)
        ax3.scatter(label_4['imc'], label_4['tensionSystolique'], 
                   color='red', alpha=0.8, label='Label 4', s=50, edgecolors='darkred')
        ax3.set_xlabel('IMC')
        ax3.set_ylabel('Tension systolique')
        ax3.set_title('IMC vs tension (label4 en rouge)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # boxplot des variables par label
        ax4 = axes[1, 0]
        data_for_box = []
        labels_for_box = []
        for label in sorted(self.donnees['label'].unique()):
            data_for_box.append(self.donnees[self.donnees['label'] == label]['cholesterol'].dropna())
            labels_for_box.append(f'L{label}')
        bp = ax4.boxplot(data_for_box, tick_labels=labels_for_box, patch_artist=True)
        for i, box in enumerate(bp['boxes']):
            if i == 3:  # label 4
                box.set_facecolor('red')
                box.set_alpha(0.7)
            else:
                box.set_facecolor('lightblue')
        ax4.set_xlabel('Label')
        ax4.set_ylabel('cholestérol')
        ax4.set_title('distribution du cholesterol par label')

        # matrice de corrélation pour label4
        ax5 = axes[1, 1]
        label_4_data = self.donnees[self.donnees['label'] == 4][
            ['age', 'imc', 'tensionSystolique', 'cholesterol', 'glucose']
        ].dropna()
        if len(label_4_data) > 0:
            corr = label_4_data.corr()
            im = ax5.imshow(corr, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
            ax5.set_xticks(range(len(corr.columns)))
            ax5.set_yticks(range(len(corr.columns)))
            ax5.set_xticklabels(corr.columns, rotation=45, ha='right')
            ax5.set_yticklabels(corr.columns)
            ax5.set_title('Corrélations - patients label 4')
            for i in range(len(corr.columns)): 
                for j in range(len(corr.columns)):
                    text = ax5.text(j, i, f"{corr.iloc[i, j]:.2f}",
                                   ha="center", va="center", color="w" if abs(corr.iloc[i, j]) > 0.5 else "black", fontsize=8)
            
        # repartition par sexe et catégorie de risque
        ax6 = axes[1, 2]
        risk_by_sex = pd.crosstab(self.donnees['sexe'], self.donnees['catRisque'])
        risk_by_sex.plot(kind='bar', stacked=True, ax=ax6, colormap='RdYlBu_r')
        ax6.set_xlabel('Sexe')
        ax6.set_ylabel('Nombre patients')
        ax6.set_title('Répartition de risque par sexe')
        ax6.set_xticklabels(['Femme', 'Homme'], rotation=0)
        ax6.legend(title='Catégorie', bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.tight_layout()
        filename = 'analyse_patients.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"graphiques sauvegardés dans '{filename}'")
        if show_plot:
            plt.show() 

    def generer_rapport(self) -> Dict: 
        if self.donnees is None:
            self.generer_donnees_exemple()

        rapport = {
            'resume_general': {
                'nombre_total_patients': len(self.donnees),
                'age_moyen': self.donnees['age'].mean(),
                'age_min': self.donnees['age'].min(),
                'age_max': self.donnees['age'].max(),
                'ratio_hommes_femmes': f"{(self.donnees['sexe']=='M').sum()}:{(self.donnees['sexe']=='F').sum()}",
                'imc_moyen': self.donnees['imc'].mean()
            },
            'distribution_labels': self.donnees['label'].value_counts().to_dict(),
            'patients_label_4': {
                'nombre': len(self.donnees[self.donnees['label'] == 4]),
                'pourcentage': len(self.donnees[self.donnees['label'] == 4]) / len(self.donnees) * 100,
                'age_moyen': self.donnees[self.donnees['label'] == 4]['age'].mean() if len(self.donnees[self.donnees['label'] == 4]) > 0 else 0,
                'liste_ids': self.donnees[self.donnees['label'] == 4]['patientId'].tolist()
            },
            'statistiques_sante': {
                'tension_moyenne': f"{self.donnees['tensionSystolique'].mean():.0f}/{self.donnees['tensionDiastolique'].mean():.0f}",
                'cholesterol_moyen': self.donnees['cholesterol'].mean(),
                'glucose_moyen': self.donnees['glucose'].mean(),
                'patients_hypertendus': len(self.donnees[self.donnees['tensionSystolique'] > 140])
            }
        }

        return rapport
    
    def export_rapport(self, path: str = 'rapport_analyse.json') -> None:
        rapport = self.generer_rapport()

        def convert_numpy(obj): # conversion types numpu en types python
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convert_numpy(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy(item) for item in obj]
            return obj
        
        rapport_clean = convert_numpy(rapport)

        with open(path, 'w') as f:
            json.dump(rapport_clean, f, ensure_ascii=False, indent=2)
        
        print(f"Rapport sauvegardé dans '{path}'")
        return rapport_clean    
    
def main():
    print("\n"+"="*30)
    print("ANALYSE DES DONNÉES DE PATIENTS")
    print("="*30+"\n")
    
    # initalisation de l'analyseur
    analyseur = AnalyseurDonnees()

    # génération et sauvegarde des données
    print("\nGénération des données d'exemple")
    print("-"*30)
    data = analyseur.generer_donnees_exemple(1000)
    print(f"{len(data)} patients générés.")
    
    print("\nAperçu des données :")
    print(data.head())
    analyseur.sauvegarder_donness('donnees_patients.csv')

    # nettoyage données
    print("\nNettoyage des données")
    print("-"*30)
    data_nettoyees = analyseur.nettoyer_donnees()

    # analyse des patients avec label 4
    patients_label_4 = analyseur.analyser_patients('label', 4)

    # affichage des visus
    print("\nAffichage des visualisations")
    print("-"*30)
    analyseur.display_donnees(show_plot=False)

    # génération du rapport
    print("\nGénération du rapport")
    print("-"*30)
    rapport = analyseur.generer_rapport()
    print("\nrésumé du rapport :")
    print(f"\t- Nombre total de patients : {rapport['resume_general']['nombre_total_patients']}\n\t- Age moyen : {rapport['resume_general']['age_moyen']:.1f} ans\n\t- Patients avec label 4 : {rapport['patients_label_4']['nombre']} ({rapport['patients_label_4']['pourcentage']:.1f}%)\n\t- patiens hypertendus : {rapport['statistiques_sante']['patients_hypertendus']}")

    #export rapport
    analyseur.export_rapport('rapport_analyse.json')

if __name__ == "__main__":
    main()

