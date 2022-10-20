from colbert import Indexer
from colbert.data import Queries
from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert import Searcher

if __name__ == "__main__":
    root = "data/official_colbert"
    index_name = "msmarco.nbits=2"
    checkpoint_path = "/data/local/li0123/soseki-dev/data/colbertv2.0"
    msmarco_path = "/data/local/li0123/soseki-dev/data/msmarco/raw_large"

    with Run().context(RunConfig(nranks=1, experiment="msmarco")):

        config = ColBERTConfig(
            nbits=2,
            root=root,
        )
        indexer = Indexer(checkpoint=checkpoint_path, config=config)
        indexer.index(name=index_name, collection=f"{msmarco_path}/collection.tsv")

    with Run().context(RunConfig(nranks=1, experiment="msmarco")):

        config = ColBERTConfig(
            root=root,
        )
        searcher = Searcher(index=index_name, config=config)
        queries = Queries(f"{msmarco_path}/queries.dev.small.tsv")
        ranking = searcher.search_all(queries, k=100)
        ranking.save("msmarco.nbits=2.ranking.tsv")
