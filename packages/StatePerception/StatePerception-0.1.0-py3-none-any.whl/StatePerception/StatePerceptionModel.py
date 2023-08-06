"""
@author: Torben Gräber
"""

# Imports
from inspect import getargvalues, stack
import numpy as np

# Keras and Tensorflow Imports
from keras.models import Model, load_model
from keras.utils import multi_gpu_model
from keras.optimizers import Adam
from keras import backend as K
import tensorflow as tf
from tensorflow.python.platform import gfile
from tensorflow.python.framework.graph_util import convert_variables_to_constants

# Custom Imports
from .StatePerceptionKerasLayer import CustomFunctionsLib
from .StatePerceptionHelperFunctions import save_pickle_file, load_pickle_file


# Function and Class Definitions
def arguments():
    """Returns tuple containing dictionary of calling function's
       named arguments and a list of calling function's unnamed
       positional arguments.
    """
    posname, kwname, args = getargvalues(stack()[1][0])[-3:]
    posargs = args.pop(posname, [])
    args.update(args.pop(kwname, []))
    return args, posargs

class SPModel():
    '''
    General Class for SPModel holding the basis functionality for prediction,
    evaluation, saving and loading models.
    '''
    def __init__(self,n_features=None,n_outputs=None,request_scaled_X=True,request_scaled_Y=True,seq2seq_prediction=True,name=None,custom_objects={},settings={'opt':Adam},settings_opt={},settings_init={},additional_fit_args={},num_gpus=None):
        # Name
        self.name = name
        # Dimensions
        self.n_features = n_features
        self.n_outputs = n_outputs
        # Data Scaled / Unscaled
        self.request_scaled_X = request_scaled_X
        self.request_scaled_Y = request_scaled_Y
        # Model Type: Sequence2Sequence or Sequence2SinglePrediction
        self.seq2seq_prediction = seq2seq_prediction
        # Optimization Settings
        self.settings = settings
        self.settings_opt = settings_opt
        self.settings_init = settings_init
        self.additional_fit_args = additional_fit_args
        self.num_gpus = num_gpus
        # Custom Objects
        self.custom_objects = custom_objects
        # Function Args and Posargs
        self._funargs = arguments()
        
    def build_models(self):
        models = []
        models_gpu = []
        for i,inout in enumerate(self.model_inputs_outputs):
            model_i = Model(inout[0],inout[1])
            if self.num_gpus is not(None):
                model_i_gpu = multi_gpu_model(model_i,self.num_gpus)
            optimizer = self.settings['opt'](**self.settings_opt)
            if len(self.settings['loss'])>1:
                loss_curr = self.settings['loss'][i]
            else:
                loss_curr = self.settings['loss']
            model_i.compile(optimizer=optimizer,loss=loss_curr,metrics=self.settings['metrics'])
            models.append(model_i)
            if self.num_gpus is not(None):
                model_i_gpu.compile(optimizer=optimizer,loss=loss_curr,metrics=self.settings['metrics'])
                models_gpu.append(model_i)
        return models, models_gpu
    
    def evaluate(self,X,Y,batch_size=None,sample_weight=None,steps=None,submodel=0,use_gpus_if_available=True):
        '''
        Evaluate Model Performance on given inputs X and Y
        
        # Arguments
            X:          Input, numpy array, shape=()
            Y:          Reference Output, numpy array, shape=()
            submodel:   Indice of the submodel to evaluate. Model 0 is the model
                        used for training purposes.
        '''
        if use_gpus_if_available and self.num_gpus is not(None):
            evaluation = self.models_gpu[submodel].evaluate(X,Y,batch_size=batch_size,sample_weight=sample_weight,steps=steps)
        else:
            evaluation = self.models[submodel].evaluate(X,Y,batch_size=batch_size,sample_weight=sample_weight,steps=steps)
        return evaluation
    
    def get_metric_names(self,submodel=0):
        return self.models[submodel].metrics_names
    
    def predict(self,X,submodel=0,use_gpus_if_available=True,**kwargs):
        '''
        Function for prediction based on the input X. Submodels that are defined
        in the build_model() function can also be used for prediction. This is
        necessary if the target network for prediction differs from the one used
        for training.
        
        # Arguments
            X:          Input, numpy Array, shape=()
            submodel:   Indice of the submodel to evaluate. Model 0 is the model
                        used for training purposes.
        
        # Returns
            Y_pred:     Prediction of Y, shape=()
        
        '''
        # Predict
        if use_gpus_if_available and self.num_gpus is not(None):
            Y_pred = self.models_gpu[submodel].predict(X,**kwargs)
        else:
            Y_pred = self.models[submodel].predict(X,**kwargs)
        # Add List if Single Output Tensor
        if type(Y_pred)==np.ndarray:
            Y_pred = [Y_pred]
        return Y_pred
        
    def summary(self,submodel=0):
        print(self.models[submodel].summary())

    def _load_weights(self,savename,submodel):
        self.models[submodel].load_weights(filepath=savename)
    
    def _save_weights(self,savename,submodel):
        self.models[submodel].save_weights(filepath=savename)
    
    def _save_model(self,savename,submodel):
        self.models[submodel].save(filepath=savename)
    
