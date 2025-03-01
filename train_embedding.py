from argparse import ArgumentParser
from typing import cast, List
from omegaconf import OmegaConf, DictConfig
import json
import glob
import networkx as nx
from gensim.models import Word2Vec, KeyedVectors
from os import cpu_count
from tqdm import tqdm
from multiprocessing import cpu_count, Manager, Pool
import functools
import os

PAD = "<PAD>"
UNK = "<UNK>"
MASK = "<MASK>"
SPECIAL_TOKENS = [PAD, UNK, MASK]
USE_CPU = cpu_count()

def tokenize_code_line(line):
    # Sets for operators
    operators3 = {'<<=', '>>='}
    operators2 = {
        '->', '++', '--', '!~', '<<', '>>', '<=', '>=', '==', '!=', '&&', '||',
        '+=', '-=', '*=', '/=', '%=', '&=', '^=', '|='
    }
    operators1 = {
        '(', ')', '[', ']', '.', '+', '-', '*', '&', '/', '%', '<', '>', '^', '|',
        '=', ',', '?', ':', ';', '{', '}', '!', '~'
    }

    tmp, w = [], []
    i = 0
    if type(i) == None:
        return []
    while i < len(line):

        if line[i] == ' ':
            tmp.append(''.join(w).strip())
            tmp.append(line[i].strip())
            w = []
            i += 1
        # Check operators and append to final list
        elif line[i:i + 3] in operators3:
            tmp.append(''.join(w).strip())
            tmp.append(line[i:i + 3].strip())
            w = []
            i += 3
        elif line[i:i + 2] in operators2:
            tmp.append(''.join(w).strip())
            tmp.append(line[i:i + 2].strip())
            w = []
            i += 2
        elif line[i] in operators1:
            tmp.append(''.join(w).strip())
            tmp.append(line[i].strip())
            w = []
            i += 1
        # Character appended to word list
        else:
            w.append(line[i])
            i += 1
    if (len(w) != 0):
        tmp.append(''.join(w).strip())
        w = []

    tmp = list(filter(lambda c: (c != '' and c != ' '), tmp))
    return tmp


def process_parallel(path: str, split_token: bool):

    node_index = dict()
    tokens_list = list()
    try:
        pdg = nx.drawing.nx_pydot.read_dot(path)
        for index, node in enumerate(pdg.nodes()):
                node_index[node] = index
                try:
                    label = pdg.nodes[node]['label'][1:-1]
                except:
                    continue
                code = label.partition(',')[2]
                for token in tokenize_code_line(code):
                    tokens_list.append(token)
    except:
        pass

    return tokens_list

def train_word_embedding(config_path: str):

    config = cast(DictConfig, OmegaConf.load(config_path))

    train_path = "/opt/data/VCM/data/pdg/qemu/"

    paths=glob.glob(train_path+'/*')
    tokens_list = list()
    with Manager():
        pool = Pool(USE_CPU)
        process_func = functools.partial(process_parallel, split_token=True)
        tokens: List = [
            res
            for res in tqdm(
                pool.imap_unordered(process_func, paths),
                desc=f"pdg paths: ",
                total=len(paths),
            )
        ]
        pool.close()
        pool.join()

    tokens_list = []
    for token_l in tokens:
        tokens_list.extend(token_l)
    print("training w2v...")
    print(tokens)
    print(len(tokens_list))
    num_workers = cpu_count() if config.num_workers == -1 else config.num_workers
    model = Word2Vec(sentences=tokens, min_count=3, vector_size=100,
                     workers=num_workers, sg=1,max_vocab_size=config.dataset.token.vocabulary_size)
    model.wv.save("/opt/data/VCM/data/chromew2v100.wv")



if __name__ == '__main__':

    __arg_parser = ArgumentParser()
    __arg_parser.add_argument("-c",
                              "--config",
                              help="Path to YAML configuration file",
                              default="configs/config.yaml",
                              type=str)
    __args = __arg_parser.parse_args()
    train_word_embedding(__args.config)

