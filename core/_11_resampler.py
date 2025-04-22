# >--Resampler.py--<

from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

def fit_resampler(strategy="smote", random_state=42, **kwargs):
    if strategy == "smote":
        resampler = SMOTE(random_state=random_state, **kwargs)
    elif strategy == "random_over":
        resampler = RandomOverSampler(random_state=random_state, **kwargs)
    elif strategy == "random_under":
        resampler = RandomUnderSampler(random_state=random_state, **kwargs)
    else:
        raise ValueError(f"Unsupported strategy: {strategy}")
    
    print(f"✅ Resampler initialized with strategy: {strategy}")
    return resampler

def apply_resampling(X, y, resampler):
    X_res, y_res = resampler.fit_resample(X, y)
    print(f"🔁 Resampling complete. Original: {len(y)}, Resampled: {len(y_res)}")
    return X_res, y_res

import matplotlib.pyplot as plt
import seaborn as sns

def visualize_class_distribution(y_before, y_after=None, labels=("Before", "After")):
    fig, axes = plt.subplots(1, 2 if y_after is not None else 1, figsize=(12, 5))

    if y_after is not None:
        ax1, ax2 = axes
        sns.countplot(x=y_before, ax=ax1)
        ax1.set_title(f"Class Distribution ({labels[0]})")
        sns.countplot(x=y_after, ax=ax2)
        ax2.set_title(f"Class Distribution ({labels[1]})")
    else:
        sns.countplot(x=y_before, ax=axes)
        axes.set_title("Class Distribution")

    plt.tight_layout()
    plt.show()

# Sample usage
from sklearn.model_selection import train_test_split

X = df.drop("target", axis=1)
y = df["target"]

visualize_class_distribution(y)

resampler = fit_resampler(strategy="smote")
X_resampled, y_resampled = apply_resampling(X, y, resampler)

visualize_class_distribution(y, y_resampled)


#  Extra Tips:
# Use SMOTE when you have enough 
# features to synthesize data.
# Prefer RandomOverSampler if the 
# dataset is small and you want faster results.
# Use RandomUnderSampler when the majority 
# class is very large and you're okay dropping some data

------------------------------------------------------------
