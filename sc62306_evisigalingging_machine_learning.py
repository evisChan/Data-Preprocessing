# -*- coding: utf-8 -*-
"""SC62306_EviSigalingging_Machine Learning.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zFE-cFsA4FDXckUqco7ZX71LH2ZF8n1I

# **Importing the Libraries**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
plt.style.use('seaborn-whitegrid')

"""#Data Preparation

## **Importing the Dataset**
"""

from google.colab import  drive
drive.mount('/content/drive')

df = pd.read_csv('/content/drive/MyDrive/Stupend-sc/heart.csv')
df.head()

"""### Understanding data"""

correlation_matrix = df.corr()
# Menampilkan matriks korelasi sebagai heatmap
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12,10))
#sns.heatmap(df.corr(), annot=True)
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidth=.5)
plt.title('Heatmap korelasi antara fitur dalam dataset heart')
plt.show()

"""## **Check Missing Values**"""

df.isnull().sum()

"""## **Handling Duplicate Values**"""

df_dup = df.duplicated().any()
df_dup

df= df.drop_duplicates()

df_dup = df.duplicated().any()
df_dup

"""## **Data Processing**"""

category_val =[]
cont_val = []
for column in df.columns:
  if df[column].nunique() <=10:
    category_val.append(column)
  else:
    cont_val.append(column)

category_val

cont_val

"""### Imbalance Data"""

from imblearn.over_sampling import SMOTE
from sklearn.datasets import make_classification
# visualisasi ketidakseimbangan data pada kolom 'target'
fig = plt.figure(figsize=(5,5))
sns.countplot(x=df['target'], color='skyblue')
fig.show()

class_counts = df['target'].value_counts()
print(class_counts)

from imblearn.over_sampling import SMOTE

# Inisialisasi SMOTE
smote = SMOTE(sampling_strategy='auto')

# Melakukan oversampling
X_resampled, y_resampled = smote.fit_resample(X, y)

# Membuat histogram untuk variabel target yang telah diresampling
plt.figure(figsize=(9, 6))
sns.histplot(data=y_resampled, color='skyblue')
plt.show()

"""### Outlier"""

# Menampilkan Outlier menggunakan Boxplot
plt.rcParams['figure.figsize'] = [10,8]
sns.boxplot(data=df[['age', 'trestbps', 'chol', 'thalach', 'oldpeak','ca']])
plt.title('Boxplot of selected Columns')
plt.show()

def outliers(df, column):
  Q1 = df[column].quantile(0.25)
  Q3 = df[column].quantile(0.75)
  IQR = Q3 - Q1

  lower_bound = Q1 - 1.5 * IQR
  upper_bound = Q3 + 1.5 * IQR

  new_data = df.index[(df[column] < lower_bound) | (df[column] > upper_bound)]
  return new_data

column_outliers = []
for col in ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'ca']:
    column_outliers.extend(outliers(df, col))

df.drop(column_outliers, axis=0, inplace=True)

