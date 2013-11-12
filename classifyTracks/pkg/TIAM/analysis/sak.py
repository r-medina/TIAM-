# run basic decision trees
dtree = tree.DecisionTreeClassifier(criterion='entropy', min_samples_leaf=50, max_depth=3, compute_importances=True)
performance = cross_validation.cross_val_score(dtree, x, y, cv=kfold, n_jobs=-1)
print 'decision tree performance (mean, stdev) under 10-fold CV:'
print performance.mean(), performance.std()

dtree.fit(x, y)
print pd.DataFrame(dtree.feature_importances_,
                   columns=['Importance'],
                   index=X.columns).sort(['Importance'], ascending=False)
tree.export_graphviz(dtree, out_file='../out/{0}/dtree.dot'.format(WHICH_EXP), feature_names=X.columns)

#run gradient boosting ensemble
gbtree = ensemble.GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=5, random_state=0)
performance = cross_validation.cross_val_score(gbtree, x, y, cv=kfold, n_jobs=-1)
print 'gradient boosting ensemble performance (mean, stdev) under 10-fold CV:'
print performance.mean(), performance.std()

gbtree.fit(x,y)
feature_importance = gbtree.feature_importances_
feature_importance = 100.0 * (feature_importance / feature_importance.max())
sorted_idx = np.argsort(feature_importance)
pos = np.arange(sorted_idx.shape[0]) + .5

plt.figure(figsize=(12, 6))
plt.subplot(1, 1, 1)
plt.barh(pos, feature_importance[sorted_idx], align='center')
plt.yticks(pos, X.columns[sorted_idx])
plt.xlabel('Relative Importance')
plt.title('Variable Importance')
plt.show()
