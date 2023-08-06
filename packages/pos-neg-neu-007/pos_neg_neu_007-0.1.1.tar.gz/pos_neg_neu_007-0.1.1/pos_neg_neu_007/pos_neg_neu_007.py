#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords

stop_words=set(stopwords.words('english'))
import nltk
nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()


# In[10]:


keywordSet = {'no','none','never','not','nor',"AINT","AIN'T","AREN'T","ARENT",'opposite',"CANNOT","CAN'T","CANT","COULDN'T","COULDNT","DIDN'T","DIDNT","DOESN'T","DOESNT","DON'T","DONT","HAVEN'T","HAVENT","ISN'T","ISNT","NEITHER","NEVER","NEVER","NO","NONE","NOR","NOT","NOTHING","SELDOM","SHOULDN'T","SHOULDNT","WASN'T","WASNT","WEREN'T","WERENT","WITHOUT","WON'T","WONT","WOULDN't",'lack','lacks'}
negation=[str.lower(i) for i in keywordSet]


# In[11]:


#########################################################################################################################################


# In[12]:


def pos_neg_neu(sentence):
  
  s21=fragment(sentence)
  
  wt1=word_tag(s21)
  
  wst1=word_score_tag(wt1)
  
  sentiment=pos_neg(wst1) 
 
  if sentiment==0:
     return 'neutral'
  elif .5>sentiment>0:
     return 'less positive'
  elif .8>=sentiment>=.5:
       return 'positive'
  elif sentiment>.8:
        return 'high positive'
  elif 0>sentiment>-.3:
     return 'less negative'
  elif -.2>=sentiment>=-.8:
        return 'negative'
  elif sentiment<-.8:
        return 'high negative'


# In[13]:


#####################################################################################################################################


# In[14]:


def fragment(s) :
 s1=s.replace('\n',' ')
 s11=sent_tokenize(s1)
 s21=[]
 for i in s11:
     s21.extend(i.split(','))
 return s21


# In[15]:


############################################################################################################################################################


# In[16]:


def word_tag(s21)  :
  wt1=[]
  for k in s21:
      
      s2=k.translate ({ord(c): "" for c in "&#^()*[]{};/<>.|,`~=_+:-"}).strip()
      wt=[(i.strip(),nltk.pos_tag([i.strip()])[0][1]) for i in s2.split()]
      wt1.append([i for i in wt if i[1].startswith('NN') or  i[1].startswith('RB') or  i[1].startswith('JJ') or  i[1].startswith('CC')])
  return wt1


# In[17]:


#################################################################################################################################


# In[18]:


def word_score_tag(wt1):
   wst1=[]
   for i in wt1:
       wst=[]
       for j in i:
          pol=TextBlob(j[0]).sentiment[0]
          if pol==0:
              
              if sid.polarity_scores(j[0])['pos'] >sid.polarity_scores(j[0])['neg'] :
                 pol=sid.polarity_scores(j[0])['pos']
              elif sid.polarity_scores(j[0])['pos'] < sid.polarity_scores(j[0])['neg'] :
                 pol=-sid.polarity_scores(j[0])['neg']
              else:                                                            
                    pol=0                                                            
          tag=nltk.pos_tag([j[0]])[0][1]
          if pol!=0:
            wst.append([j[0],pol,tag]) 
          else: 
            wst.append([j[0],0,tag])
       wst1.append(wst)
   return wst1


# In[19]:




################################################################################################################################


# In[20]:


def pos_neg(wst1):
   sen1=[]
    
   for i in wst1:
        sen=[]
        for j in i:
            sen.append(j[1])
        #print(sen)
        for j in range(1,len(i)):            
                if  i[j][0] not in negation and i[j-1][0] in negation :
                    
                    sen[j]=-sen[j]/1.5
                    sen[j-1]=0
                    
                if   i[j][2]=='RB' and i[j][1]==0 and i[j][0] not in negation and i[j-1][0] in negation:            
                    sen[j]=-.3
                    
                    sen[j-1]=0
                    
                if   i[j][2]=='RBR' and i[j][1]==0 and i[j][0] not in negation and i[j-1][0] in negation:            
                    sen[j]=-.7
                    
                    sen[j-1]=0
                    
                if   i[j][2]=='RBS' and i[j][1]==0 and i[j][0] not in negation and i[j-1][0] in negation:            
                    sen[j]=-1
                    
                    sen[j-1]=0
                    
                #print(sen)
                ######################################################################################################
                if i[j-1][0] not in negation and i[j-1][2].startswith('RB'):  
                     if i[j-1][2].startswith('RB') and sen[j]<0:               
                               sen[j]=sen[j]-sen[j-1]                
                               sen[j-1]=0
                               
                     if i[j-1][2].startswith('RB') and sen[j]>0:  
                               sen[j]=sen[j]+sen[j-1]                  
                               sen[j-1]=0
                  
                            
        #print(sum(sen))
        sen1.append(sum(sen)) 
   return sum(sen1)


# In[ ]:




