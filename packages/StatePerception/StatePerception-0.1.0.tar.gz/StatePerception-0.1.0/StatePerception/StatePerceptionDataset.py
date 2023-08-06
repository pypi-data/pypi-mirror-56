"""
@author: Torben Gräber

TODO:
    - Repair load and save scripts
    
    - Add Measurement Functions
        - Add from MF4
        - Add from MAT
    
    - Restructure Raw Data Representation
        - Add Meta Data (Labels)
        - Manage Data in 
    
    - Plotting Tool
        - Vetical Lines for New file
        - name of Files on vertical line
        
        - Seperate plots for every signal
    
    - Function Check consistency
        - dimensions X, Y, labels, etc
    - check Consistency on first Call init
    
    - X Labels, Y Labels and Title for Standard Plots
    
    - Get Data (only valid)
    - Filter by Signals (e.g. Speed)
    

"""

# Imports
import numpy as np
from numpy.lib.stride_tricks import as_strided
from scipy.io import loadmat, savemat
import matplotlib.pyplot as plt

from keras.utils.data_utils import Sequence
from sklearn.preprocessing import StandardScaler

from .StatePerceptionHelperFunctions import save_pickle_file, load_pickle_file, ensure_dir

# Function and Class Definitions
class SPDataset():
    '''
    class SPDataset()
    
    # Description
    Class holding a dataset for a state perception task. A data set can be made
    up of many measurements. Each measurement holds Inputs X, Outputs Y, a 
    Validity I in a list. The validity vector describes where the reference Y
    is valid (1) or invalid (0). If no validity I is given, it is assumed that
    all data points are valid.
    
    Each dataset (train/val/test) is a list of measurements:
        
        data_* = [meas1_*, meas2_*, ...]
        
    Each measurement holds the Inputs X, Outputs Y, and a Validity I in a list:
        
        meas1_* = [X_meas1_*, Y_meas1_*]
    
    Each of these entries are a list of numpy arrays (the model can have an
    arbitrary number of input and output tensors, but only one validity vector):
        
        X_meas1_* = [X1_meas1_*, X2_meas1_*,...]
            X1_meas1_* = np.array(...)           # shape = (n_*,n_features_1)
            X2_meas1_* = np.array(...)           # shape = (n_*,n_features_2)
            ...                                  ...
            
        Y_meas1_* = [Y1_meas1_*, Y2_meas1_*,...]
            Y1_meas1_* = np.array(...)           # shape = (n_*,n_outputs_1)
            Y2_meas1_* = np.array(...)           # shape = (n_*,n_outputs_2)
            ...                                  ...
            
        I_meas1_* = [I1_meas1_*]
            I1_meas1_* = np.array(...)           # shape = (n_*,1)
    
    Example with two input tensors and one output tensor:
        
            data_train = [ [[X11,X12],[Y11],[I11]] ,[[X21,X22],[Y21],[I21]] ]
        
    If the dataset only consists of one measurement, the dataset can easily be
    initialized via the function SPDataset.init_from_XY_arrays().
    
    # Arguments
        
        * = (train/val/test)
        
        data_*:     list of measurements in dataset * as described above.
        dt:         Sample time of Data Set (assumed to be constant)
        X_scaler:   List of Scaler Objects in SKLearn format. Custom scaler need 
                    implemented .fit() .transform() .inverse_transform() functions.
        Y_scaler:   List of Scaler Objects in SKLearn format. Custom scaler need 
                    implemented .fit() and .transform() functions.
        X_signal_names:     List of Signal Names of Input Data (for documentation or
                            and Plotting Purposes). Optional. Shape must match number
                            of measurements and number of inputs X.
        Y_signal_names:     List of Signal Names of Output Data (for documentation or
                            and Plotting Purposes). Optional. Shape must match number
                            of measurements and number of outputs Y.
        X_signal_units:     List of Signal Units of Input Data (for documentation or
                            and Plotting Purposes). Optional. Shape must match number
                            of measurements and number of inputs X.
        Y_signal_units:     List of Signal Units of Output Data (for documentation or
                            and Plotting Purposes). Optional. Shape must match number
                            of measurements and number of outputs Y.
        name:       Name of Dataset
        
    # Functions
        
    '''
    def __init__(self,data_train=None,data_val=None,data_test=None,dt=None,X_scaler=None,Y_scaler=None,X_signal_names=None,Y_signal_names=None,X_signal_units=None,Y_signal_units=None,name=None,verbose=True):
        # Verbosity
        self.verbose = verbose
        # Write Data to Object
        self.data_train = data_train
        self.data_val   = data_val
        self.data_test  = data_test
        # Check Validity Vectors I and Dimensions
        # Set Data Sets to None if no Entries
        if self.data_train is not(None):
            if len(self.data_train)==0:
                self.data_train = None 
                if self.verbose:
                    print('WARNING: Training Data List Empty - Setting Training Data to None')
        if self.data_val is not(None):
            if len(self.data_val)==0:
                self.data_val = None 
                if self.verbose:
                    print('WARNING: Validation Data List Empty - Setting Validation Data to None')
        if self.data_test is not(None):
            if len(self.data_test)==0:
                self.data_test = None 
                if self.verbose:
                    print('WARNING: Test Data List Empty - Setting Test Data to None')
        # Scaler X
        if X_scaler is None and self.X_train is not(None):
            X_scaler = [StandardScaler() for _ in self.X_train]
        self.X_scaler = X_scaler
        # Scaler Y
        if Y_scaler is None and self.Y_train is not(None):
            Y_scaler = [StandardScaler() for _ in self.Y_train]
        self.Y_scaler = Y_scaler
        # Time Constant
        self.dt = dt
        # Signal Names and Units
        self.X_signal_names = X_signal_names
        self.Y_signal_names = Y_signal_names
        self.X_signal_units = X_signal_units
        self.Y_signal_units = Y_signal_units
        # Dataset Name
        self.name = name
        # Savelist for Saving and Loading
        self._savelist = [self.data_train,self.data_val,self.data_test,self.X_signal_names,self.Y_signal_names,self.X_signal_units,self.Y_signal_units,self.X_scaler,self.Y_scaler]
    
    def add_measurement(self,X,Y,I=None,dataset='train'):
        # Check Dimensions and Consistency
        
        # Check if Data initialized. If Not Initialize. If yes, append
        
        # Append to fitting array
        
        print('Not implemented yet')
    
    def init_from_XY_arrays(self,X_train=None,Y_train=None,I_train=None,X_val=None,Y_val=None,I_val=None,X_test=None,Y_test=None,I_test=None,dt=None,X_scaler=None,Y_scaler=None,X_signal_names=None,Y_signal_names=None,X_signal_units=None,Y_signal_units=None,name=None):
        # If data is list of arrays keep, if single array pack in list
        X_train = [X_train] if type(X_train)==np.ndarray else X_train
        Y_train = [Y_train] if type(Y_train)==np.ndarray else Y_train
        I_train = [I_train] if type(I_train)==np.ndarray else I_train
        X_val =   [X_val]   if type(X_train)==np.ndarray else X_val
        Y_val =   [Y_val]   if type(Y_train)==np.ndarray else Y_val
        I_val =   [I_val]   if type(I_train)==np.ndarray else I_val
        X_test =  [X_test]  if type(X_train)==np.ndarray else X_test
        Y_test =  [Y_test]  if type(Y_train)==np.ndarray else Y_test
        I_test =  [I_test]  if type(I_train)==np.ndarray else I_test
        # Construct data_train, data_val and data_test. I_* is optional
        if X_train is not(None):
            data_train = [[X_train,Y_train]] if I_train is None else [[X_train,Y_train,I_train]]
        else:
            data_train = None
        if X_val is not(None):
            data_val = [[X_val,Y_val]] if I_val is None else [[X_val,Y_val,I_val]]
        else:
            data_val = None
        if X_test is not(None):
            data_test = [[X_test,Y_test]] if I_test is None else [[X_test,Y_test,I_test]]
        else:
            data_test = None
        # Call Init
        self.__init__(data_train=data_train,data_val=data_val,data_test=data_test,
                      dt=dt,X_scaler=X_scaler,Y_scaler=Y_scaler,
                      X_signal_names=X_signal_names,Y_signal_names=Y_signal_names,
                      X_signal_units=X_signal_units,Y_signal_units=Y_signal_units,
                      name=name)
    
    def add_data_from_mat(self):        
        print('Not implemented yet.')
    
    def add_data_from_mdf(self):        
        print('Not implemented yet.')
    
    def _scaler_fit_on_2d_arrays(self,scaler_in,arrays_in):
        scaler_out = []
        for scaler_, array_ in zip(scaler_in, arrays_in):
            scaler_ = scaler_.fit(array_)
            scaler_out.append(scaler_)
        return scaler_out
    
    def _get_scaled_2d_arrays(self,scaler_in,arrays_in):
        arrays_standardized_out = []
        for scaler_, array_ in zip(scaler_in, arrays_in):
            array_std_ = scaler_.transform(array_)
            arrays_standardized_out.append(array_std_)
        return arrays_standardized_out
    
    def _fit_X_scaler(self):
        if self.X_train is not(None):
            self._X_scaler = self._scaler_fit_on_2d_arrays(self.X_scaler,self.X_train)
        else:
            if self.verbose:
                print('No training data available. Cancelling scaling...')
    
    def _fit_Y_scaler(self):
        if self.Y_train is not(None):
            Y = self._set_inval_Y_to_zero(self.Y_train,self.I_train)
            self._Y_scaler = self._scaler_fit_on_2d_arrays(self.Y_scaler,Y)
    
    def _unscale_X(self,X_scaled):
        return self._unscale_XorY(X_scaled,choice='X')
    
    def _unscale_Y(self,Y_scaled):
        return self._unscale_XorY(Y_scaled,choice='Y')
    
    def _unscale_XorY(self,array_scaled,choice):
        # Check Format of X
        islist = isinstance(array_scaled,list)
        # Get Scaler
        if choice == 'X':
            scaler = self._X_scaler
        elif choice == 'Y':
            scaler = self._Y_scaler
        # Apply Unscaler
        if islist:
            array_unscaled = []
            for scaler, array_ in zip(scaler, array_scaled):
                array_unscaled.append(self._unscale_np_array(scaler,array_))
        else:
            scaler = self._X_scaler[0]
            array_unscaled = self._unscale_np_array(scaler,array_)
        # Return
        return array_unscaled
    
    def _unscale_np_array(self,scaler_in,array_in):
        shape = array_in.shape
        dimensions = len(shape)
        if dimensions == 2:
            array_out = scaler_in.inverse_transform(array_in)
        elif dimensions == 3:
            array_in_2d = array_in.reshape((array_in.shape[0]*array_in.shape[1],array_in.shape[2]))
            array_out_2d = scaler_in.inverse_transform(array_in_2d)
            array_out = array_out_2d.reshape((array_in.shape[0],array_in.shape[1],array_in.shape[2]))
        return array_out
    
    def _batch_arrays(self,Tensor,timesteps=None,shift=None):
        '''
        Function for batching the dataset. Useful as data preparation for
        fit() function.
        
        # Arguments
            Tensor:     2D Numpy Array
            timesteps:  number of time steps in sample
            shift:      shift of timesteps between beginnings of batches
            
        # Outputs
            Tesor_:     3D Numpy Array (batched)
        '''
        # Settings
        if timesteps is None:
            timesteps = Tensor.shape[0]
        if shift is None:
            shift = timesteps
        # Batch Arrays
        Tensor_ = []
        for i in range(int(np.floor(Tensor.shape[0]/shift))):
            start, end = i*shift, i*shift+timesteps
            if end>Tensor.shape[0]:
                continue
            Tensor_.append(Tensor[start:end,:])
        Tensor_ = np.stack(Tensor_)
        return Tensor_
    
    def _batch_list_of_arrays(self,X,Y,I,timesteps=None,shift=None):
        # Settings
        if timesteps is None:
            timesteps = X[0].shape[0]
        if shift is None:
            shift = timesteps
        # Batch Tensors
        X_list, Y_list, I_list = [], [], []
        for X_curr in X:
            X_list.append(self._batch_arrays(X_curr,timesteps=timesteps,shift=shift))
        for Y_curr in Y:
            Y_list.append(self._batch_arrays(Y_curr,timesteps=timesteps,shift=shift))
        for I_curr in I:
            I_list.append(self._batch_arrays(I_curr,timesteps=timesteps,shift=shift))
        # Return
        return X_list, Y_list, I_list
    
    def _tensorsignal_to_pick_signal(self,tensor,signal):
        pick_signal = []
        n_tensors = self.n_X if tensor[0]=='X' else self.n_Y
        for i in range(n_tensors):
            if i==tensor[1]:
                pick_signal.append([signal])
            else:
                pick_signal.append([])
        return pick_signal
    
    def _get_signal_from_tensor(self,dataset,tensor,signal,indices=None,scaled=False):
        '''
        tensor = ['X',0] # pick tensor
        signal = 0 # pick signal from tensor
        '''
        # Create pick_signals - Axis 1
        pick_signal = self._tensorsignal_to_pick_signal(tensor,signal)
        # Choose Datset + Mapping
        signal = self._get_tensor(dataset=dataset,tensor=tensor[0],scaled=scaled,indices=indices,pick_signals=pick_signal)[tensor[1]]
        return signal
    
    def _scale_tensor():
        # Consolidate Code in properties
        print('Not implemented yet')
    
    def _discard_invalid():
        # Consolidate Code in properties
        print('Not implemented yet')
    
    def _get_tensor(self,dataset,tensor,scaled,indices=None,pick_signals=None,discard_invalid=False):
        # Data Mapping
        if dataset == 'all':
            if tensor == 'X':
                if discard_invalid is False:
                    tensor = self.X_scaled if scaled else self.X
                else:
                    tensor = self.X_valid_scaled if scaled else self.X_valid
            elif tensor == 'Y':
                if discard_invalid is False:
                    tensor = self.Y_scaled if scaled else self.Y
                else:
                    tensor = self.Y_valid_scaled if scaled else self.Y_valid
            elif tensor == 'I':
                if discard_invalid is False:
                    tensor = self.I
                else:
                    tensor = self.I_valid
            else:
                return None
        elif dataset == 'train':
            if tensor == 'X':
                if discard_invalid is False:
                    tensor = self.X_train_scaled if scaled else self.X_train
                else:
                    tensor = self.X_train_valid_scaled if scaled else self.X_train_valid
            elif tensor == 'Y':
                if discard_invalid is False:
                    tensor = self.Y_train_scaled if scaled else self.Y_train
                else:
                    tensor = self.Y_train_valid_scaled if scaled else self.Y_train_valid
            elif tensor == 'I':
                if discard_invalid is False:
                    tensor = self.I_train
                else:
                    tensor = self.I_train_valid
            else:
                return None
        elif dataset == 'val':
            if tensor == 'X':
                if discard_invalid is False:
                    tensor = self.X_val_scaled if scaled else self.X_val
                else:
                    tensor = self.X_val_valid_scaled if scaled else self.X_val_valid
            elif tensor == 'Y':
                if discard_invalid is False:
                    tensor = self.Y_val_scaled if scaled else self.Y_val
                else:
                    tensor = self.Y_val_valid_scaled if scaled else self.Y_val_valid
            elif tensor == 'I':
                if discard_invalid is False:
                    tensor = self.I_val
                else:
                    tensor = self.I_val_valid
            else:
                return None
        elif dataset == 'test':
            if tensor == 'X':
                if discard_invalid is False:
                    tensor = self.X_test_scaled if scaled else self.X_test
                else:
                    tensor = self.X_test_valid_scaled if scaled else self.X_test_valid
            elif tensor == 'Y':
                if discard_invalid is False:
                    tensor = self.Y_test_scaled if scaled else self.Y_test
                else:
                    tensor = self.Y_test_valid_scaled if scaled else self.Y_test_valid
            elif tensor == 'I':
                if discard_invalid is False:
                    tensor = self.I_test
                else:
                    tensor = self.I_test_valid
            else:
                return None
        else:
            return None
        # Check indices
        if indices is None:
            if dataset == 'all':
                indices = [0,self.n_samples]
            elif dataset == 'train':
                indices = [0,self.n_train]
            elif dataset == 'val':
                indices = [0,self.n_val]
            elif dataset == 'test':
                indices = [0,self.n_test]
            else:
                return None
        # Apply Picks and Indices
        tensor = [(tensor_[indices[0]:indices[1],sig],sig)[0] for tensor_,sig in zip(tensor,pick_signals)] if pick_signals is not(None) else [tensor_[indices[0]:indices[1],:] for tensor_ in tensor]
        # Return
        return tensor
    
    def _get_XYI(self,dataset,scaled_X,scaled_Y,indices=None,pick_signals_X=None,pick_signals_Y=None,discard_invalid=False):
        # Get Data
        X = self._get_tensor(dataset=dataset,tensor='X',scaled=scaled_X,indices=indices,pick_signals=pick_signals_X,discard_invalid=discard_invalid)
        Y = self._get_tensor(dataset=dataset,tensor='Y',scaled=scaled_Y,indices=indices,pick_signals=pick_signals_Y,discard_invalid=discard_invalid)
        I = self._get_tensor(dataset=dataset,tensor='I',scaled=False,indices=indices,pick_signals=None,discard_invalid=discard_invalid)
        # Return
        return X, Y, I
    
    def _set_inval_Y_to_zero(self,Y,I):
        Y_out = []
        I_ = I[0]
        for Y_ in Y:
            Y_out.append(np.multiply(Y_,I_))
        return Y_out
    
