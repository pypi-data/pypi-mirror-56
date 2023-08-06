# USAGE

```
pip install genderClassifier
```

#### Download the model before proceeding for the first time

```python
# SWAMI KARUPPASWAMI THUNNAI

from gender_classifier import download
download.latest_model()
```


```python
# SWAMI KARUPPASWAMI THUNNAI

from gender_classifier.classifier import GenderClassifier

classifier = GenderClassifier()
print(classifier.classify_gender("example_image.jpg"))
```