#    def _load_model(self,savename,submodel):
#        cflib = CustomFunctionsLib()
#        self.models[submodel] = load_model(filepath=savename,custom_objects=cflib.fundict)
    
    def save_model(self,savename=None,submodel='all'):
        # Savename
        if savename is None:
            if self.name is None:
                print('Please pass savename to save function.')
            else:
                savename='SPModel_'+self.name
        # Save Model
        if submodel == 'all':
            for i_model,model in enumerate(self.models):
                self._save_model(savename+'_'+str(i_model)+'.spm',i_model)
        else:
            self._save_model(savename+'_'+str(submodel)+'.spm',submodel)
    
    def _freeze_session(self, session, keep_var_names=None, output_names=None, clear_devices=True):
        """
        Freezes the state of a session into a pruned computation graph.
        Creates a new computation graph where variable nodes are replaced by
        constants taking their current value in the session. The new graph will be
        pruned so subgraphs that are not necessary to compute the requested
        outputs are removed.
        @param session The TensorFlow session to be frozen.
        @param keep_var_names A list of variable names that should not be frozen,
                              or None to freeze all the variables in the graph.
        @param output_names Names of the relevant graph outputs.
        @param clear_devices Remove the device directives from the graph for better portability.
        @return The frozen graph definition.
        
        Code from https://github.com/pipidog/keras_to_tensorflow/blob/master/keras_to_tensorflow.py
        """
        graph = session.graph
        with graph.as_default():
            freeze_var_names = list(set(v.op.name for v in tf.global_variables()).difference(keep_var_names or []))
            #output_names = output_names or []
            #output_names += [v.op.name for v in tf.global_variables()]
            input_graph_def = graph.as_graph_def()
            if clear_devices:
                for node in input_graph_def.node:
                    node.device = ""
            frozen_graph = convert_variables_to_constants(session, input_graph_def,
                                                          output_names, freeze_var_names)
            return frozen_graph
    
    def freeze_model(self,savename='frozen_model',savepath='frozen_model/',model_indice_for_inference=1,save_additional_readable_graph=False):
        # Get Model
        model = self.models[model_indice_for_inference]
        # Get Model Meta Data
        input_names=[inp.op.name for inp in model.inputs]
        input_shapes=[inp.get_shape().as_list() for inp in model.inputs]
        output_names=[out.op.name for out in model.outputs]
        output_shapes=[out.get_shape().as_list() for out in model.outputs]
        # Freeze Graph and Write
        frozen_graph = self._freeze_session(K.get_session(),output_names=output_names)
        tf.train.write_graph(frozen_graph, savepath, savename+'.pb', as_text=False)
        if save_additional_readable_graph:
            tf.train.write_graph(frozen_graph, savepath, savename+'_text.pb', as_text=True)
        # Write Meta Data
        save_pickle_file(savename=savepath+savename+'.pkl',data=[input_names,input_shapes,output_names,output_shapes])
        # Write Meta Data Text File
        with open(savepath+savename+'.config','w') as f:
            f.write('Model Input Tensors:\n')
            for input_name in input_names:
                f.write(input_name+'\n')
            f.write('\n')
            f.write('Model Input Shapes:\n')
            for input_shape in input_shapes:
                f.write(str(input_shape)+'\n')
            f.write('\n')
            f.write('Model Output Tensors:\n')
            for output_name in output_names:
                f.write(output_name+'\n')
            f.write('\n')
            f.write('Model Output Shapes:\n')
            for output_shape in output_shapes:
                f.write(str(output_shape)+'\n')
            
#    def load_model(self,savename=None,submodel=0,n_models=1):
#        # Savename
#        if savename is None:
#            if self.name is None:
#                print('Please pass savename to load function.')
#            else:
#                savename='SPModel_'+self.name
#        # Save Model
#        if submodel == 'all':
#            self.models = []
#            for i_model in range(n_models):
#                self.models.append([])
#                self._load_model(savename+'_'+str(i_model)+'.spm',i_model)
#        else:
#            self.models[submodel] = self._load_model(savename+'_'+str(submodel)+'.spm',submodel)
                
class SPFrozenModel():
    
    def __init__(self):
        # Model Info
        self.input_names = None
        self.input_shapes = None
        self.input_tensors = None
        self.output_names = None
        self.output_shapes = None
        self.output_tensors = None
        # Tensorflow Session and Graph
        self.sess = None
        self.graph_def = None
        print('')
    
    def _init_model(self,save_graph=False):
        # Start Session
        self.sess = tf.Session()
        # Get Graph Def
        self.graph_def = tf.GraphDef()
        with gfile.FastGFile('frozen_model/frozen_model.pb','rb') as f:
            self.graph_def.ParseFromString(f.read())
            self.sess.graph.as_default()
            tf.import_graph_def(self.graph_def,name='frozen_graph')
        # Write Graph
        if save_graph:
            writer = tf.summary.FileWriter('frozen_model/log/')
            writer.add_graph(self.sess.graph)
            writer.flush()
            writer.close()
        # Get Input and Output Tensors
        self.input_tensors = [self.sess.graph.get_tensor_by_name('frozen_graph/'+name+':0') for name in self.input_names]
        self.output_tensors = [self.sess.graph.get_tensor_by_name('frozen_graph/'+name+':0') for name in self.output_names]
        
    def load_frozen_model(self,savename='frozen_model',savepath='frozen_model/'):
        # Load Frozen Model
        [self.input_names,self.input_shapes,self.output_names,self.output_shapes] = load_pickle_file(savename=savepath+savename+'.pkl')
        # Init Frozen Model
        self._init_model()
    
    def predict(self,x):
        # Predict
        predictions = self.sess.run(self.output_tensors[0], {self.input_tensors[0]: x})
        return predictions