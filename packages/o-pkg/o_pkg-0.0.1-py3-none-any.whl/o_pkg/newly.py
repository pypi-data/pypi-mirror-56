import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np
import seaborn as sns
from sklearn.datasets import load_breast_cancer
b_cancer = load_breast_cancer()
t_names = b_cancer.target_names
data1 = pd.DataFrame(b_cancer.data, columns= b_cancer.feature_names) 
#b_cancer['target'] = pd.Series(b_cancer.target)
data1['diagnosis'] = b_cancer.target
#print(b_cancer['target'].value_counts())
#sns.countplot(b_cancer['target'],label='Count')
#plt.show()

#print(data1.keys())
#for el in data1.keys():
#    plt.scatter(b_cancer['target'],data1[el])
#    plt.xlabel('diagnoses')
#    plt.ylabel(el)
#    plt.show()
data2 = data1[['mean radius','mean perimeter','mean area','mean concave points','perimeter error','area error',
              'worst radius','worst perimeter','worst area','worst concave points','diagnosis']]


sns.pairplot(data2, hue='diagnosis', diag_kind = 'hist')
plt.savefig('pairplot_target.png')
plt.show()

sns.heatmap(data2.corr(),annot=True,fmt='.0%')
plt.savefig('breastcancer heat map')
plt.show()

plt.scatter(data1['mean radius'],data1['mean area']/data1['mean area'].max(),label='mean area', marker='D')
plt.scatter(data1['mean radius'],data1['mean perimeter']/data1['mean perimeter'].max(),label='mean perimeter')
plt.scatter(data1['mean radius'],data1['perimeter error']/data1['perimeter error'].max(),label='perimeter error', marker='^',alpha=0.4)
plt.xlabel('mean radius')
plt.legend(loc='upper left', fontsize='small')
plt.savefig('similarities.png')
plt.show()

data3 = data1[['worst concave points', 'perimeter error','mean radius', 'diagnosis']]
sns.pairplot(data3, hue = 'diagnosis', diag_kind = 'hist', palette=sns.color_palette("cubehelix",2), markers=['D','o'])
plt.savefig('final_feature.png')
plt.show()
#plt.scatter(range(len(data1['perimeter error'])),data1['perimeter error']/data1['perimeter error'].max(), label='perimeter error')
#plt.scatter(range(len(data1['worst concave points'])),data1['worst concave points']/data1['worst concave points'].max(),label='worst concave points')
#plt.scatter(range(len(data1['mean radius'])),data1['mean radius']/data1['mean radius'].max(), label='mean radius')
#plt.show()