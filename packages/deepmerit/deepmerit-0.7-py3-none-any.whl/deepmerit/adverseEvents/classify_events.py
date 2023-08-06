#Code
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import scale, MinMaxScaler, StandardScaler
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.decomposition import PCA
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import fbeta_score, precision_score, make_scorer, average_precision_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
import datetime
import matplotlib.pyplot as plt
from scipy import interp
from itertools import cycle
from sklearn.metrics import auc, roc_curve, roc_auc_score
mlb = MultiLabelBinarizer()
def stitch_to_pubchem(_id):
    assert _id.startswith("CID")
    return int(int(_id[3:]) - 1e8)
columns = [
    'stitch_id_flat',
    'stitch_id_sterio',
    'umls_cui_from_label',
    'meddra_type',
    'umls_cui_from_meddra',
    'side_effect_name',
]
df = pd.read_table('../data/meddra_all_se.tsv', names=columns)
df.drop(df[df.meddra_type == "LLT"].index, inplace=True)
df = df.groupby('stitch_id_flat').side_effect_name.apply(list).reset_index()
df['pubchem_id'] = df.stitch_id_flat.map(stitch_to_pubchem)
d2 = pd.read_excel("../data/2d_prop.xlsx")
d3 = pd.read_excel("../data/3d_prop.xlsx")
d2 = d2.select_dtypes(include=['int64','float64'])
d3 = d3.select_dtypes(include=['float64'])
df = pd.concat([df, d2, d3], axis=1)
df.drop("stitch_id_flat", inplace=True, axis=1)
df3=pd.read_csv('system.csv')
df3 = df3[['DIGESTIVE SYSTEM']]
df3.head(144)
df3 = df3['DIGESTIVE SYSTEM'].tolist()
j=0
df['bool'] = ''
for i in df['side_effect_name']:
    c=any(item in i for item in df3)
    df['bool'][j]=c
    j+=1
df2 = df.loc[df['bool'] == bool(True)]
df2 = df2.reset_index()
df2.drop("index", inplace=True, axis=1)
df2.drop("bool", inplace=True, axis=1)
df1 = df2
k=0
df1['side_effect'] = ''
for i in df1['side_effect_name']:
    new = []
    j = 0
    length = len(i)
    #print(length)
    while j < length:
        if i[j] in df3:
            c = i[j]
            new.append(c)
            unique = set(new)
            new_1 = list(unique)
        j = j+1
    df1['side_effect'][k] =new_1   
    k = k+1    
df1.drop("side_effect_name", inplace=True, axis=1)
df = df1
X = df.drop("side_effect", axis=1)
Y = df[df.columns[-1]]
X.fillna(X.mean(), inplace=True)
mlb = MultiLabelBinarizer()
y=mlb.fit_transform(Y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)


clf=OneVsRestClassifier(LogisticRegression(C=20, penalty='l2'))
clf.fit(X_train, y_train)

score=fbeta_score(y_test, clf.predict(X_test), beta=2, average=None)

avg_sample_score=fbeta_score(y_test, clf.predict(X_test), beta=2, average='samples')

avg_prec=average_precision_score(y_test.T, clf.predict(X_test).T)

metrics = [score, avg_sample_score, roc_auc_score(y_test.T, clf.predict_proba(X_test).T)]

app = dict()

app['Classwise Scores'] = ([(mlb.classes_[l], score[l]) for l in score.argsort()[::-1]])
app['F2 Score'] = avg_sample_score
app['ROC_AUC'] = roc_auc_score(y_test.T, clf.predict_proba(X_test).T)
app['Precision Score Avg (PR Curve)'] = avg_prec

# pre=clf.predict(X_test.loc[1192].to_frame().T)
# a = mlb.inverse_transform(pre)
# a

# df1.iloc[1192]['side_effect']  



clf1=OneVsRestClassifier(RandomForestClassifier(n_estimators=200, max_depth=6, random_state=42, min_samples_split=10))
clf1.fit(X_train, y_train)

score=fbeta_score(y_test, clf1.predict(X_test), beta=2, average=None)

avg_sample_score=fbeta_score(y_test, clf1.predict(X_test), beta=2, average='samples')


avg_prec=average_precision_score(y_test.T, clf1.predict(X_test).T)


metrics = [score, avg_sample_score, roc_auc_score(y_test.T, clf1.predict_proba(X_test).T)]

app = dict()

app['Classwise Scores'] = ([(mlb.classes_[l], score[l]) for l in score.argsort()[::-1]])
app['F2 Score'] = avg_sample_score
app['ROC_AUC'] = roc_auc_score(y_test.T, clf1.predict_proba(X_test).T)
app['Precision Score Avg (PR Curve)'] = avg_prec


