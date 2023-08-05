from regtester.RegExTestItem import RegExTestItem
from regtester.RegExTest import RegExTest
import regex
import re
from re import RegexFlag
from typing import Pattern, List


class LawTypeTest(RegExTest):

    def get_regex(self) -> str:
        return r"""
        # USE THIS WITH r WHEN CREATING THE STRING IN PYTHON
        ^.{0,100}(d(?:é|e)cret|arr(?:e|ê)t(?:e|é)\s*minist(?:e|é)riel|loi)\s+n°\s*(\d{1,4})(?:\s*)(\S+)?(-\d{1,4}|\d{1,4}\s*(\S{1,3}-\S{1,4}-\S{4}\s*)?)?\s*(?:en\s+date)?\s*du\s+(?:(?:lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)?\s+(\d{1,2}\s+(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre|\d{1,2})\s+\d{2,4}))\s+(?:(?:portant|relatif|modifiant|fixant)(?:code)?\s+(?:de)?\s*(.*?)\.)?
        """

    def get_regex_flags(self)-> RegexFlag:
        return re.DOTALL|re.M|re.VERBOSE
    
    def get_regex_name(self)-> str:
        return "extract_doc_type"
        
    def get_tests(self)-> List[RegExTestItem]:
        return [
            RegExTestItem(
                text= """
                LOI n° 2009-24 du 8 juillet 2009 LOI n° 2009-24 du 8 juillet 2009 portant Code de l’Assainissement.
                 EXPOSE DE MOTIFS L’Etat du Sénégal s’est engagé, depuis 2005, dans le processus 
                 d’attente des Objectifs du Millénaire pour le Développement (OMD) qui consistent
                  à réduire de moitié la pauvreté dans les pays en développement, non pas en termes de 
                """,
                expected_result={
                    'doc_type': "loi", 'date': "8 juillet 2009", 
                    'obj': "Code de l’Assainissement", 'number': "2009-24"
                    }
            ),
             RegExTestItem(
                text= """
                Arrêté ministériel n° 9523 MEF-CGCPE en date du 17 octobre 2007 portant collecte d’informations comptables.
                 Article premier. - La Cellule de Gestion et de Contrôle du Portefeuille de l’Etat est 
                 habilité à collecter auprès des entreprises du secteur parapublic et des sociétés
                  anonymes à participation publique minoritaire, les documents suivants : 
                """,
                expected_result={
                    'doc_type': "Arrêté ministériel", 'date': "17 octobre 2007", 
                    'obj': "collecte d’informations comptables", 'number': "9523 MEF-CGCPE"
                    }            )
        ]

    def exec_regex(self, regex:Pattern, text:str)-> any:
        results = regex.findall(text)
        if len(results) <= 0:
            return None
        else:
            match = results[0]
            doc_type = match[0].lower()
            number = match[1] + " " + match[2]
            date = match[5].lower()
            obj = match[6].lower()
            return {'doc_type': doc_type, 'date': date, 'obj': obj, 'number': number}