#    def _set_inval_Y_to_value(self,Y,I):
#        Y_out = []
#        I_ = I[0]
#        for Y_ in Y:
#            Y_out.append(np.multiply(Y_,I_))
#        return Y_out
    
    def _validity_vector_transitions(self,dataset,inval_timesteps):
        if dataset == 'train':
            idx_transition = [np.sum(self.n_train_list[:i]) for i in range(self.n_meas_train)]
            I = self.I_train
        elif dataset == 'val':
            idx_transition = [np.sum(self.n_val_list[:i]) for i in range(self.n_meas_val)]
            I = self.I_val
        elif dataset == 'test':
            idx_transition = [np.sum(self.n_test_list[:i]) for i in range(self.n_meas_test)]
            I = self.I_test
        I_transitions = np.ones_like(I)
        for idx in idx_transition:
            I_transitions[0,idx:idx+inval_timesteps,0] = 0
        return I_transitions
    
    def summary(self):
        # General Info
        print(' ')
        print('------------------------------------------------------')
        if self.name:
            print('Data Summary - ' + self.name)
        else:
            print('Data Summary - (no name given)')
        print('------------------------------------------------------')
        print(' ')
        
        # Number of Measurements and Samples
        data_info_1 = [['Overall',self.n_meas_train+self.n_meas_val+self.n_meas_test,self.n_train+self.n_val+self.n_test,100],
                            ['Train',self.n_meas_train,self.n_train,self.n_train/(self.n_samples)*100],
                            ['Val',self.n_meas_val,self.n_val,self.n_val/(self.n_samples)*100],
                            ['Test',self.n_meas_test,self.n_test,self.n_test/(self.n_samples)*100]]
        
        template_header = '{0:14}|{1:8}{2:13}{3:9}' # column widths: 8, 10, 15, 7, 10
        template = '{0:14}|{1:8}{2:13}{3:9.2f}' # column widths: 8, 10, 15, 7, 10
        print(template_header.format('Measurements', ' Number', ' Samples', ' Percent')) # header
        print(template_header.format('--------------', '--------', '-------------', '---------')) # header
        for rec in data_info_1: 
          print(template.format(*rec))
        print(' ')
        
        # Number of Inputs and Outputs
        data_info_0 = [['Input X',self.n_X,self.n_features],
                       ['Output Y',self.n_Y,self.n_outputs],
                       ['Validity I',1,' ']]
        
        template_header = '{0:14}|{1:8}{1:10}' # column widths: 8, 10, 15, 7, 10
        template = '{0:14}|{1:8}{1:10}' # column widths: 8, 10, 15, 7, 10
        print(template_header.format('Tensor', ' Number', 'Dimension')) # header
        print(template_header.format('--------------', '--------','-------')) # header
        for rec in data_info_0: 
          print(template.format(*rec))
        print(' ')
        
        # Description Input Tensors
        input_tensor_info = []
        for i in range(self.n_X):
            input_tensor_info.append(['Tensor ' + str(i),self.n_features[i]])
