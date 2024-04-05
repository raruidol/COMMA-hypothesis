from sentence_transformers import SentenceTransformer
from datasets import Dataset, DatasetDict
import json
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix


def load_dataset(path):
    data = {'train': {}, 'dev': {}, 'test': {}}

    data['train']['label'] = []
    data['train']['text'] = []
    data['dev']['label'] = []
    data['dev']['text'] = []
    data['test']['label'] = []
    data['test']['text'] = []

    try:
        with open(path) as filehandle:
            json_data = json.load(filehandle)
    except:
        print('The file is not available.')
        exit()

    print('File loaded.')

    for sample in json_data['train']:
        data['train']['text'].append(sample[0])
        data['train']['label'].append(sample[1])

    for sample in json_data['dev']:
        data['dev']['text'].append(sample[0])
        data['dev']['label'].append(sample[1])

    for sample in json_data['test']:
        data['test']['text'].append(sample[0])
        data['test']['label'].append(sample[1])

    final_data = DatasetDict()
    for k, v in data.items():
        final_data[k] = Dataset.from_dict(v)

    return final_data


def vectorize_data(data, embedding):
    print('Generating embeddings...')

    tr_lb = data['train']['label']
    de_lb = data['dev']['label']
    te_lb = data['test']['label']

    tr = embedding.encode(data['train']['text'])
    de = embedding.encode(data['dev']['text'])
    te = embedding.encode(data['test']['text'])

    print('Embeddings finished.')
    return np.array(tr), np.array(de),  np.array(te), np.array(tr_lb), np.array(de_lb), np.array(te_lb)


def make_predictions(model, inputs):
    preds = model.predict(inputs)
    return preds


if __name__ == "__main__":

    data_path = 'data_split/locution_hypothesis.json'

    # LOAD DATA FOR THE MODEL
    dataset = load_dataset(data_path)
    shuffled_dataset = dataset.shuffle(seed=42)

    embedding_model = SentenceTransformer('sentence-transformers/all-roberta-large-v1')

    tr_x, de_x, te_x, tr_y, de_y, te_y = vectorize_data(shuffled_dataset, embedding_model)

    svc = make_pipeline(StandardScaler(), SVC(gamma='auto', C=100))
    svc.fit(tr_x, tr_y)

    de_preds = make_predictions(svc, de_x)
    te_preds = make_predictions(svc, te_x)

    mf1_dev = precision_recall_fscore_support(de_y, de_preds, average='macro')
    mf1_test = precision_recall_fscore_support(te_y, te_preds, average='macro')

    print('Macro F1 score in DEV:', mf1_dev)
    print('Confusion matrix:')
    print(confusion_matrix(de_y, de_preds))

    print('Macro F1 score in TEST:', mf1_test)
    print('Confusion matrix:')
    print(confusion_matrix(te_y, te_preds))