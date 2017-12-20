import matplotlib.pyplot as plt
from sklearn import metrics

def compute_metrics (classifier, X_test, y_test, classes):
    """
    This function computes and prints various performance measures for a classifier.
    """
    # Use the classifier to make predictions for the test set.
    y_pred = classifier.predict(X_test)
    
    # Choose the class with the highest estimated probability.
    y_pred = np.argmax(y_pred, axis=1)

    print('Classes:', classes, '\n')

    # Compute the confusion matrix.
    cm = metrics.confusion_matrix(y_test, y_pred, labels=classes)
    print('Confusion matrix, without normalization')
    print(cm, '\n')

    # Normalize the confusion matrix by row (i.e by the number of samples in each class).
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    np.set_printoptions(precision=3, linewidth=132)
    print('Normalized confusion matrix')
    print(cm_normalized, '\n')

    # The confusion matrix as percentages.
    cm_percentage = 100 * cm_normalized
    print('Confusion matrix as percentages')
    print(np.array2string(cm_percentage, formatter={'float_kind':lambda x: "%6.2f" % x}), '\n')
    
    # Precision, recall, and f-score.
    print(metrics.classification_report(y_test, y_pred, digits=3))

    return cm


#model_history is just the model fitted
def plot_model_history(model_history):
    fig, axs = plt.subplots(1,2,figsize=(15,5))
    # summarize history for accuracy
    axs[0].plot(range(1,len(model_history.history['acc'])+1),model_history.history['acc'])
    axs[0].plot(range(1,len(model_history.history['val_acc'])+1),model_history.history['val_acc'])
    axs[0].set_title('Model Accuracy')
    axs[0].set_ylabel('Accuracy')
    axs[0].set_xlabel('Epoch')
    axs[0].set_xticks(np.arange(1,len(model_history.history['acc'])+1),len(model_history.history['acc'])/10)
    axs[0].legend(['train', 'val'], loc='best')
    # summarize history for loss
    axs[1].plot(range(1,len(model_history.history['loss'])+1),model_history.history['loss'])
    axs[1].plot(range(1,len(model_history.history['val_loss'])+1),model_history.history['val_loss'])
    axs[1].set_title('Model Loss')
    axs[1].set_ylabel('Loss')
    axs[1].set_xlabel('Epoch')
    axs[1].set_xticks(np.arange(1,len(model_history.history['loss'])+1),len(model_history.history['loss'])/10)
    axs[1].legend(['train', 'val'], loc='best')
    plt.show()