#            print('Dimensions of Tensor ' + str(i) + ': ' + str(self.n_features[i]))
#            print('')
            
        template_header = '{0:14}|{1:8}' # column widths: 8, 10, 15, 7, 10
        template = '{0:14}|{1:8}' # column widths: 8, 10, 15, 7, 10
        print(template_header.format('Input Tensor', ' Dimension')) # header
        print(template_header.format('--------------', '----------','-------')) # header
        for rec in input_tensor_info:
            print(template.format(*rec))
         
        # Description Output Tensors
        output_tensor_info = []
        for i in range(self.n_Y):
            output_tensor_info.append(['Tensor ' + str(i),self.n_outputs[i]])
#            print('Dimensions of Tensor ' + str(i) + ': ' + str(self.n_features[i]))
#            print('')
            
        template_header = '{0:14}|{1:8}' # column widths: 8, 10, 15, 7, 10
        template = '{0:14}|{1:8}' # column widths: 8, 10, 15, 7, 10
        print(template_header.format('Input Tensor', ' Dimension')) # header
        print(template_header.format('--------------', '----------','-------')) # header
        for rec in output_tensor_info:
          print(template.format(*rec))
            
        if self.X_signal_names:
            print(' ')
            print('Signal Names Input:')
            print(self.X_signal_names)
        else:
            print('No signal names given.')
        
        if self.Y_signal_names:
            print(' ')
            print('Signal Names Input:')
            print(self.Y_signal_names)
        else:
            print('No signal names given.')
        
        # Scaler for Tensors
        print('(Info scaling not available yet.)')
    
    def _discard_invalid_samples(self,X,Y,I,method='complete'):
        # Initialize Arrays
        Xv, Yv, Iv = [], [], []
        # Get indices of valid samples
        if method=='complete' or method==True:
            samples_valid = np.where(np.all(I[0],axis=1))[0]
        elif method=='last timestep':
            samples_valid = np.where(I[0][:,-1,:])[0]
        else:
            raise ValueError('Not a valid discard method for invalid samples. Choose between [''complete'',''last timestep'']')
        # Pick valid samples
        for X_,Y_ in zip(X,Y):
            Xv.append(X_[samples_valid,:,:])
            Yv.append(Y_[samples_valid,:,:])
        Iv.append(I[0][samples_valid,:,:])
        # Return
        return Xv,Yv,Iv
    
    def get_3D_data(self,dataset='train',scaled_X=True,scaled_Y=True,timesteps=None,shift=None,zero_inval_Y=True,set_measurement_transition_invalid=False,indices=None,seq2seq_prediction=True,pick_signals_X=None,pick_signals_Y=None,discard_invalid=False):
        '''
        Returns a numpy array with batched training data for keras.
        
        # Arguments
            dataset: Dataset train/val/test
            scaled_X: If true returns scaled data, if false unscaled
            scaled_Y: If true returns scaled data, if false unscaled
            timesteps: Timesteps in one batch. If None all timesteps are in
                one batch. If it has a value the data is batched.
            shift: Shift between the start of two batches. If None, then
                shift = timesteps. This means that every data point will be in
                once in the batched data.
            zero_inval_Y: Sets invalid Outputs Y to zero. This is used to elimi-
                nate it from the cost function in training.
            set_measurement_transitions_invalid: The measurements available in
                the data set are batched to one array and then cut to batches.
                If there is a transition between datasets this can cause "steps"
                between the measurements. The estimators will be given a number
                of timesteps to converge, where the cost function is set to zero.
                Set to False if not necessary.
                
        # Returns
            X: List of inputs. Each input is numpy array with shape=(batches,
                timesteps,features). Equivalent to keras format.
            Y: List of outputs. Each output is numpy array with shape=(batches,
                timesteps,outputs). Equivalent to keras format.
            I: List with single entry validity. shape=(batches,timesteps,1)
        '''
        # Parameters
        if shift is None:
            shift = timesteps
        # Get Data
        X, Y, I = self._get_XYI(dataset,scaled_X,scaled_Y,indices,pick_signals_X=pick_signals_X,pick_signals_Y=pick_signals_Y)
        # Set Validity at Measurement Transition to Zero if Necessary
        if set_measurement_transition_invalid and timesteps is not(None):
            I_transition = self._validity_vector_transitions(dataset,inval_timesteps=timesteps)
            I = I * I_transition
        # Multiply Invalid Reference Y by Zero
        if zero_inval_Y:
            Y = self._set_inval_Y_to_zero(Y,I)
        # Batch Data
        X, Y, I = self._batch_list_of_arrays(X,Y,I,timesteps=timesteps,shift=shift)
        # Discard Invalid Samples
        if discard_invalid:
            X, Y, I = self._discard_invalid_samples(X,Y,I,method=discard_invalid)
        # Extract last Time Step for Y and I if no Sequence to Sequence Prediction
        if not(seq2seq_prediction):
            Y = [Y_[:,[-1],:] for Y_ in Y]
            I = [I_[:,[-1],:] for I_ in I]
        return X,Y,I
        
    def get_timeseries_generator(self,timesteps,batch_size,dataset='train',scaled_X=True,scaled_Y=True,seq2seq_prediction=False):
        '''
        Time series generator for .fit_generator() in Keras, built on SPDataset.
        
        # Arguments
            timesteps: Timesteps in one batch.
            batch_size: Batch size for gradient update during training.
            dataset: Dataset upon which time series generator is built. 'train'
                for training purposes.
            scaled: If true, provides scaled data set, if False unscaled.
        
        # Returns
            SPTSG: State Perception Time Series Generator for use with SPTrainer
        
        '''
        # Get Data
        X, Y, I = self._get_XYI(dataset,scaled_X=scaled_X,scaled_Y=scaled_Y)
        # Create Flags
        flag_3d_X = []
        for _ in [*X,*I]:
            flag_3d_X.append(True)
        flag_3d_Y = []
        for _ in Y:
            flag_3d_Y.append(True)
        # Instantiate Time Series Generator
        SPTSG = SPTimeSeriesGenerator(data=[*X,*I],flag_3d_data=flag_3d_X,targets=Y,flag_3d_targets=flag_3d_Y,look_back=timesteps,batch_size=batch_size,seq2seq_prediction=seq2seq_prediction)
        return SPTSG
    
    def _save_dataset_mat(self,savename):
        # Save Data in Mat File
        savedict = {'X_train':self.X_train,'Y_train':self.Y_train,'I_train':self.I_train,
                    'X_val':self.X_val,'Y_val':self.Y_val,'I_val':self.I_val,
                    'X_test':self.X_test,'Y_test':self.Y_test,'I_test':self.I_test,
                    'X_train_scaled':self.X_train_scaled,'Y_train_scaled':self.Y_train_scaled,
                    'X_val_scaled':self.X_val_scaled,'Y_val_scaled':self.Y_val_scaled,
                    'X_test_scaled':self.X_test_scaled,'Y_test_scaled':self.Y_test_scaled,
                    'dt':self.dt,
                    'X_mean':self.X_mean,'X_scale':self.X_scale,'Y_mean':self.Y_mean,'Y_scale':self.Y_scale,
                    'X_signal_names':self.X_signal_names,'Y_signal_names':self.Y_signal_names,
                    'X_signal_units':self.X_signal_units,'Y_signal_units':self.Y_signal_units,
                    'name':self.name}
        savedict = {k:v for k,v in savedict.items() if v is not(None)}
        if savename is not(None):
            savemat(savename,savedict)
        else:
            print('Data set hasnt ben saved, no savename was given.')

    def _save_dataset_pickle(self,savename):
        save_pickle_file(savename,self._savelist)
        
    def _load_dataset_pickle(self,savename):
        [self.data_train,self.data_val,self.data_test,self.X_signal_names,self.Y_signal_names,self.X_signal_units,self.Y_signal_units,self.X_scaler,self.Y_scaler] = load_pickle_file(savename)
        
    def save_dataset(self,savename=None,savepath='data/',saveformat='pickle'):
        # Determine Savename
        if savename is None:
            if self.name is None:
                print('Please pass savename to save_dataset function.')
            else:
                savename='SPData_'+self.name
        # Ensure Directory
        if savepath:
            ensure_dir(savepath)
        # Choose Format
        if saveformat == 'pickle':
            self._save_dataset_pickle(savepath+savename)
        elif saveformat == 'mat':
            self._save_dataset_mat(savepath+savename)
        else:
            print('Not a valid format.')
    
    def load_dataset(self,savename=None,savepath='data/',saveformat='pickle'):
        # Determine Savename
        if savename is None:
            if self.name is None:
                print('Please pass savename to save_dataset function.')
            else:
                savename='SPData_'+self.name
        # Choose Format
        if saveformat == 'pickle':
            self._load_dataset_pickle(savepath+savename)
        elif saveformat == 'mat':
            self._load_dataset_mat(savepath+savename)
        else:
            print('Not a valid format.')
    
    def _construct_legend_entry(self,i_signal,name,unit,bias,scale):
        if name is None:
            legend_entry = 'Signal {:d}'.format(i_signal)
        else:
            legend_entry = name
        if unit is not(None):
            legend_entry = legend_entry + ' [{:s}]'.format(unit)
        if bias is not(None):
            legend_entry = legend_entry + '-{:1.3f}'.format(bias)
        if scale is not(None):
            legend_entry = legend_entry + '*{:1.3f}'.format(scale)
        return legend_entry
    
    def _get_legend_entry(self,tensor,signal,scaled=False):
        # Generate Pick Signals
        pick_signal = self._tensorsignal_to_pick_signal(tensor,signal)
        # Get Signal Name from Legend Entriy
        legend_entry = self._get_legend_entries(tensor=tensor[0],scaled=scaled,pick_signals=pick_signal)[tensor[1]][0]
        # Return
        return legend_entry
    
    def _get_legend_entries(self,tensor='X',scaled=True,pick_signals=None):
        # Mapping
        if tensor=='X':
            n = self.n_features
            signal_names = self.X_signal_names
            signal_units = self.X_signal_units
            biases = self.X_mean
            scales = self.X_scale
        elif tensor=='Y':
            n = self.n_outputs
            signal_names = self.Y_signal_names
            signal_units = self.Y_signal_units
            biases = self.Y_mean
            scales = self.Y_scale
        else:
            return None
        # Construct Legend Entries
        legend_entries = []
        # Loop over Input Tensors
        for i_tensor,n_tensor in enumerate(n):
            # Construct Legend Entries Current Tensor
            legend_entries_tensor = []
            # Loop over Signals
            for i_signal in range(n_tensor):
                # Get Elements
                name_ = signal_names[i_tensor][i_signal] if signal_names is not(None) else None
                unit_ = signal_units[i_tensor][i_signal] if signal_units is not(None) else None
                bias_ = biases[i_tensor][i_signal] if biases is not(None) and scaled else None
                scale_ = scales[i_tensor][i_signal] if scales is not(None) and scaled else None
                # Get Legend Name
                legend_entry = self._construct_legend_entry(i_signal,name_,unit_,bias_,scale_)
                if pick_signals is None or i_signal in pick_signals[i_tensor]:
                    legend_entries_tensor.append(legend_entry)
            # Append Legend Entries Current Tensor
            legend_entries.append(legend_entries_tensor)
        # Return
        return legend_entries
    
    def _get_histogram(self,dataset='train',bins=50,normalize=True):
        # Choose Datset + Mapping
        X,Y,_ = self.get_3D_data(dataset)
        # Loop over Model Outputs
        histogramX = []
        histogramY = []
        # Histogram X
        for X_ in X:
            # Loop over Output Signals
            histogramX.append([])
            for X_sig_ in X_[0].transpose():
                # Calculate Histogram
                x_h = np.histogram(X_sig_,bins=bins)
                x_h = x_h + (x_h[0]/np.sum(x_h[0]),)
                # Append
                histogramX[-1].append(x_h)
        # Hisotgram Y
        for Y_ in Y:
            # Loop over Output Signals
            histogramY.append([])
            for Y_sig_ in Y_[0].transpose():
                # Calculate Histogram
                y_h = np.histogram(Y_sig_,bins=bins)
                y_h = y_h + (y_h[0]/np.sum(y_h[0]),)
                # Append
                histogramY[-1].append(y_h)
        # Return
        return histogramX, histogramY
    
    @property
    def X(self):
        if self.X_train is None and self.X_val is None and self.X_test is None:
            return None
        else:
            X = []
            for i_tensor in range(self.n_X):
                Tensor = []
                if self.X_train is not(None):
                    Tensor.append(self.X_train[i_tensor])
                if self.X_val is not(None):
                    Tensor.append(self.X_val[i_tensor])
                if self.X_test is not(None):
                    Tensor.append(self.X_test[i_tensor])
                X.append(np.concatenate(Tensor,axis=0))
            return X
    
    @property
    def X_train(self):
        if self.data_train is not(None):
            X_train = []
            for i_tensor in range(self.n_X):
                X_train.append(np.concatenate([meas[0][i_tensor] for meas in self.data_train],axis=0))
            return X_train
        else:
            return None
    
    @property
    def X_val(self):
        if self.data_val is not(None):
            X_val = []
            for i_tensor in range(self.n_X):
                X_val.append(np.concatenate([meas[0][i_tensor] for meas in self.data_val],axis=0))
            return X_val
        else:
            return None
    
    @property
    def X_test(self):
        if self.data_test is not(None):
            X_test = []
            for i_tensor in range(self.n_X):
                X_test.append(np.concatenate([meas[0][i_tensor] for meas in self.data_test],axis=0))
            return X_test
        else:
            return None
    
    @property
    def Y(self):
        if self.Y_train is None and self.Y_val is None and self.Y_test is None:
            return None
        else:
            Y = []
            for i_tensor in range(self.n_Y):
                Tensor = []
                if self.Y_train is not(None):
                    Tensor.append(self.Y_train[i_tensor])
                if self.Y_val is not(None):
                    Tensor.append(self.Y_val[i_tensor])
                if self.Y_test is not(None):
                    Tensor.append(self.Y_test[i_tensor])
                Y.append(np.concatenate(Tensor,axis=0))
            return Y
        
    @property
    def Y_train(self):
        if self.data_train is not(None):
            Y_train = []
            for i_tensor in range(self.n_Y):
                Y_train.append(np.concatenate([meas[1][i_tensor] for meas in self.data_train],axis=0))
            return Y_train
        else:
            return None
    
    @property
    def Y_val(self):
        if self.data_val is not(None):
            Y_val = []
            for i_tensor in range(self.n_Y):
                Y_val.append(np.concatenate([meas[1][i_tensor] for meas in self.data_val],axis=0))
            return Y_val
        else:
            return None
    
    @property
    def Y_test(self):
        if self.data_test is not(None):
            Y_test = []
            for i_tensor in range(self.n_Y):
                Y_test.append(np.concatenate([meas[1][i_tensor] for meas in self.data_test],axis=0))
            return Y_test
        else:
            return None
    
    @property
    def I(self):
        if self.I_train is None and self.I_val is None and self.I_test is None:
            return None
        else:
            I = []
            for i_tensor in range(1):
                Tensor = []
                if self.I_train is not(None):
                    Tensor.append(self.I_train[i_tensor])
                if self.I_val is not(None):
                    Tensor.append(self.I_val[i_tensor])
                if self.I_test is not(None):
                    Tensor.append(self.I_test[i_tensor])
                I.append(np.concatenate(Tensor,axis=0))
            return I
    
    @property
    def I_train(self):
        if self.data_train is not(None):
            return [np.concatenate([meas[2][0] for meas in self.data_train],axis=0)]
        else:
            return None
    
    @property
    def I_val(self):
        if self.data_val is not(None):
            return [np.concatenate([meas[2][0] for meas in self.data_val],axis=0)]
        else:
            return None
    
    @property
    def I_test(self):
        if self.data_test is not(None):
            return [np.concatenate([meas[2][0] for meas in self.data_test],axis=0)]
        else:
            return None
    
    @property
    def I_valid(self):
        if self.I_train is None and self.I_val is None and self.I_test is None:
            return None
        else:
            I_valid = []
            for i_tensor in range(1):
                Tensor = []
                if self.I_train_valid is not(None):
                    Tensor.append(self.I_train_valid[i_tensor])
                if self.I_val_valid is not(None):
                    Tensor.append(self.I_val_valid[i_tensor])
                if self.I_test_valid is not(None):
                    Tensor.append(self.I_test_valid[i_tensor])
                I_valid.append(np.concatenate(Tensor,axis=0))
            return I_valid
    
    @property
    def I_train_valid(self):
        if self.data_train is not(None):
            I_train_valid = []
            for tensor in self.I_train:
                I_train_valid.append(tensor[self.I_train_idx,:])
            return I_train_valid
        else:
            return None
    
    @property
    def I_val_valid(self):
        if self.data_val is not(None):
            I_val_valid = []
            for tensor in self.I_val:
                I_val_valid.append(tensor[self.I_val_idx,:])
            return I_val_valid
        else:
            return None
    
    @property
    def I_test_valid(self):
        if self.data_test is not(None):
            I_test_valid = []
            for tensor in self.I_test:
                I_test_valid.append(tensor[self.I_test_idx,:])
            return I_test_valid
        else:
            return None
    
    @property
    def I_idx(self):
        if self.data_train is not(None) or self.data_val is not(None) or self.data_test is not(None):
            return np.where(self.I[0])[0]
        else:
            return None
    
    @property
    def I_train_idx(self):
        if self.data_train is not(None):
            return np.where(self.I_train[0])[0]
        else:
            return None
    
    @property
    def I_val_idx(self):
        if self.data_val is not(None):
            return np.where(self.I_val[0])[0]
        else:
            return None
        
    @property
    def I_test_idx(self):
        if self.data_test is not(None):
            return np.where(self.I_test[0])[0]
        else:
            return None
    
    @property
    def X_train_valid(self):
        if self.data_train is not(None):
            X_train_valid = []
            for tensor in self.X_train:
                X_train_valid.append(tensor[self.I_train_idx,:])
            return X_train_valid
        else:
            return None
    
    @property
    def X_val_valid(self):
        if self.data_val is not(None):
            X_val_valid = []
            for tensor in self.X_val:
                X_val_valid.append(tensor[self.I_val_idx,:])
            return X_val_valid
        else:
            return None
        
    @property
    def X_test_valid(self):
        if self.data_test is not(None):
            X_test_valid = []
            for tensor in self.X_test:
                X_test_valid.append(tensor[self.I_test_idx,:])
            return X_test_valid
        else:
            return None
    
    @property
    def X_valid(self):
        if self.data_train is not(None) or self.data_val is not(None) or self.data_test is not(None):
            X_valid = []
            for tensor in self.X:
                X_valid.append(tensor[self.I_idx,:])
            return X_valid
        else:
            return None
    
    @property
    def Y_train_valid(self):
        if self.data_train is not(None):
            Y_train_valid = []
            for tensor in self.Y_train:
                Y_train_valid.append(tensor[self.I_train_idx,:])
            return Y_train_valid
        else:
            return None
    
    @property
    def Y_val_valid(self):
        if self.data_val is not(None):
            Y_val_valid = []
            for tensor in self.Y_val:
                Y_val_valid.append(tensor[self.I_val_idx,:])
            return Y_val_valid
        else:
            return None
    
    @property
    def Y_test_valid(self):
        if self.data_test is not(None):
            Y_test_valid = []
            for tensor in self.Y_test:
                Y_test_valid.append(tensor[self.I_test_idx,:])
            return Y_test_valid
        else:
            return None
    
    @property
    def Y_valid(self):
        if self.data_train is not(None) or self.data_val is not(None) or self.data_test is not(None):
            Y_valid = []
            for tensor in self.Y:
                Y_valid.append(tensor[self.I_idx,:])
            return Y_valid
        else:
            return None
    
    @property
    def X_train_valid_scaled(self):
        if self.data_train is not(None):
            X_train_valid_scaled = []
            for tensor in self.X_train_scaled:
                X_train_valid_scaled.append(tensor[self.I_train_idx,:])
            return X_train_valid_scaled
        else:
            return None
    
    @property
    def X_val_valid_scaled(self):
        if self.data_val is not(None):
            X_val_valid_scaled = []
            for tensor in self.X_val_scaled:
                X_val_valid_scaled.append(tensor[self.I_val_idx,:])
            return X_val_valid_scaled
        else:
            return None
        
    @property
    def X_test_valid_scaled(self):
        if self.data_test is not(None):
            X_test_valid_scaled = []
            for tensor in self.X_test_scaled:
                X_test_valid_scaled.append(tensor[self.I_test_idx,:])
            return X_test_valid_scaled
        else:
            return None
    
    @property
    def X_valid_scaled(self):
        if self.data_train is not(None) or self.data_val is not(None) or self.data_test is not(None):
            X_valid_scaled = []
            for tensor in self.X_scaled:
                X_valid_scaled.append(tensor[self.I_idx,:])
            return X_valid_scaled
        else:
            return None
    
    @property
    def Y_train_valid_scaled(self):
        if self.data_train is not(None):
            Y_train_valid_scaled = []
            for tensor in self.Y_train_scaled:
                Y_train_valid_scaled.append(tensor[self.I_train_idx,:])
            return Y_train_valid_scaled
        else:
            return None
    
    @property
    def Y_val_valid_scaled(self):
        if self.data_val is not(None):
            Y_val_valid_scaled = []
            for tensor in self.Y_val_scaled:
                Y_val_valid_scaled.append(tensor[self.I_val_idx,:])
            return Y_val_valid_scaled
        else:
            return None
    
    @property
    def Y_test_valid_scaled(self):
        if self.data_test is not(None):
            Y_test_valid_scaled = []
            for tensor in self.Y_test_scaled:
                Y_test_valid_scaled.append(tensor[self.I_test_idx,:])
            return Y_test_valid_scaled
        else:
            return None
    
    @property
    def Y_valid_scaled(self):
        if self.data_train is not(None) or self.data_val is not(None) or self.data_test is not(None):
            Y_valid_scaled = []
            for tensor in self.Y_scaled:
                Y_valid_scaled.append(tensor[self.I_idx,:])
            return Y_valid_scaled
        else:
            return None

    @property
    def X_scaled(self):
        if self.X_train is None and self.X_val is None and self.X_test is None:
            return None
        else:
            X_scaled = []
            for i_tensor in range(self.n_X):
                Tensor = []
                if self.X_train_scaled is not(None):
                    Tensor.append(self.X_train_scaled[i_tensor])
                if self.X_val_scaled is not(None):
                    Tensor.append(self.X_val_scaled[i_tensor])
                if self.X_test_scaled is not(None):
                    Tensor.append(self.X_test_scaled[i_tensor])
                X_scaled.append(np.concatenate(Tensor,axis=0))
            return X_scaled
    
    @property
    def X_train_scaled(self):
        if self.X_train is not(None) and self.X_scaler is not(None):
            X_train_scaled = self._get_scaled_2d_arrays(self.X_scaler,self.X_train)
            return X_train_scaled
        else:
            return None
    
    @property
    def X_val_scaled(self):
        if self.X_val is not(None) and self.X_scaler is not(None):
            X_val_scaled = self._get_scaled_2d_arrays(self.X_scaler,self.X_val)
            return X_val_scaled
        else:
            return None
    
    @property
    def X_test_scaled(self):
        if self.X_test is not(None) and self.X_scaler is not(None):
            X_test_scaled = self._get_scaled_2d_arrays(self.X_scaler,self.X_test)
            return X_test_scaled
        else:
            return None
    
    @property
    def Y_scaled(self):
        if self.Y_train is None and self.Y_val is None and self.Y_test is None:
            return None
        else:
            Y_scaled = []
            for i_tensor in range(self.n_X):
                Tensor = []
                if self.Y_train_scaled is not(None):
                    Tensor.append(self.Y_train_scaled[i_tensor])
                if self.Y_val_scaled is not(None):
                    Tensor.append(self.Y_val_scaled[i_tensor])
                if self.Y_test_scaled is not(None):
                    Tensor.append(self.Y_test_scaled[i_tensor])
                Y_scaled.append(np.concatenate(Tensor,axis=0))
            return Y_scaled
    
    @property
    def Y_train_scaled(self):
        if self.Y_train is not(None) and self.Y_scaler is not(None):
            Y_train_scaled = self._get_scaled_2d_arrays(self.Y_scaler,self.Y_train)
            return Y_train_scaled
        else:
            return None
    
    @property
    def Y_val_scaled(self):
        if self.Y_val is not(None) and self.Y_scaler is not(None):
            Y_val_scaled = self._get_scaled_2d_arrays(self.Y_scaler,self.Y_val)
            return Y_val_scaled
        else:
            return None
    
    @property
    def Y_test_scaled(self):
        if self.Y_test is not(None) and self.Y_scaler is not(None):
            Y_test_scaled = self._get_scaled_2d_arrays(self.Y_scaler,self.Y_test)
            return Y_test_scaled
        else:
            return None
    
    @property
    def X_mean(self):
        if self.X_scaler is not(None):
            return [sc.mean_ for sc in self.X_scaler]
        else:
            return None
    
    @property
    def X_scaler(self):
        return self._X_scaler
    
    @X_scaler.setter
    def X_scaler(self, scaler, fit_scaler=True):
        self._X_scaler = scaler
        if fit_scaler:
            self._fit_X_scaler()
    
    @property
    def Y_scaler(self):
        return self._Y_scaler
    
    @Y_scaler.setter
    def Y_scaler(self, scaler, fit_scaler=True):
        self._Y_scaler = scaler
        if fit_scaler:
            self._fit_Y_scaler()
    
    @property
    def X_scale(self):
        if self.X_scaler is not(None):
            return [sc.scale_ for sc in self.X_scaler]
        else:
            return None
    
    @property
    def Y_mean(self):
        if self.Y_scaler is not(None):
            return [sc.mean_ for sc in self.Y_scaler]
        else:
            return None
    
    @property
    def Y_scale(self):
        if self.Y_scaler is not(None):
            return [sc.scale_ for sc in self.Y_scaler]
        else:
            return None
    
    @property
    def n_meas(self):
        return len(self.data_train+self.data_val+self.data_test)
    
    @property
    def n_meas_train(self):
        return len(self.data_train)
    
    @property
    def n_meas_val(self):
        return len(self.data_val)
    
    @property
    def n_meas_test(self):
        return len(self.data_test)
    
    @property
    def n_X(self):
        if self.data_train is not(None):
            return len(self.data_train[0][0])
        elif self.data_val is not(None):
            return len(self.data_val[0][0])
        elif self.data_test is not(None):
            return len(self.data_test[0][0])
        else:
            return None
    
    @property
    def n_Y(self):
        if self.data_train is not(None):
            return len(self.data_train[0][1])
        elif self.data_val is not(None):
            return len(self.data_val[0][1])
        elif self.data_test is not(None):
            return len(self.data_test[0][1])
        else:
            return None
    
    @property
    def n_samples(self):
        n_train = self.n_train if self.n_train is not(None) else 0
        n_val = self.n_val if self.n_val is not(None) else 0
        n_test = self.n_test if self.n_test is not(None) else 0
        return n_train+n_val+n_test
    
    @property
    def n_train_list(self):
        if self.data_train is not(None):
            return np.array([d[0][0].shape[0] for d in self.data_train])
        else:
            return None
    
    @property
    def n_val_list(self):
        if self.data_val is not(None):
            return np.array([d[0][0].shape[0] for d in self.data_val])
        else:
            return None
    
    @property
    def n_test_list(self):
        if self.data_test is not(None):
            return np.array([d[0][0].shape[0] for d in self.data_test])
        else:
            return None
    
    @property
    def n_train(self):
        if self.data_train is not(None):
            return np.sum(self.n_train_list)
        else:
            return None

    @property
    def n_val(self):
        if self.data_val is not(None):
            return np.sum(self.n_val_list)
        else:
            return None

    @property
    def n_test(self):
        if self.data_test is not(None):
            return np.sum(self.n_test_list)
        else:
            return None
 
    @property
    def n_features(self):
        if self.X_train is not(None):
            return [X_.shape[1] for X_ in self.X_train]
        elif self.X_val is not(None):
            return [X_.shape[1] for X_ in self.X_val]
        elif self.X_test is not(None):
            return [X_.shape[1] for X_ in self.X_test]
        else:
            return None
    
    @property
    def n_outputs(self):
        if self.Y_train is not(None):
            return [Y_.shape[1] for Y_ in self.Y_train]
        elif self.Y_val is not(None):
            return [Y_.shape[1] for Y_ in self.Y_val]
        elif self.Y_test is not(None):
            return [Y_.shape[1] for Y_ in self.Y_test]
        else:
            return None
    
    
