from transformers import DataCollatorWithPadding, AutoModelForSequenceClassification
from transformers import AutoTokenizer, TrainingArguments, Trainer
from datasets import Dataset, DatasetDict
from sklearn.metrics import f1_score, confusion_matrix, precision_recall_fscore_support
import json, evaluate
import numpy as np


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


def tokenize_sequence(samples):
    return tknz(samples["text"], padding=True, truncation=True)


def load_model():
    tokenizer_hf = AutoTokenizer.from_pretrained('roberta-large')
    model = AutoModelForSequenceClassification.from_pretrained('roberta-large', num_labels=2,
                                                                   ignore_mismatched_sizes=True)

    return tokenizer_hf, model


def load_local_model(path):
    tokenizer_hf = AutoTokenizer.from_pretrained('')
    model = AutoModelForSequenceClassification.from_pretrained(path)

    return tokenizer_hf, model


def compute_metrics(eval_preds):
    metric = evaluate.load("f1")
    logits, labels = eval_preds
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels, average='macro')


def train_model(mdl, tknz, data):

    training_args = TrainingArguments(
        output_dir="models",
        evaluation_strategy="epoch",
        logging_strategy='epoch',
        save_strategy='epoch',
        save_total_limit=2,
        learning_rate=1e-5,
        weight_decay=0.01,
        per_device_train_batch_size=42,
        per_device_eval_batch_size=42,
        num_train_epochs=15,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        fp16=True
    )

    trainer = Trainer(
        model=mdl,
        args=training_args,
        train_dataset=data['train'],
        eval_dataset=data['dev'],
        tokenizer=tknz,
        data_collator=DataCollatorWithPadding(tokenizer=tknz),
        compute_metrics=compute_metrics
    )

    trainer.train()

    return trainer


if __name__ == "__main__":

    PRETRAIN = True
    CONTINUE = False

    data_path = 'data_split/argument_hypothesis.json'

    # LOAD DATA FOR THE MODEL
    dataset = load_dataset(data_path)

    shuffled_dataset = dataset.shuffle(seed=42)

    if CONTINUE:
        # LOAD PRE_TRAINED MODEL
        model_path = ''
        tknz, mdl = load_local_model(model_path)

        # TOKENIZE THE DATA
        tokenized_data = shuffled_dataset.map(tokenize_sequence, batched=True)

        # TRAIN THE MODEL
        trainer = train_model(mdl, tknz, tokenized_data)

        # GENERATE PREDICTIONS FOR DEV AND TEST
        dev_predictions = trainer.predict(tokenized_data['dev'])
        dev_predict = np.argmax(dev_predictions.predictions, axis=-1)
        test_predictions = trainer.predict(tokenized_data['test'])
        test_predict = np.argmax(test_predictions.predictions, axis=-1)

        mf1_dev = f1_score(tokenized_data['dev']['label'], dev_predict, average='macro')
        mf1_test = f1_score(tokenized_data['test']['label'], test_predict, average='macro')

        print('Macro F1 score in DEV:', mf1_dev, 'TEST:', mf1_test)

    elif PRETRAIN:

        # LOAD PRE_TRAINED LLM
        tknz, mdl = load_model()

        # TOKENIZE THE DATA
        tokenized_data = shuffled_dataset.map(tokenize_sequence, batched=True)

        # TRAIN THE MODEL
        trainer = train_model(mdl, tknz, tokenized_data)

        # GENERATE PREDICTIONS FOR DEV AND TEST
        dev_predictions = trainer.predict(tokenized_data['dev'])
        dev_predict = np.argmax(dev_predictions.predictions, axis=-1)
        test_predictions = trainer.predict(tokenized_data['test'])
        test_predict = np.argmax(test_predictions.predictions, axis=-1)

        mf1_dev = f1_score(tokenized_data['dev']['label'], dev_predict, average='macro')
        mf1_test = f1_score(tokenized_data['test']['label'], test_predict, average='macro')

        print('Macro F1 score in DEV:', mf1_dev, 'TEST:', mf1_test)
        print('Confusion matrix:')
        print(confusion_matrix(tokenized_data['test']['label'], test_predict))

    else:

        path_model = 'models/'

        tknz, mdl = load_local_model(path_model)

        tokenized_data = shuffled_dataset.map(tokenize_sequence, batched=True)

        trainer = Trainer(mdl)

        dev_predictions = trainer.predict(tokenized_data['dev'])
        dev_predict = np.argmax(dev_predictions.predictions, axis=-1)
        test_predictions = trainer.predict(tokenized_data['test'])
        test_predict = np.argmax(test_predictions.predictions, axis=-1)

        #print(dev_predict)

        #print(test_predict)

        mf1_dev = precision_recall_fscore_support(tokenized_data['dev']['label'], dev_predict, average='macro')
        mf1_test = precision_recall_fscore_support(tokenized_data['test']['label'], test_predict, average='macro')

        print('Score in, DEV:', mf1_dev, 'TEST:', mf1_test)
        print('Confusion matrix:')
        print(confusion_matrix(tokenized_data['test']['label'], test_predict))