# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 13:28:39 2021

@author: user
"""

########### Importation des bibliotheques nécessaire
import nltk,re
import wikipedia
import spacy
nlp = spacy.load("en_core_web_sm")
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


class WebSemanticBackEnd():
###################################################################################################
# fonction du traitement language naturel pour analyser les commentaires des liens
    def preprocessing1(self,documents):
            phrase_Requete=documents.replace("</p>","") # removing </p>
            phrase_Requete=phrase_Requete.replace("<p>"," ")  # removing <p>
            phrase_Requete=phrase_Requete.replace("<"," ")  # removing <
            phrase_Requete=phrase_Requete.replace(">"," ")  # removing <
            phrase_Requete = phrase_Requete.replace("http", " ")
            phrase_Requete = phrase_Requete.replace("www", " ")
            phrase_Requete = re.sub('\s+', ' ', phrase_Requete)
            phrase_Requete = re.sub('\.+', '.', phrase_Requete)
            phrase_Requete = re.sub(r"[0-9](?:\@|'|https?\://)\s+","",phrase_Requete) #delete punctuation
            phrase_Requete = re.sub("[^a-zA-Z]", " ",phrase_Requete)
            phrase_Requete = re.sub(r'[^\w\s]','',phrase_Requete) # remove punctuation
            phrase_Requete = re.sub("\d+","",phrase_Requete) # remove number from text
            tokens_phrase = nltk.word_tokenize(phrase_Requete) # tokenizing the documents
            stopwords = nltk.corpus.stopwords.words('english') #stopword reduction
            tokens_phrase=[w for w in tokens_phrase if w.lower() not in stopwords]
            tokens_phraset=[w.lower() for w in tokens_phrase] #convert to lower case
            tokens_phraset=[w for w in tokens_phrase if len(w)>2] #considering tokens with length>2(meaningful words)
            str1=' '.join(tokens_phraset)
            return str1
    ###################################################################################################
    # fonction du traitement language naturel pour analyser la phrase requete  
    def preprocessing_requete(self,request_sent):
        sansPonc = s = re.sub(r'[^\w\s]','',request_sent)
        Requete=[]
        doc = nlp(sansPonc)
        for token in doc:
            if((token.pos_)!="VERB"):
                Requete.append(token.text)
        stopwords = nltk.corpus.stopwords.words('english') #stopword reduction
        Requete=[w for w in Requete if w.lower() not in stopwords]
        toTextBlob = ' '.join(Requete)
        from textblob import TextBlob
        blob = TextBlob(toTextBlob)
        blob = blob.noun_phrases
        list_of__s=[]
        for word in blob:
            tempWordList = word.split(" ")
            i=0
            while(len(tempWordList)>i+1):
                list_of__s.append(tempWordList[i].capitalize()+"_"+tempWordList[i+1])
                i+=1
        Requete += list_of__s
        return Requete
    ###################################################################################################
    #fonction qui prend en paramètre une phrase et retourne une chaine de caractères à partir Wikipédia
    def search_wikipedia(self,request_sent):
        wiki_help = wikipedia.search(request_sent)
        str1=' '.join(wiki_help)
        print("wikipedia"+str1)
        sentence_data=request_sent+" "+str1
        return sentence_data
    #################################################################################################
    #fonction qui contient une requête de sparql et nous permettant de récupérer un dictionnaire 
    #des liens, des commentaires et les sujets
    def search_dbpedia(self,Requete):
        dict={}
        # <http://dbpedia.org/resource/"""+ Rq.capitalize() +"""_(disambiguation)> dbo:wikiPageDisambiguates $object.
        # rd:"""+ Rq.capitalize() +""" dbo:wikiPageWikiLink $object.
        #rd:"""+ Rq.capitalize() +""" dbo:wikiPageWikiLink $object.
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        for Rq in Requete:
            #print(Rq)
            sparql.setQuery("""
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX rd: <http://dbpedia.org/resource/>
                PREFIX dbo:<http://dbpedia.org/ontology/>
                SELECT  ?object $abs $comment
                WHERE {
                <http://dbpedia.org/resource/"""+ Rq.capitalize() +"""_(disambiguation)> dbo:wikiPageDisambiguates $object.
                $object rdfs:comment $comment.
                $object dbo:abstract $abs.
                FILTER (lang(?abs) = 'en').
                FILTER (lang(?comment) = 'en')
                } 
            """)
            sparql.setReturnFormat(JSON)
            res = sparql.query().convert()
            #result["abs"]["value"]
            for result in res["results"]["bindings"]:
                object_v=result["object"]["value"]
                abs_v=result["abs"]["value"]
                list_abs=[] 
                list_comment=[]
                list_sujet=[]
                list=[]
                comm_v=result["comment"]["value"]
                if len(object_v)!=0:
                    list_sujet.append(Rq.capitalize())
                    list_abs.append(abs_v)
                    list_comment.append(self.preprocessing1(comm_v))
                    list.append(list_abs)
                    list.append(list_comment)
                    list.append(list_sujet)
                    dict[result["object"]["value"]]=list
        return dict
    ###################################################################################################
    #fonction qui prend en paramètre une dictionnaire et chaine de caractére(wikipedia) et retourne 
    # des listes (sujet,commentaire,objet)
    def get_dict(self,dict,sentence_data):
        liste_object=[]
        liste_comment=[]
        liste_sujet=[]
        liste_object.append(sentence_data)
        liste_comment.append(sentence_data)
        liste_sujet.append(sentence_data)
        #print(dict.items())
        for cle, valeur in dict.items():
            #print(cle)
            liste_object.append(cle)
            liste_comment.append(valeur[1][0])
            liste_sujet.append(valeur[2][0])
            #print("=>Cle ", cle,"\n ==>abstract \n", valeur[0]," \n ==>Comment \n" ,valeur[1] ,"\n"
        return liste_sujet,liste_comment,liste_object
   
    #fonction qui calcule la similarité des commentaires des liens dbpedia avec la phrase requête
    def similarity(self,liste_comment,liste_sujet,liste_object,Requete,head):
        tfidf = TfidfVectorizer().fit_transform(liste_comment)
        # no need to normalize, since Vectorizer will return normalized tf-idf
        pairwise_similarity = (tfidf * tfidf.T)
    
        """
            >>> import numpy as np     
                                                                                                                                                                                                                                      
    >>> arr = pairwise_similarity.toarray()     
    >>> np.fill_diagonal(arr, np.nan)                                                                                                                                                                                                                            
                                                                                                                                                                                                                     
    >>> input_doc = Requete                                                                                                                                                                                                  
    >>> input_idx = corpus.index(input_doc)                                                                                                                                                                                                                      
    >>> input_idx                                                                                                                                                                                                                                                
    4
    
    >>> result_idx = np.nanargmax(arr[input_idx])                                                                                                                                                                                                                
    >>> corpus[result_idx] 
        """
    
        t = pairwise_similarity[:,0]
        pdSim = pd.DataFrame(t.todense(),columns=['Requete'])
        ttt = pd.DataFrame(liste_comment,columns=["comment"])
    
        sujet=pd.DataFrame(liste_sujet,columns=["sujet"])
        links = pd.DataFrame(liste_object,columns=["link"])
    
        result = pd.concat([pdSim, ttt,sujet,links], axis=1)
        D1=result.sort_values(by=['Requete'],ascending=False)
        D1=D1.iloc[1:,:]
        return D1
    ####################################################################################################    
    #fonction principale
    def main(self,request_sent,head):
        req=self.preprocessing_requete(request_sent)
        #print(Requete)
        dict=self.search_dbpedia(req)
        #print(dict)
        sentence_data=self.search_wikipedia(request_sent)
        #print(sentence_data)
        liste_sujet,liste_comment,liste_object=self.get_dict(dict,sentence_data)
        #print(liste_comment)
        D1=self.similarity(liste_comment,liste_sujet,liste_object,req,head)
        return D1,req
    def affichage(self,request_sent,head):
        D1,rr=self.main(request_sent, head)
        D2=D1
        D1=D1.head(5)
        for i in range(len(D1)):
            print(D1.iloc[i,0],D1.iloc[i,3])     
        #X=pd.concat([pdSim,sujet,links], axis=1)  
        for sujet in rr:
            x=D2[(D2.sujet == sujet.capitalize())] 
            if len(x)!=0:
                print("les liens similaire à: ",sujet)
            x1=x.head(5)
            for i in range(len(x1)):
                print(x1.iloc[i,0],x1.iloc[i,3])