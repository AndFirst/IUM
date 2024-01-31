import config
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_curve, roc_auc_score, f1_score, confusion_matrix, classification_report, roc_curve, auc
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, Tuple, Union
from scipy.stats import ttest_ind


def split_data(X: Union[list, np.ndarray],
               y: Optional[Union[list, np.ndarray]] = None,
               test_size: float = 0.2,
               valid_size: float = 0.2,
               random_state: int = 42
               ) -> Tuple[Union[list, np.ndarray], Union[list, np.ndarray],
                          Union[list, np.ndarray], Optional[Union[list, np.ndarray]],
                          Optional[Union[list, np.ndarray]], Optional[Union[list, np.ndarray]]]:

    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state)

    X_train, X_valid, y_train, y_valid = train_test_split(X_temp, y_temp, test_size=valid_size/(1-test_size),
                                                          random_state=random_state)

    return X_train, X_valid, X_test, y_train, y_valid, y_test


def print_metrics_for_class(y_true_class: Union[list, pd.Series], y_pred_class: Union[list, pd.Series], class_name: str) -> None:
    accuracy = accuracy_score(y_true_class, y_pred_class)
    auc = roc_auc_score(y_true_class, y_pred_class)
    f1 = f1_score(y_true_class, y_pred_class)

    print(f"\nClass: {class_name}")
    print(f"Accuracy: {accuracy}")
    print(f"AUC: {auc}")
    print(f"F1-score: {f1}")

    class_report_class = classification_report(y_true_class, y_pred_class)
    print(f"Classification Report:\n{class_report_class}")


def plot_confusion_matrix(y_true_class: Union[list, pd.Series], y_pred_class: Union[list, pd.Series], class_name: str) -> None:
    conf_matrix_class = confusion_matrix(
        y_true_class, y_pred_class, labels=[1, 0])
    plt.figure(figsize=(5, 4))
    sns.heatmap(conf_matrix_class, annot=True, fmt="d", cmap="Blues", xticklabels=['Positive', 'Negative'],
                yticklabels=['Positive', 'Negative'])
    plt.xlabel('Predicted')
    plt.ylabel('Real')
    plt.title(f'Confusion Matrix of {class_name}')
    plt.show()


def print_classification_metrics(y_true: dict, y_pred: np.ndarray, class_names: list, name="") -> None:
    for i, class_name in enumerate(class_names):
        y_true_class = y_true[:, i]
        y_pred_class = y_pred[:, i]

        precision, recall, f1_scores, optimal_threshold, y_pred_optimal_threshold, thresholds = calculate_precision_recall_f1(
            y_true_class, y_pred_class)
        print('===============================================')
        print(name)
        print('===============================================')
        print('Optimal threshold:', optimal_threshold)
        print_metrics_for_class(
            y_true_class, y_pred_optimal_threshold, class_name)
        plot_precision_recall_curve(thresholds, precision, recall, class_name)
        plot_roc_curve(y_true_class, y_pred_class)
        plot_confusion_matrix(
            y_true_class, y_pred_optimal_threshold, class_name)
        print('===============================================')


def plot_precision_recall_curve(thresholds, precision, recall, class_name):
    """
    Plot the Precision-Recall curve for different thresholds.

    Parameters:
    - thresholds: Threshold values
    - precision: Precision values
    - recall: Recall values
    """
    plt.title(f'Precission - Recall curve for class: {class_name}')
    plt.plot(thresholds, precision[:-1], label='Precision')
    plt.plot(thresholds, recall[:-1], label='Recall')
    plt.xlabel('Threshold')
    plt.legend()
    plt.show()


def calculate_precision_recall_f1(y_true_class, y_pred_class):
    """
    Calculate precision, recall, F1-score, and optimal threshold for precision-recall curve.

    Parameters:
    - y_true_class: True labels for the class
    - y_pred_class: Predicted probabilities for the class

    Returns:
    - precision: Precision values
    - recall: Recall values
    - f1_scores: F1-score values
    - optimal_threshold: Optimal threshold for maximizing F1-score
    - y_pred_optimal_threshold: Predictions using the optimal threshold
    """
    precision, recall, thresholds = precision_recall_curve(
        y_true_class, y_pred_class)
    f1_scores = 2 * (precision * recall) / (precision + recall)
    optimal_threshold = thresholds[np.argmax(f1_scores)]
    y_pred_optimal_threshold = (y_pred_class > optimal_threshold).astype(int)

    return precision, recall, f1_scores, optimal_threshold, y_pred_optimal_threshold, thresholds


def plot_roc_curve(y_true, y_pred):
    """
    Plot the Receiver Operating Characteristic (ROC) curve.

    Parameters:
    - y_true: True labels
    - y_pred: Predicted probabilities
    """
    fpr, tpr, _ = roc_curve(y_true, y_pred)
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2,
             label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.show()


def t_student_test(group_a, group_b):
    # Przeprowadź test t-Studenta
    t_statistic, p_value = ttest_ind(
        group_a, group_b, equal_var=False)

    # Wyświetl wyniki testu
    print(f'T-statistic: {t_statistic}')
    print(f'P-value: {p_value}')

    # Sprawdź hipotezy na podstawie p-wartości
    alpha = 0.05  # Ustal poziom istotności
    if p_value < alpha:
        print("Odrzucamy hipotezę zerową. Istnieje istotna różnica między grupami.")
        if t_statistic > 0:
            print("Grupa A jest lepsza niż grupa B.")
        else:
            print("Grupa B jest lepsza niż grupa A.")
    else:
        print("Nie ma istotnej różnicy między grupami.")