plt.rcParams['figure.figsize'] = [7,5]
sns.boxplot(data=df[['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'ca']])
plt.show()

"""saya tidak membuat future encoding karena semua data sudah numeric

# EDA

**Kolaborasi features & tipe data (nominal, ordinal, numerical)**
"""

df_info = pd.DataFrame(df.dtypes, columns=['Data Type'])

# tipe data numerik dan kategori
df_info['Feature Type']=''
df_info.loc[df_info['Data Type'] == 'object', 'Feature Type'] = 'Categorical'
df_info.loc[df_info['Data Type'] == 'object', 'Feature Type'] = 'Numerical'
# menampilkan fitur
print("Informasi Features dan Type Data: ")
print(df_info)

"""**Perbedaan Mean, Median, Modus**

*  Mean, adalah nilai rata-rata dari semua data dalam suatu sampel atau populasi. mean sering digunakan untuk mengisi missing values dalam sebuah dataset dengan variabel numerical

*  Median, adalah nilai tengah dari dataset yang telah diurutkan. Median sering digunakan untuk mengisi missing values jika distribusi data memiliki skewness atau terdapat outliers yang signifikan.

*  Modus, adalah nilai yang paling sering muncul dalam dataset. Modus digunakan untuk mengisi missing values dalam variabel kategorikal.

Perbedaannya Mean mengisi missing values dengan membagi dengan jumlah total nilai, median dengan mengambil nilai tengah dan berlaku untuk varibael numerical sedangkan Modus dengan nilai yang sering muncul dan hanya untuk variabel kategorikal dan tidak optimal untuk data Numeric

"""

age_mean = df['age'].mean()
age_modus = df['age'].mode().values[0]
age_median = df['age'].median()

print("Mean Usia", age_mean)
print("Modus Usia", age_modus)
print("Median Usia", age_median)

"""**Statistical five summary**"""

df.describe()

min_value = df.min()
min_value

max_value = df.max()
max_value

quarts = np.percentile(df, [25,50,75])
q1 = quarts[0]
q1

q2 = quarts[1]
q2

q3 = quarts[2]
q3

print("q1 : ", q1)
print("q2 : ", q2)
print("q3: ", q3)

"""**Deskripsi Distribusi Data**"""

# Menampilkan data dalam histogram
df.hist(figsize=(15,10), color='skyblue')

# Membuat Histogram untuk data Kolom Numerik
plt.figure(figsize=(16,10))
df[['age', 'trestbps', 'chol', 'thalach', 'oldpeak']].hist(color='skyblue')
plt.show()

# distribusi data Numerik
df[['age', 'trestbps', 'chol', 'thalach', 'oldpeak']].hist(color='skyblue', figsize=(16, 10))
print(df[['age', 'trestbps', 'chol', 'thalach', 'oldpeak']].skew())

"""Insight : Pada histrogram di atas dapat dikategorikan menjadi right skewed dan left skewed pada kolom numerik berikut penjelasannya.

 Distribusi Miring Kanan(Right Skewed): Modus < Median <Rata-rata. Pada Histogram  Data trestbps, oldpeak, chol

Distribusi Miring kiri(Left Skewed) : Rata-rata < Median pada histogram terdapat pada data age dan thalach

Pada Histogram di atas kolom kategori dapat ditentukan modus(nilai yang sering muncul) diantaranya:
- Data sex nilai modus 1 (laki-laki) yang lebih banyak mengalami sakit jantung
- cp dengan nilai modus 0 yaitu jenis nyeri dada yang dialami pasien adalah nyeri dada tipikal angina
- fbs dengan nilai modus 0 yang berarti pasien paling banyak memiliki fasting blood sugar yang tidak melebihi 120 mg/dL.
- restecg memiliki nilai modus 1 yaitu resting electrocardiographic result paling banyak terdapat kelainan gelombang S-T yang tidak normal.
- exang dengan nilai modus 0 yaitu pasien paling banyak tidak mengalami angina yang diinduksi oleh latih.
- slope dengan nilai modus 1 yaitu pasien paling banyak memiliki kemiringan segmen ST naik secara perlahan pada saat latihan puncak.
- ca dengan nilai modus 0 yaitu pasien memiliki kemungkinan yang kecil untuk terjadi penyempitan atau kerusakan pada pembuluh darah.
- thal dengan nilai modus 2 yaitu pasien paling banyak memiliki hasil tes thallium scan fixed defect
-target dengan nilai modus 1 yaitu pasien paling banyak memiliki riwayat risiko terkena penyakit jantung berdasarkan pertimbangan-pertimbangan di atas.

# **Feature Scalling**
"""

df.head()

from sklearn.preprocessing import StandardScaler
st = StandardScaler()
df[cont_val] = st.fit_transform(df[cont_val])

df.head()

"""# **QUESTIONS**

## 1,2

Pada Dataset heart disease sudah dilakukan cleaning data dan dataset ini adalah supervised learning

Penggunaan Machine Learning model yang sudah saya buat ada sebanyak 6 yaitu ada regression dan classification:
*   Logistic Regression
*   SVM
*   KNeighbors Classifier
*   Decision Tree Classifier
*   Random Forest Classifier
*   Gradient Boosting Classifier

Disini saya mencoba semua dan hasil Random Forest Classifier lebih akurat yakni 83%. Model Random Forest Classifier mampu mengatasi masalah klasifikasi dengan data yang memiliki banyak fitur atau variabel input (datanya kompleks).


Random Forest Classifier (RFC) mampu mengatasi kekurangan variabel, mengatasi Overfitting dengan ensemble learning yang menggunakan banyak pohon keputusan (decision trees) untuk membuat prediksi. RFC juga dapat menangani tipe data yang beragam, termasuk data kategorikal dan numerikal. Dan diantara semua model yang sudah saya coba RFC hasilnya lebih akurat

## 3
"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

X, y = df.drop(columns=['target']), df['target']
X_train, X_test, y_train, y_test= train_test_split(X, y, test_size=0.33, random_state=0)

df= df.drop_duplicates()

from sklearn.model_selection import train_test_split

X, y = df.drop(columns=['target']), df['target']

X_train, X_test, y_train, y_test=train_test_split(X,y,test_size=0.2, random_state=42)

print(y_test)

"""###**Logistic Regression**"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test=train_test_split(X,y,test_size=0.2, random_state=42)



# Melatih Model
log = LogisticRegression()
log.fit(X_train, y_train)

# Membuat prediksi pada data uji
y_pred1 = log.predict(X_test)

# Menghitung akurasi
acc1=accuracy_score(y_test, y_pred1)

print("Akurasi Logistic Regression: {:.2f}%".format(acc1 * 100))

"""###**Support Vector Machine**"""

from sklearn import svm
from sklearn.metrics import accuracy_score

svm = svm.SVC(C=1.0) # C=1.0 default value utk meisahkan data latih dengan benar

# Melatih model
svm.fit(X_train, y_train)

# Membuat prediksi
y_pred2 = svm.predict(X_test)

# menghitung akurasi
acc2=accuracy_score(y_test, y_pred2)
print("Akurasi SVC: {:.2f}%".format(acc2 * 100))

"""###**KNeighbors Classifier**"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
knn = KNeighborsClassifier()

# Melatih Model
knn.fit(X_train, y_train)

# Membuat prediksi pada data uji
y_pred3 = knn.predict(X_test)

#accuracy_score(y_test, y_pred3)
acc3 = accuracy_score(y_test, y_pred3)
print("Akurasi KNeighrbors Classifier: {:.2f}%".format(acc3 * 100))

# cek nilai lain
score =[]

for k in range(1,40):
  knn=KNeighborsClassifier(n_neighbors=k)
  knn.fit(X_train, y_train)
  y_pred = knn.predict(X_test)
  score.append(accuracy_score(y_test, y_pred))

score

knn=KNeighborsClassifier(n_neighbors=2)
  knn.fit(X_train, y_train)
  y_pred = knn.predict(X_test)
  accuracy_score(y_test, y_pred)

"""### **Decision Tree Classifier**"""

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
dtc = DecisionTreeClassifier(criterion='gini', random_state=42)

# Melatih Model
dtc.fit(X_train,y_train)

# Membuat prediksi pada data uji
y_pred4=dtc.predict(X_test)

# Menghitung akurasi Model
acc4 = accuracy_score(y_test, y_pred4)

print("Akurasi Decision Tree Classifier: {:.2f}%".format(acc4*100))

"""### **Random Forest Classifier**"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
rf = RandomForestClassifier(criterion='gini', random_state=42)

# Melatih Model
rf.fit(X_train,y_train)

# Membuat prediksi pada data uji
y_pred5=rf.predict(X_test)

# Menghitung akurasi Model
acc5 = accuracy_score(y_test, y_pred5)

print("Akurasi Random Forest Classifier: {:.2f}%".format(acc5 * 100))

"""### **Gradient Boosting Classifier**"""

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
gbc = GradientBoostingClassifier(random_state=42)

# Melatih Model
gbc.fit(X_train,y_train)

# membuat orediksi pada data uji
y_pred6 = gbc.predict(X_test)

# Menghitung akurasi model
acc6 =accuracy_score(y_test,y_pred6)
print("Akurasi Gradient Boosting Classifier: {:.2f}%".format(acc6 * 100))

final_df = pd.DataFrame({'Models' :['Logistic Regression', 'Support Vector Machine', 'KNeighbours Classifier', 'Decision Tree Classifier', 'Random Forest Classifier', 'Gradient Boosting Classifier'],
                         'ACC':[accuracy_score(y_test, y_pred1),
                                accuracy_score(y_test, y_pred2),
                                accuracy_score(y_test, y_pred3),
                                accuracy_score(y_test, y_pred4),
                                accuracy_score(y_test, y_pred5),
                                accuracy_score(y_test, y_pred6)]})

final_df # rf model yg terbaik

import seaborn as sns
sns.barplot(x=final_df['Models'], y=final_df['ACC'], palette='rainbow')
plt.xticks(rotation=45, ha='right')

"""##**4 Cross Validation**"""

#df= df.drop_duplicates()

df.head()

"""Implementasi Cross Validation pada model"""

from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.tree import DecisionTreeClassifier

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Membagi data latih
X,y = df.drop(columns=['target']), df['target']

clf = DecisionTreeClassifier(random_state=42)

cv_score = cross_val_score(clf, X,y, cv=10)
print("Cross Validation score")
print(cv_score)

# predict using cross validation
y_pred = cross_val_predict(clf, X,y, cv=3)
print("\n")
print("Cross Validation score: ", cv_score.mean())

"""**Menampilkan Learning Curve dengan cross validation**"""

# import nescessary libraries
from sklearn.model_selection import LearningCurveDisplay, learning_curve, train_test_split
from sklearn.model_selection import cross_val_score, cross_val_predict
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier

# X, y harus ditandai dari dataset
X, y = df.drop(columns=['target']), df['target']

train_sizes = np.linspace(0.1, 1, 50)
tree = DecisionTreeClassifier(random_state=42)
train_sizes, train_scores, test_scores, = learning_curve(tree, X, y, cv=25)

display =LearningCurveDisplay(train_sizes=train_sizes,
                              train_scores=train_scores,
                              test_scores=test_scores,
                              score_name="Score")
display.plot()
plt.show()

"""## 5 Penjelasan Cross Validation

Dengan membagi data menjadi data latih dan data uji menggunakan fungsi train_test_split. Dengan menggunakan fungsi cross_validation_score debfab parameter cv=10 (10 fold cross validation) yang akan mencetak score dari setiap iterasi cross-validation. **Pada Ouput yang dihasilkan mencetak rata-rata skor Cross-Validation adalah 0.7947** hal ini memberikan prediksi data model Decision Tree Classifier dan mampu menghasilkan data dengan **akurasi sekitar 79.47%**. Dan Score dari Cross-validation pada setiap iterasi yaitu: 0.8387, 0.7419, .., dst, membantu untuk memahami konsisten kinerja model dalam mengklasifikasikan data pada K-Fold yang berbeda

##**6 Learning Curve**
"""

# import nescessary libraries
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# X, y harus ditandai dari dataset
X, y = df.drop(columns=['target']), df['target']

#split the data into a training set and set testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# used to devide
train_sizes = np.linspace(0.1, 1, 50)
learning_curve_train = []
learning_curve_test =[]

rfc = RandomForestClassifier(n_estimators=100, random_state=42)

for train_size in train_sizes:
  num_samples = int(train_size * len(X_train))
  X_subset = X_train[:num_samples]
  y_subset = y_train[:num_samples]

  rfc.fit(X_subset, y_subset)

  y_pred_train = rfc.predict(X_subset)
  acc_train = accuracy_score(y_subset, y_pred_train)
  learning_curve_train.append(acc_train)

  y_pred_test = rfc.predict(X_test)
  acc_test = accuracy_score(y_test, y_pred_test)
  learning_curve_test.append(acc_test)

# plot learning curves
plt.figure(figsize=(10,6))
plt.title('Learning Curves')
plt.xlabel('Training set size')
plt.ylabel('Accuracy')
plt.grid()
plt.plot(train_sizes, learning_curve_train, 'o-', color="r", label="Training score")
plt.plot(train_sizes, learning_curve_test, 'o-', color="g", label="Testing score")
plt.legend(loc="best")
plt.show()

"""##7  Penjelasan Learning Curve

Learning Curve pada Training score terindikasi model memiliki kapasitas yang lumayan banyak yaitu pada titik 1.00. Parameter dialokasikan sebagai data uji 0.2 (20% dari data), parameter random_state=42 untuk menentukan seed untuk pembagian data sehingga dapat di reproduksi. Model Random Forest Classifier menggunakan subset data latih yang telah dipilih


Pada Model di atas mengalami Overfitting hal ini terlihat pada kinerja model Data Train berada pada sumbu Y di titik 1.00, namun hasil Testingnya mengalami Overfit, hal ini biasanya terjadi jika
*   jarak nilai akurasi dan validasi yang cukup tinggi
*   Akurasi training yang bertambah dan memiliki nilai yang sangat tinggi

##**8 Bootstrapping**
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# load the dataset
X, y = df.drop(columns=['target']), df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rfc = RandomForestClassifier(n_estimators=100, random_state=42)

# implement bootstrapping
n_bootstraps = 100
bootstrapped_scores = []

for _ in range(n_bootstraps):
  bootstrap_indices = np.random.choice(len(X_train), size=len(X_train), replace=True)
  X_bootstrap = X_train.iloc[bootstrap_indices]
  y_bootstrap = y_train.iloc[bootstrap_indices]

  rfc.fit(X_bootstrap, y_bootstrap)
  y_pred = rfc.predict(X_test)
  acc = accuracy_score(y_test, y_pred)
  bootstrapped_scores.append(acc)

# print the result
print("Bootstrap scores:", bootstrapped_scores)

print("Averange Bootstrap score: ", np.mean(bootstrapped_scores))

"""**Hyperparameter Tuning Random Forest Classifier**"""

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import LearningCurveDisplay, learning_curve
from sklearn.metrics import accuracy_score

X, y = df.drop(columns=['target']), df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# create a random forest classifier
rfc = RandomForestClassifier(random_state=43)
rfc.fit(X_train, y_train)
score = rfc.score(X_test, y_test)

rfc_max_depth = RandomForestClassifier(max_depth=2, random_state=0)
rfc_max_depth.fit(X_train, y_train)
score_max_depth = rfc_max_depth.score(X_test, y_test)

print("Score default:")
print(score)
print("Score max depth")
print(score_max_depth)

"""Pada Sampling Method saya membuat Hyperparameter dan Bootstrapping. Boostrapping digunakan untuk melakukan resampling data secara random berdasarkan sample yang sudah kita miliki dengan "replacement".
disini saya mengisialisasi Model dengan Random Forest Classifier dengan 100 tree (n_estimators=100) untuk dilakukan iterasi sebanyak n_bootstraps 100 kali. Pada setiap iterasi dilakukan pengambilan sampel dengan np.random.choice (memilih secara acak) kemudian skor accuracy dihitung menggunakan accuracy_score dan **disimpan dalam list bootstarpped_scores** dan menghasilkan rata-rata dari semua skor akurasi sebesar 81%

Pada Hyperparameter Tuning Random Forest Classifier terdapat konfigurasi defaul dan batas kedalaman maksimum (max_depth=2) yang dimana panjang dari percabagan random forest dan berhenti melakukan iterasi jika percabangan telah mencapai 2.
kemudian outputnya adalah **Score default 0.84% dan score max depth sebesar 0.82%**

##**9 Metric Evaluation**
"""

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=42, test_size=0.2)

model = LogisticRegression(max_iter=1000)

#training the LogisticRegression model with Training data
model.fit(X_train, y_train)

"""Model Evaluation"""

# Accuracy Score
from sklearn.metrics import accuracy_score

# accuracy on training data
X_train_prediction = model.predict(X_train)
training_data_acc = accuracy_score(X_train_prediction, y_train)

print("Accuracy on Training data: {:.2f}%".format(training_data_acc * 100))

# accuracy on test data
X_test_prediction = model.predict(X_test)
test_data_acc = accuracy_score(X_test_prediction, y_test)

print("Accuracy on Test data: {:.2f}%".format(test_data_acc * 100))

"""**Confusion Matrix**"""

from sklearn.metrics import confusion_matrix, classification_report

cf_matrix = confusion_matrix(X_test_prediction, y_test)
print(cf_matrix)

tn, fp, fn, tp = cf_matrix.ravel()

print(tn, fp, fn, tp)

import seaborn as sns
sns.heatmap(cf_matrix, annot=True, cmap='Blues')

report = classification_report(y_test, X_test_prediction)
print("Classification report:")
print(report)

"""##10  Penjelasan Metric Evaluation

**Model Evaluation** didefenisikan dengan memberikan inisialisasi model regresi logistik dengan memberikan parameter max_iter=100 yang dimana menentukan jumlah iterasi maksimum saat menyelesaikan optimisasi
*   Akurasi pada data latih digunakan untuk mempelajari pola pada data latih dan memprediksi label dengan mempertimbangkan pola yang ditemukan. Accuracynya sebesar 86.31% yang dimana model memiliki kinerja yang baik karena sudah mendekati hampir 100%

*   Akurasi pada data uji memiliki kinerja yang baik dalam memprediksi bahwa model mampu melakukan generalisasi dari pola yang telah dipelajari pada data latih ke data yang baru dan Accuracynya sebesar 80.33%

**Confusion Matrix**
confusion matrix adalah tabel yang digunakan untuk mengevaluasi kinerja model klasifikasi. Confusion matrix ini menggunakan matriks 2x2 yang berisi nilai-nilai True positive, True Negative, False Positive dan False Negative
kemudian didekomposisi dengan metode ravel() untuk mendapatkan tn, fp, fn, tp untuk menghitung matrik evaluasi presisi, recall, f1-score.
**Evalusasi Hasil** tn=23 fp=3 fn=9 tp=26. Dengan membuat classification report memberikan infromasi lebih detail tentang presisi, recall dan F1-score untuk setiap kelas serta akurasi keseluruhan dari model

alasan saya memilih model ini karena memberikan pemahaman yang mudah untuk melihat nilai-nilai True positive, True Negative, False Positive dan False Negative. dan kinerja model yang sudah akurat, dan interpretasi yang sederhana dan mampu mengatasi keterbatasan data
"""