class SPDatasetPlotter():
    '''
    Plotter for SPDataset Object.
    
    # Arguments
        SPDataset:  SPDataset for Plotting
    
    # Functions
        plot_dataset
        
    '''
    def __init__(self,SPDataset=None):
        self.SPDataset = SPDataset
    
    def _plot_dataset(self,X,Y,I,plot_X=True,plot_Y=True,X_legend_entries=None,Y_legend_entries=None,downsample=1,sharex=True,plot_legend=True,mark_invalid=False):
        # Time Vector
        dt = self.SPDataset.dt
        if self.SPDataset.dt is None:
            dt = 1
        t = np.arange(0,np.int(np.ceil(X[0].shape[1]/downsample)))*dt*downsample
        # Dimensions
        n_sp_row = np.max([len(X),len(Y)])
        n_sp_col = np.sum([plot_X,plot_Y])
        # Get valid indices
        Inval_idx = np.where(I[0][0,::downsample,0]==0)
        # Create Figure
        plt.figure()
        # Plot X
        spx=[]
        if plot_X:
            for i_X_curr,X_curr in enumerate(X):
                if plot_Y:
                    spx_=plt.subplot(n_sp_row,n_sp_col,(i_X_curr+1)*2-1)
                else:
                    spx_=plt.subplot(n_sp_row,n_sp_col,(i_X_curr+1))
                spx.append(spx_)
                plt.plot(t,X_curr[0,::downsample,:])
                plt.ylabel('Feature')
                if self.SPDataset.dt is not(None):
                    plt.xlabel('Time t [s]')
                else:
                    plt.xlabel('Timestep k')
                if X_legend_entries is not(None) and plot_legend:
                    plt.legend(X_legend_entries[i_X_curr])
                plt.grid()
        # Plot Y
        spy=[]
        if plot_Y:
            for i_Y_curr,Y_curr in enumerate(Y):
                sharedaxis = spx[i_Y_curr] if sharex and plot_X else None
                if plot_X:
                    spy_=plt.subplot(n_sp_row,n_sp_col,(i_Y_curr+1)*2,sharex=sharedaxis)
                else:
                    spy_=plt.subplot(n_sp_row,n_sp_col,(i_Y_curr+1),sharex=sharedaxis)
                spy.append(spy_)
                plt.plot(t,Y_curr[0,::downsample,:])
                if mark_invalid:
                    plt.plot(t[Inval_idx],Y_curr[0,::downsample,:][Inval_idx],'o',color='red')
                plt.ylabel('Feature')
                if self.SPDataset.dt is not(None):
                    plt.xlabel('Time t [s]')
                else:
                    plt.xlabel('Timestep k')
                if Y_legend_entries is not(None) and plot_legend:
                    plt.legend(Y_legend_entries[i_Y_curr])
                plt.grid()
    
    def _plot_scatter(self,sig1,sig2,name1=None,name2=None,marker='o',alpha=0.5):
        plt.figure()
        plt.plot(sig1,sig2,marker,alpha=alpha)
        plt.xlabel(name1)
        plt.ylabel(name2)
        plt.grid()
    
    def _plot_heatmap(self,sig1,sig2,name1=None,name2=None,bins=(100,100),cmap='inferno',log=False,density=False):
        # Get bins
        from matplotlib import colors
        H,xedges,yedges = np.histogram2d(sig1,sig2,bins=bins,density=density)
        # Meshgrid
        X, Y = np.meshgrid(xedges, yedges)
        # Plot
        fig = plt.figure()
        ax = plt.subplot(111)
        im = ax.pcolormesh(X, Y, H.T, norm=colors.SymLogNorm(linthresh=0.03, linscale=0.03, vmin=0.1, vmax=np.max(H)), cmap=cmap)
        plt.xlabel(name1)
        plt.ylabel(name2)
        fig.colorbar(im,ax=ax)
    
    def plot_dataset(self,dataset='all',plot_X=True,plot_Y=True,plot_legend=True,sharex=True,downsample=1,scaled_X=False,scaled_Y=False,indices=None,pick_signals_X=None,pick_signals_Y=None,mark_invalid=False,zero_inval_Y=False):
        # Legend Entries
        X_legend_entries = self.SPDataset._get_legend_entries(tensor='X',scaled=scaled_X,pick_signals=pick_signals_X)
        Y_legend_entries = self.SPDataset._get_legend_entries(tensor='Y',scaled=scaled_Y,pick_signals=pick_signals_Y)
        # Choose Datset + Mapping
        X,Y,I = self.SPDataset.get_3D_data(dataset,scaled_X=scaled_X,scaled_Y=scaled_Y,indices=indices,pick_signals_X=pick_signals_X,pick_signals_Y=pick_signals_Y,zero_inval_Y=zero_inval_Y)
        # Plot Data Set
        self._plot_dataset(X,Y,I,plot_X,plot_Y,X_legend_entries,Y_legend_entries,downsample=downsample,sharex=sharex,plot_legend=plot_legend,mark_invalid=mark_invalid)
    
    def plot_scatter(self,dataset='all',tensor_axis_1=['X',0],tensor_axis_2=['X',0],signal_axis_1=0,signal_axis_2=0,scaled_axis_1=False,scaled_axis_2=False,indices=None,marker='o',alpha=0.5):
        # Get Signal Names from Legend Entries - Axis 1
        signal_name_axis_1 = self.SPDataset._get_legend_entry(tensor=tensor_axis_1,signal=signal_axis_1,scaled=scaled_axis_1)
        signal_name_axis_2 = self.SPDataset._get_legend_entry(tensor=tensor_axis_2,signal=signal_axis_2,scaled=scaled_axis_2)
        # Choose Datset + Mapping
        signal_1 = self.SPDataset._get_signal_from_tensor(dataset=dataset,tensor=tensor_axis_1,signal=signal_axis_1,indices=indices,scaled=scaled_axis_1)
        signal_2 = self.SPDataset._get_signal_from_tensor(dataset=dataset,tensor=tensor_axis_2,signal=signal_axis_2,indices=indices,scaled=scaled_axis_2)
        # Plot
        self._plot_scatter(sig1=signal_1,sig2=signal_2,name1=signal_name_axis_1,name2=signal_name_axis_2,marker=marker,alpha=alpha)
    
    def plot_heatmap(self,dataset='all',tensor_axis_1=['X',0],tensor_axis_2=['X',0],signal_axis_1=0,signal_axis_2=0,scaled_axis_1=False,scaled_axis_2=False,indices=None,bins=(1000,1000),cmap='inferno',log=False,density=False):
        # Get Signal Names from Legend Entries - Axis 1
        signal_name_axis_1 = self.SPDataset._get_legend_entry(tensor=tensor_axis_1,signal=signal_axis_1,scaled=scaled_axis_1)
        signal_name_axis_2 = self.SPDataset._get_legend_entry(tensor=tensor_axis_2,signal=signal_axis_2,scaled=scaled_axis_2)
        # Choose Datset + Mapping
        signal_1 = self.SPDataset._get_signal_from_tensor(dataset=dataset,tensor=tensor_axis_1,signal=signal_axis_1,indices=indices,scaled=scaled_axis_1)
        signal_2 = self.SPDataset._get_signal_from_tensor(dataset=dataset,tensor=tensor_axis_2,signal=signal_axis_2,indices=indices,scaled=scaled_axis_2)
        # Plot
        self._plot_heatmap(sig1=signal_1[:,0],sig2=signal_2[:,0],name1=signal_name_axis_1,name2=signal_name_axis_2,bins=bins,cmap=cmap,log=log,density=density)
    
    def plot_distribution(self,dataset='all',bins=50,plotX=True,plotY=True,normalize=True):
        # Get Histograms
        hX, hY = self.SPDataset._get_histogram(dataset=dataset,bins=bins,normalize=normalize)
        # Plot Hisograms
        if plotX:
            plt.figure()
            for i_X, h_ in enumerate(hX):
                axX = plt.subplot(self.SPDataset.n_X,1,i_X+1)
                axX.set_yscale('log')
                for h_sig_ in h_:
                    h_count = h_sig_[0] if not(normalize) else h_sig_[2]
                    h_base = (h_sig_[1][1:]+h_sig_[1][:-1])/2
                    axX.plot(h_base,h_count)
                axX.legend(self.SPDataset.X_signal_names[i_X])
                axX.grid()
        # Plot Hisograms
        if plotY:
            plt.figure()
            for i_Y, h_ in enumerate(hY):
                axY = plt.subplot(self.SPDataset.n_Y,1,i_Y+1)
                axY.set_yscale('log')
                for h_sig_ in h_:
                    h_count = h_sig_[0] if not(normalize) else h_sig_[2]
                    h_base = (h_sig_[1][1:]+h_sig_[1][:-1])/2
                    axY.plot(h_base,h_count)
                axY.legend(self.SPDataset.Y_signal_names[i_Y])
                axY.grid()
        # Title
        plt.title('Disbtibution')
        if normalize:
            plt.ylabel('Density')
        else:
            plt.ylabel('Count')
        plt.xlabel('Value')
                
    def plot_trainvaltest_distribution(self,bins=50,plotX=True,plotY=True,relative=True):
        # Get Histograms
        hX_train, hY_train = self.SPDataset._get_histogram(dataset='train',bins=bins)
        hX_val, hY_val   = self.SPDataset._get_histogram(dataset='val',bins=bins)
        hX_test, hY_test  = self.SPDataset._get_histogram(dataset='test',bins=bins)
