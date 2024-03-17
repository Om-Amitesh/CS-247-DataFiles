import numpy as np


def load_npz_data(text_path, labels_path):
    '''
        load_npz_data:
            Params:
                text_path: path to the .npz file pertaining to texts
                labels_path: path to the .npz pertaining to labels
            Returns:
                Tuple(
                encoded_text: a NxM np array that has N data points of M dimensional embeddings,
                labels: a N-sized np array with each element being a List() of label IDs for the corresponding text embedding row
                )
        Usage:
            from load_data import load_npz_data
            X, Y = load_npz_data('~/wikidata/enc_txt.npz', '~/wikidata/enc_labs.npz')
            # X - Text Embeddings N X 256 
            # Y - Labels N-sized List()s of arbritary length.
    '''
    encoded_text = np.load(text_path)['arr_0']
    labels = np.load(labels_path, allow_pickle=True)['arr_0']
    
    return encoded_text, labels