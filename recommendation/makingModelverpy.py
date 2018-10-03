import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from surprise import Reader, Dataset, SVD, evaluate
from konlpy.tag import Okt
import time

select_type = 4
original_data = pd.read_csv('./sunblock.csv')
type = {'건성': 0, '지성': 1, '중성': 2, '복합성': 3, '민감성': 4}
original_data['type'] = original_data['type'].map(type)

twitter = Okt()
totalWord = ''
print(1)
for index, data in enumerate(original_data['review']):
    words = twitter.pos(data, norm=True)
    for word in words:
        if word[1] not in ["Punctuation", "Eomi", "Josa"] and word[0] not in ["\ud83d", "\ud83e"]:
            totalWord += word[0] + ' '
    original_data.loc[index, 'review'] = totalWord
    totalWord = ''


print(2)
id_purify_data = original_data.copy()
member_per_type = {0: len(original_data.loc[original_data['type']==0,:]), 1: len(original_data.loc[original_data['type']==1,:]), 2: len(original_data.loc[original_data['type']==2,:]),
                   3: len(original_data.loc[original_data['type']==3,:]), 4: len(original_data.loc[original_data['type']==4,:])}
print(3)
for i in range(5):
    np.random.seed(42)
    id_purify_data.loc[id_purify_data["type"] == i, "userId"] = [np.random.randint(i * 200, 200 * (i + 1))
                                                                 for j in range(0, member_per_type[i])]

id_purify_data = id_purify_data.sort_values('userId')
print(4)
def reviewData(type):
    review_data = ['' for i in range(100)]
    review_type_popid_data = pd.DataFrame(id_purify_data[["popId", "type", "review"]])
    review_type_popid_data = review_type_popid_data.reset_index(drop=True)
    review_type_popid_data = review_type_popid_data.loc[review_type_popid_data["type"] == type, :]
    for index, row in review_type_popid_data.iterrows():
        review_data[row["popId"]] += row["review"]
    return review_data
print(5)
review_data = reviewData(select_type)
id_to_name = original_data[["popId", "name"]].drop_duplicates()
id_to_name = id_to_name.reset_index(drop=True)
id_to_name = id_to_name.drop(columns="popId", axis=1)
name_to_id = original_data[["popId", "name"]].drop_duplicates()
name_to_id = name_to_id.set_index("name", drop=True)
review_data = pd.Series(review_data)
tf = TfidfVectorizer(analyzer='word', min_df=2, stop_words=['\r', '\n'], sublinear_tf=True)
tf_matrix = tf.fit_transform(review_data)
cosine_sim = linear_kernel(tf_matrix, tf_matrix)
print(6)
def making_evaluate_data(type = 0):
    evaluate_data = id_purify_data[id_purify_data["type"]==type]
    evaluate_data = evaluate_data.drop(columns=['name', 'review', 'type'], axis=1)
    print(evaluate_data)
    reader = Reader()
    evaluate_data = Dataset.load_from_df(evaluate_data, reader)
    return evaluate_data
evaluate_data = making_evaluate_data(select_type)
evaluate_data.split(5)
svd = SVD()
evaluate(svd, evaluate_data, measures=['RMSE', 'MAE'])
from sklearn.externals import joblib
print(7)
trainset = evaluate_data.build_full_trainset()
svd.fit(trainset)
joblib.dump(svd, 'sunblock_4.pkl')