#        # Plot Hisograms
#        if plotX:
#            plt.figure()
#            axX = plt.subplot(1,1,1)
#            axX.set_yscale('log')
#            for i_X, h_ in enumerate(hX):
#                for h_sig_ in h_:
#                    h_count = h_sig_[0]
#                    h_base = (h_sig_[1][1:]+h_sig_[1][:-1])/2
#                    axX.plot(h_base,h_count)
#                axX.legend(self.SPDataset.X_signal_names[i_X])
#                axX.grid()
        # Plot Hisograms
        if plotY:
            plt.figure()
            axY_ref = plt.subplot(self.SPDataset.n_Y,self.SPDataset.n_outputs[0],1)
            # Loop over Datasets
            for i_D,hY in enumerate([hY_train,hY_val,hY_test]):
                # Loop over Output Tensors
                for i_Y, h_ in enumerate(hY):
                    # Loop over Signals
                    for i_sig, h_sig_ in enumerate(h_):
                        # Get subplot
                        i_sp = self.SPDataset.n_outputs[0] * i_Y + i_sig + 1
                        axY = plt.subplot(self.SPDataset.n_Y,self.SPDataset.n_outputs[0],i_sp,sharey=axY_ref) if i_sp>1 else axY_ref
                        # Plot
                        h_count = h_sig_[2] if relative else h_sig_[0]
                        h_base = (h_sig_[1][1:]+h_sig_[1][:-1])/2
                        axY.plot(h_base,h_count)
                        # Axes Properties
                        axY.set_yscale('log')
                        axY.legend(['train','val','test'])
                        axY.grid()
                        # Axes
                        if self.SPDataset.Y_signal_names is not(None) and self.SPDataset.Y_signal_units is not(None):
                            plt.xlabel(self.SPDataset.Y_signal_names[i_Y][i_sig] + ' [' + self.SPDataset.Y_signal_units[i_Y][i_sig] + ']')
                        elif self.SPDataset.Y_signal_names is not(None):
                            plt.xlabel(self.SPDataset.Y_signal_names[i_Y][i_sig])
                        if i_sig==0:
                            if relative:
                                axY.set_ylabel('Probability Density [-]')
                            else:
                                axY.set_ylabel('Number of Samples [-]')
        