# pre=clf1.predict(X_test.loc[1295].to_frame().T)
# a = mlb.inverse_transform(pre)
# a

# df1.iloc[55]['side_effect'] 


clf2=OneVsRestClassifier(SVC(probability=True, kernel='rbf'))
clf2.fit(X_train, y_train)

score=fbeta_score(y_test, clf2.predict(X_test), beta=2, average=None)

avg_sample_score=fbeta_score(y_test, clf2.predict(X_test), beta=2, average='samples')

avg_prec=average_precision_score(y_test.T, clf2.predict(X_test).T)


metrics = [score, avg_sample_score, roc_auc_score(y_test.T, clf2.predict_proba(X_test).T)]

app = dict()

app['Classwise Scores'] = ([(mlb.classes_[l], score[l]) for l in score.argsort()[::-1]])
app['F2 Score'] = avg_sample_score
app['ROC_AUC'] = roc_auc_score(y_test.T, clf2.predict_proba(X_test).T)
app['Precision Score Avg (PR Curve)'] = avg_prec


clf3=OneVsRestClassifier(GaussianNB())
clf3.fit(X_train, y_train)

score=fbeta_score(y_test, clf3.predict(X_test), beta=2, average=None)

avg_sample_score=fbeta_score(y_test, clf3.predict(X_test), beta=2, average='samples')


avg_prec=average_precision_score(y_test.T, clf3.predict(X_test).T)

metrics = [score, avg_sample_score, roc_auc_score(y_test.T, clf3.predict_proba(X_test).T)]

app = dict()

app['Classwise Scores'] = ([(mlb.classes_[l], score[l]) for l in score.argsort()[::-1]])
app['F2 Score'] = avg_sample_score
app['ROC_AUC'] = roc_auc_score(y_test.T, clf3.predict_proba(X_test).T)
app['Precision Score Avg (PR Curve)'] = avg_prec

# app

# pre=clf3.predict(X_test.loc[435].to_frame().T)
# a = mlb.inverse_transform(pre)
# a


# # In[83]:


# df1.iloc[626]['side_effect']

clf4=OneVsRestClassifier(KNeighborsClassifier(n_neighbors=10))
clf4.fit(X_train, y_train)

score=fbeta_score(y_test, clf4.predict(X_test), beta=2, average=None)

avg_sample_score=fbeta_score(y_test, clf4.predict(X_test), beta=2, average='samples')

avg_prec=average_precision_score(y_test.T, clf4.predict(X_test).T)

metrics = [score, avg_sample_score, roc_auc_score(y_test.T, clf4.predict_proba(X_test).T)]

app = dict()

app['Classwise Scores'] = ([(mlb.classes_[l], score[l]) for l in score.argsort()[::-1]])
app['F2 Score'] = avg_sample_score
app['ROC_AUC'] = roc_auc_score(y_test.T, clf4.predict_proba(X_test).T)
app['Precision Score Avg (PR Curve)'] = avg_prec

# app

# pre=clf4.predict(X_test.loc[1295].to_frame().T)
# a = mlb.inverse_transform(pre)
# a

# df1.iloc[1295]['side_effect']



results=[0.9132882785198946,0.933242482493899,0.9338025084160225,0.5621761822541855,0.8762347875196086]
names=["Logistic Regression","Random Forest","SVC","Gaussian NB","KNN"]

data = {'AUC-ROC': results, 'Model Name': names}
dataset=pd.DataFrame(data)
# dataset

import seaborn as sns
sns.set(style="whitegrid")
#tips = sns.load_dataset("tips")
sns.set(rc={'figure.figsize':(11.7,8.27)})
ax = sns.barplot( x="Model Name",y="AUC-ROC", data=dataset)


# ## Final Verdict - Random Forest


def label_map(out):
    pre=clf1.predict(out)
    a = mlb.inverse_transform(pre)
    return a


# df1.iloc[1295]['side_effect']

print("For the Pubchem ID: ",df1['pubchem_id'][1295],", the possible side effects affecting the DIGESTIVE System are \nPredicted:\n",label_map(X_test.loc[1295].to_frame().T),"\nActual:\n",df1['side_effect'][1295])


print("For the Pubchem ID: ",df1['pubchem_id'][406],", the possible side effects affecting the DIGESTIVE System are \nPredicted:\n",label_map(X_test.loc[406].to_frame().T),"\nActual:\n",df1['side_effect'][406])

print("For the Pubchem ID: ",df1['pubchem_id'][55],", the possible side effects affecting the DIGESTIVE System are \nPredicted:\n",label_map(X_test.loc[55].to_frame().T),"\nActual:\n",df1['side_effect'][55])



