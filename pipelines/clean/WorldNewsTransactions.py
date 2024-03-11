import pandas as pd

wdm = pd.read_csv('data/wdms/count/worldnewsapi/lemmed/title.csv',index_col=0)

basket_df = pd.DataFrame(columns=['transactions'])
for i in range(len(wdm)):
    terms=wdm.iloc[i,4:].astype(int)
    # For each row, filter that row by x>0, i.e. there is at least one instance of that term in the document.
    filter=terms.apply(lambda x:x>0)
    terms=terms[filter]
    # Then turn the index of the resulting series into a comma separated list to get the basket of terms.
    basket = ' '.join(list(terms.index))
    basket_df.loc[len(basket_df.index)]=basket

basket_df.to_csv('data/transaction/worldnews_title.csv')