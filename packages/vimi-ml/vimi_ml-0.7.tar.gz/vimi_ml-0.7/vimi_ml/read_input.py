import ast
class ReadInput(object):
    
    def read_input(input_text_file):
        d = {}
        with open(input_text_file) as f:
            for line in f:
                (key, val) = line.split('=', 2)
                d[(key)] = val.strip()
                d[(key)] = d[(key)].replace("\n", '')
        for key in d:
            if (key in ['data_preprocess','hyperparameters','input_features','target_feature','plots']):
                d[key] = ast.literal_eval(d[key])
        
                
        return d