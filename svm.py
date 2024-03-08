from sklearn import svm
from sklearn.svm import LinearSVC, SVC
import pickle
import numpy as np
from sklearn.decomposition import PCA, KernelPCA
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from sklearn.kernel_approximation import Nystroem
from sklearn.utils import resample
from sklearn.linear_model import LogisticRegression

scaler = StandardScaler()


with open("dmaothqtrack.pkl","rb") as f:
    train = pickle.load(f)
with open("dmaothqtrack_test.pkl","rb") as f:
    test = pickle.load(f)




X = np.array([x[2:4]+x[6:8] for x in train])

y = np.array([x[8] for x in train])


r = np.random.RandomState()

clf = svm.SVC(C=1, class_weight='balanced', kernel='rbf', verbose=True) 

print(len(X), len(y),sum(y))
clf.fit(X, y)

sample = np.array([x[2:4]+x[6:8] for x in test])


label = clf.predict(sample)

p = np.where(sum(sample.T) == 0)
label[p] = 1

with open('svm1dmaothqtrack.pkl','wb') as f:
    pickle.dump([h for h in label], f)

                                      
print(sum(label==1), len(test))