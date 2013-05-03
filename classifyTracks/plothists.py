import pylab as pl
import pickle

from getfeatures import how_many, many_features, feature_names

f_in = open('labels_panel.pk','r')
labels_panel = pickle.load(f_in)
f_in.close()

f_in = open('features_panel.pk','r')
features_panel = pickle.load(f_in)
f_in.close()

# make feat_array and label_arrays so that the following loop can
# use vstack and hstack
# we need the arrays to make histograms and such
feat_array = pl.vstack([features_panel[0].dropna(axis=0)[:], \
                        features_panel[1].dropna(axis=0)[:]])
label_array = pl.hstack([labels_panel[0].dropna(axis=0)['labels'],\
                         labels_panel[1].dropna(axis=0)['labels']])

for i in range(2,howMany):
    feat_array = pl.vstack([feat_array, \
                            features_panel[i].dropna(axis=0)[:]])
    label_array = pl.hstack([label_array, \
                             labels_panel[i].dropna(axis=0)['labels']])
label_array = pl.transpose(label_array)

pl.figure()
for i in range(many_features):
    a = label_array
    b = feat_array
    pl.hold()
    if (i==2):
        counts0, bins0 = pl.histogram(b[a==0,i],100,range=(0.,0.08))
        counts1, bins1 = pl.histogram(b[a==1,i],100,range=(0.,0.08))
    elif (i==5):
        counts0, bins0 = pl.histogram(b[a==0,i],100,range=(1,5))
        counts1, bins1 = pl.histogram(b[a==1,i],100,range=(1,5))
    elif (i==6):
        counts0, bins0 = pl.histogram(b[a==0,i],100,range=(0,15))
        counts1, bins1 = pl.histogram(b[a==1,i],100,range=(0,15))
    else:
        counts0, bins0 = pl.histogram(b[a==0,i],100)
        counts1, bins1 = pl.histogram(b[a==1,i],100)
    pl.subplot(2,4,i+1)
    pl.plot(bins0[0:100],counts0,'r',bins1[0:100],counts1,'b')
    pl.title(feature_names[i])
pl.show()
