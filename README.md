LexComp - Single Document Summarization Using LexRank and Sentence Compression

ABSTRACT
Single document summarization is the task of summarizing a given document without using any other sources and purely based on the context provided in the document. It has applications in document search, fake article detection and it is a widely researched natural language processing topic. In this paper, we present LexComp a hybrid of both extractive and abstractive summarization techniques. LexComp first applies Lexical Ranking on the document and picks top 5 sentences from the document. Then it compresses these sentences and generates the summary. Our model beats the simple Lexical Ranking algorithm in both Rouge-1 and Bleu scores. It achieves a Rouge-1 score of 0.3270.