class SPTimeSeriesGenerator(Sequence):
    """Class takes in a sequence of data-points gathered at
    equal intervals, along with time series parameters such as
    stride, length of history, etc., to produce batches for
    training/validation.

    # Arguments
        data: List of numpy arrays (2d) with data points.
        flag_3d_data[Boolean]: Size equals number of input arrays. If flag[i] = True, input array i will be transformed to a 3d time series array
        targets: Targets corresponding to timesteps in data. It should have same length as data.
        flag_3d_targets[Boolean]: Size equals number of target arrays. If flag[i] = True, target array i will be transformed to a 3d time series array
        end_of_file: data is a sequence of datafiles. end_of_file is 1, when a new file start. In the 3d array you have
                    to look back only on data of the same file.
        train_param: Struct with the following argument:
            look back: Length of the output sequences (in number of timesteps).
            sampling_rate: Period between successive individual timesteps
            stride: Period between successive output sequences.
                For stride `s`, consecutive output samples would
                be centered around `data[i]`, `data[i+s]`, `data[i+2*s]`, etc.
            start_index: Data points earlier than `start_index` will not be used
                in the output sequences. This is useful to reserve part of the
                data for test or validation.
            end_index: Data points later than `end_index` will not be used
                in the output sequences. This is useful to reserve part of the
                data for test or validation.
            shuffle: Whether to shuffle output samples,
                or instead draw them in chronological order.
            reverse: Boolean: if `true`, timesteps in each output sample will be
                in reverse chronological order.
            batch_size: Number of timeseries samples in each batch
                (except maybe the last one).

    # Returns
        A time series generator

    # Example:
    train_generator = SSMTimeSeriesGenerator([data_nn_train_scaled, data_info_train], [True, False], # DATA
                                         [data_ref_train[:, 0], data_ref_train[:, 1], data_ref_train[:, 2], # TARGET 1, 2, 3
                                          np.roll(data_nn_train_scaled, shift=-train_param.PREDICT_STEPS, axis=0)],  # TARGET 4, Shift for prediction
                                         [False, False, False, False],
                                         data_EOF_array, train_param.LOOK_BACK, train_param.BATCH_SIZE)
    """

    def __init__(self, data, flag_3d_data, targets, flag_3d_targets, look_back, batch_size, seq2seq_prediction):
        self.data = self.conv_array_2_list(data)
        self.data = self.add_2nd_dim(self.data)
        self.end_index = len(self.data[0]) - 1

        self.targets = self.conv_array_2_list(targets)
        self.targets = self.add_2nd_dim(self.targets)

        self.flag_3d_data = self.conv_array_2_list(flag_3d_data)
        self.flag_3d_targets = self.conv_array_2_list(flag_3d_targets)
        
        self.seq2seq_prediction = seq2seq_prediction
        
        if any(flag_3d_targets[:]) or any(flag_3d_data[:]):
            self.look_back = look_back
            self.start_index = self.look_back
        else:
            self.start_index = 0
            self.look_back = 0

        self.end_index = len(self.data[0]) - 1
        self.batch_size = batch_size

        if len(self.data) != len(self.flag_3d_data):
            raise ValueError('Number of Input-Data and 3d-Flags have to be' +
                             ' of same length. '
                             'Number of input arrays {}'.format(len(self.data)) +
                             ' while flag-length is {}'.format(len(self.flag_3d_data)))
        if len(self.targets) != len(self.flag_3d_targets):
            raise ValueError('Number of Target-Data and 3d-Flags have to be' +
                             ' of same length. '
                             'Number of target arrays {}'.format(len(self.targets)) +
                             ' while flag-length is {}'.format(len(self.flag_3d_targets)))


        if len(self.data[0]) != len(self.targets[0]):
            raise ValueError('Data and targets have to be' +
                             ' of same length. '
                             'Data length is {}'.format(len(data[0])) +
                             ' while target length is {}'.format(len(targets[0])))

        if self.start_index > self.end_index:
            raise ValueError('`start_index+length=%i > end_index=%i` '
                             'is disallowed, as no part of the sequence '
                             'would be left to be used as current step.'
                             % (self.start_index, self.end_index))

    def __len__(self):
        return (self.end_index - self.start_index + self.batch_size) // self.batch_size

    def __getitem__(self, index):
        if index > ((len(self.data[0])-self.look_back)//self.batch_size) + 1:
            raise ValueError('Index for data generator is larger than maximum number of Batches')
#        print('getting item....')
        i = self.start_index + self.batch_size * index
        rows = np.arange(i, min(i + self.batch_size, self.end_index), 1)  # rows for output
        data_list = []
        target_list = []
        for flag_3d, data in zip(self.flag_3d_data, self.data):
            data = self.get_n_dim_array(data, flag_3d, rows)
            data_list.append(data)
        data_list = self.add_2nd_dim(data_list)

        for flag_3d, target in zip(self.flag_3d_targets, self.targets):
            target = self.get_n_dim_array(target, flag_3d, rows)
            target_list.append(target)
        target_list = self.add_2nd_dim(target_list)
        
        # If Not Sequence to Sequence, Take Last Element of I and Y
        if not(self.seq2seq_prediction):
            data_list[-1] = data_list[-1][:,[-1],:]
            target_list = [t_[:,[-1],:] for t_ in target_list]
#        print(len(target_list))
#        print([t_.shape for t_ in target_list])
        
        return data_list, target_list

# HELP FUNCTIONS #####################################################################
    def get_3d_data(self, data, rows):
        # Relevant slice for the batch => Create 3d time series array
        data_slice = data[rows[0] - self.look_back:rows[-1], :]
        # Reshape with stride tricks as a "sliding window"
        data_strides = data_slice.strides
        batch_shape = (len(rows), self.look_back, data_slice.shape[-1])
        batch_strides = (data_strides[0], data_strides[0], data_strides[1])
        return as_strided(data_slice, batch_shape, batch_strides, writeable=False)  # 185 times faster than 3d indexing

    def add_2nd_dim (self, data):
        if isinstance(data, list):
            for idx, array in enumerate(data):
                if len(array.shape) == 1:
                    data[idx] = np.expand_dims(array, axis=1)
        else:
            if len(data.shape) == 1:
                data = np.expand_dims(data, axis=1)
        return data

    def get_n_dim_array(self, data, flag_3d, rows):
        if flag_3d:
            data = self.get_3d_data(data, rows)  # build 3d
        else:
            data = data[rows - 1, :]  # build 2d
        return data

    def conv_array_2_list(self, obj):
        if not isinstance(obj, list):
            obj = [obj]
        return obj

