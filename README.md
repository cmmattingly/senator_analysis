# Senator Analysis

The senator_analysis.py script is used to perform analysis on the scraped documents pulled from das-lab.org. The script uses the LdaMallet gensim wrapper for topic modeling.

# Description

First the script pulls the data from das-lab.org and performs preprocessing of the data. Removing stopwords, white spaces, numbers, and punctuation.

The script then tokenizes the words creating the texts, creates an id2word dictionary for the lda model, and then converts the id2words into a bag-of-words format for the model.

We then compute the coherence values for the models with different number of topics within a range. Uses the highest coherence value model that has a reasonable number of topics.

The script then posts the topics from the new LDA model to the database, and pulls the new topic_ids that have been created for the pushed topics. Then creates the doc_top matrix with the new model's topics.

Next we obtain the excerpts (the sentences with the highest total probability of the topics' words probabilities) for each topic within each document.

This allow us to now create a json payload of the doc_top matrix and excerpts by using the topic_ids obtained earlier.

This json payload is then posted to the das-lab.org doctopics endpoint. Where it is parsed and inserted into the database.

# Usage

Running the script does everything for you.

'''
python3 sen_analysis.py
'''

# Notebook

The notebook is used to edit/run portions of the code, so certain portions of the code aren't run everytime.

ex. pushing the new topics everytime
