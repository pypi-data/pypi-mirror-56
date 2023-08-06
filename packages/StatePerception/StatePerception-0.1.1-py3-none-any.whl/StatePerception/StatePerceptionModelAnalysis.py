"""
@author: Torben Gräber
"""

# Imports
import numpy as np
import matplotlib.pyplot as plt
from .StatePerceptionHelperFunctions import get_color_setup_3_colours
from .StatePerceptionHelperFunctions import ensure_dir

# Keras and Tensorflow Imports
from keras import backend as K

# Function and Class Definitions
def bias_disturbance(intensity,tensor_to_disturb):
    disturbance = np.ones_like(tensor_to_disturb) * intensity
    return disturbance

class SPSensitivityAnalyzer():
    '''
    Sensitivity Analysis (error metric over input disturbance)
    Standard is to evaluate the sensitivity on the evaluation data set 'val'
    
    # Arguments
        SPModel:        State Perception Model to be analyzed
        SPDataset:      Dataset that the SPModel will be analyzed on
    '''
    def __init__(self,SPModel,SPDataset):
        self.SPModel = SPModel
        self.SPDataset = SPDataset
        self.sensitivities={'train':None,'val':None,'test':None}
        self.disturbed_predictions={'train':None,'val':None,'test':None}
    
    def _bias(self):
        print('Not implemented yet.')
    
    def perform_analysis(self,disturbance_fun=bias_disturbance,dataset='val',input_tensors='all',scale_intensities=None,num_intensities=7,save_predictions=False,verbose=True):
        '''
        Performs the Sensitivity Analysis to Specified Disturbances
        
        # Arguments
            dataset: The dataset that the analysis will be performed on. Options
                are 'train', 'val', 'test'.
            input_tensors: List with the indices of the input tensors to the
                State Perception Model SPModel. Alternative: Choose the option
                input_tensors='all' to perform the analysis on all of them.
            scale_intensities: The intensities of the disturbance can be scaled
                with this option.
            num_intensities: The number of disturbance intensities that are
                evaluated. The number of evaluations can be calculated as follows:
                num_eval = num_tensors * num_features_per_tensor * num_intensities
            verbose: Verbosity on/off
            
        # Writes to Object
            self.sensitivities[dataset]: Results of the analysis are saved here.
                List with sensitivities for each Input Tensor shape=(input_tensors)
                For each tensor sensitivities with shape=(feature,intensity,metric)
            self.disturbed_predictions[dataset]
                shape=(input_tensor,output_tensor)
                shape=(input_signal,intensity,batch,timestep,output_signal)
        
        '''
        # Print Info
        if verbose:
            print('Performing Sensitivity Analysis on Model {:s}'.format(self.SPModel.name))
        # Get Indices
        if input_tensors == 'all':
            input_tensors_c = []
            for i_X in range(self.SPDataset.n_X):
                input_tensors_c.append(np.arange(0,self.SPDataset.n_features[i_X]))
            input_tensors = input_tensors_c
        # Get Dataset (continuous prediction)
        X,Y,I = self.SPDataset.get_3D_data(dataset=dataset,timesteps=None,shift=None)
        # Calculate Intensities
        if scale_intensities is None:
            scale_intensities = []
            for i_X in range(self.SPDataset.n_X):
                scale_intensities.append(np.ones(shape=(self.SPDataset.n_features[i_X])))
        # Number of Metrics
        num_metrics = len(self.SPModel.models[0].metrics_names)
        # Instantiate Lists
        self._intensities_list = []
        self._evaluations_list = []
        if save_predictions:
            predictions_list = []
        # Loop over Input Tensors
        for i_X,list_input_signals in enumerate(input_tensors):
            # Print Info
            if verbose:
                print('   Input Tensor {:d} ...'.format(i_X))
            # Initialize Arrays
            intensities = np.zeros(shape=(self.SPDataset.n_features[i_X],num_intensities))
            evaluations = np.zeros(shape=(self.SPDataset.n_features[i_X],num_intensities,num_metrics))
            # Predictions are saved in list
            predictions = []
            if save_predictions:
                for i_Y in range(self.SPDataset.n_Y):
                    predictions.append(np.zeros(shape=(len(list_input_signals),num_intensities,Y[i_Y].shape[0],Y[i_Y].shape[1],Y[i_Y].shape[2])))
            # Loop over number of disturbance intensities
            for i_input_signal,idx_input_signal in enumerate(list_input_signals):
                # Calculate Intensities for current Signal in current Tensor
                scale_intensities_curr = scale_intensities[i_X][idx_input_signal]
                intensities_curr = np.arange(0,((num_intensities+1)/num_intensities)*scale_intensities_curr,scale_intensities_curr/(num_intensities-1)) - scale_intensities_curr/2
                intensities[idx_input_signal] = intensities_curr
                # Print Info
                if verbose:
                    print('      Input Feature {:d} ...'.format(idx_input_signal))
                # Loop over Disturbance Intensities
                for i_intensity,intensity in enumerate(intensities_curr):
                    # Get Disturbance
                    disturbance = disturbance_fun(intensity,X[i_X][:,:,idx_input_signal])
                    # Apply Disturbance
                    X_dist = np.copy(X)
                    X_dist[i_X][:,:,idx_input_signal] = X_dist[i_X][:,:,idx_input_signal] + disturbance
                    # Evaluate Model
                    eval_curr = self.SPModel.evaluate([*X_dist,*I],[*Y])
                    if save_predictions:
                        prediction_curr = self.SPModel.predict([*X_dist,*I])
#                        if self.SPDataset.n_Y==1:
#                            prediction_curr = np.expand_dims(prediction_curr,axis=0)
                        # Loop over Output Tensors
                        for i_Y in range(self.SPDataset.n_Y):
                            # Correct Shape if Prediction is Numpy Array
                            if type(prediction_curr)==np.ndarray:
                                if len(prediction_curr.shape)==2:
                                    prediction_curr = np.expand_dims(prediction_curr,axis=0)
                            # Correct Prediction if List of Numpy Arrays
                            if type(prediction_curr)==list:
                                if len(prediction_curr[i_Y].shape)==2:
                                    prediction_curr[i_Y] = np.expand_dims(prediction_curr[i_Y],axis=0)
                            # Write
                            predictions[i_Y][i_input_signal,i_intensity,:,:,:] = prediction_curr[i_Y]
                    # Save Results
                    evaluations[idx_input_signal,i_intensity,:] = eval_curr
                # Print Info
                if verbose:
                    print('   Sensitivity is: ' + str(eval_curr))
            self._intensities_list.append(intensities)
            self._evaluations_list.append(evaluations)
            if save_predictions:
                predictions_list.append(predictions)
        # Write Results
        self.sensitivities[dataset] = {'metrics_names':self.SPModel.models[0].metrics_names,'disturbed_channels':input_tensors,'intensities':self._intensities_list,'metrics':np.array(self._evaluations_list)}
        self.disturbed_predictions[dataset] = predictions_list
        # Print Info
        if verbose:
            print('Finished Sensitivity Analysis on Model {:s}'.format(self.SPModel.name))
    
    def plot_sensitivities(self,dataset='val',index_metric=0):
        disturbed_channels = self.sensitivities[dataset]['disturbed_channels']
        intensities = self.sensitivities[dataset]['intensities']
        metrics = self.sensitivities[dataset]['metrics']
        metric_name = self.sensitivities[dataset]['metrics_names'][index_metric]
        for i_X,(intensities_curr,metrics_curr,disturbed_channels_curr) in enumerate(zip(intensities,metrics,disturbed_channels)):
            plt.figure()
            plt.subplot(1,1,1)
            plt.title('Model {:s} - Sensitivity {:s} on Input Tensor {:d}'.format(self.SPModel.name,metric_name,i_X))
            plt.plot(intensities_curr[disturbed_channels_curr,:].transpose(),metrics_curr[disturbed_channels_curr,:,index_metric].transpose())
            plt.grid()
            plt.xlabel('Disturbance Intensity on Scaled Input')
            plt.ylabel('Performance Metric')
    
    def plot_disturbances(self,input_tensor,input_signal,dataset='val',legend_entries=True,unscale_data=True):
        # Colour Setup
        color_meas = np.array([169, 50, 38])/256
        colour_start = np.array([171, 178, 185])/256
        colour_mid = np.array([242, 243, 244])/256
        colour_end = np.array([171, 178, 185])/256
        # Data
        if dataset=='train':
            Y = self.SPDataset.Y_train_scaled
        if dataset=='val':
            Y = self.SPDataset.Y_val_scaled
        if dataset=='test':
            Y = self.SPDataset.Y_test_scaled
        # Rename
        i_X, idx_input_signal = input_tensor, input_signal
        i_input_signal = np.where(np.array(self.sensitivities[dataset]['disturbed_channels'][i_X])==idx_input_signal)[0]
        # Loop over Outputs
        for i_Y in range(self.SPDataset.n_Y):
            # One Figure for every Output Tensor
            plt.figure()
            # Loop over Output Signals
            for i_output_signal in range(self.SPDataset.n_outputs[i_Y]):
                # Get Prediction
                pred = self.disturbed_predictions[dataset][i_X][i_Y]
                # Scales
                scale_curr, mean_curr = 1, 0
                if unscale_data:
                    scale_curr, mean_curr = self.SPDataset.Y_scale[i_Y][i_output_signal], self.SPDataset.Y_mean[i_Y][i_output_signal]
                # Dimension
                n_intensities = pred.shape[1]
                # Create Time Vector
                t = np.arange(0,pred.shape[3])
                # Plot
                colours = get_color_setup_3_colours(colour_start,colour_mid,colour_end,n_intensities)
                ax1=plt.subplot(self.SPDataset.n_outputs[i_Y],1,i_output_signal+1)
                if i_output_signal==0:
                    plt.title('Predictions Output Tensor {:d}, Disturbance: Input Tensor {:d} / Signal {:d}'.format(i_Y,i_X,idx_input_signal))
                for i_intensity in range(n_intensities):
                    pred_curr = pred[i_input_signal,i_intensity,0,:,i_output_signal].transpose()
                    ax1.plot(t,pred_curr*scale_curr + mean_curr,color=colours[i_intensity])
                plt.plot(Y[i_Y][:,i_output_signal]*scale_curr + mean_curr,color=color_meas)
                plt.grid()
                plt.xlabel('Time [s]')
                plt.ylabel('Signal {:d}'.format(i_output_signal))
                if legend_entries is not(None):
                    Y_legend_entries = self.SPDataset._get_legend_entries(tensor='Y',scaled=not(unscale_data))
                    plt.legend([Y_legend_entries[i_output_signal]])
                

class SPConvergenceAnalysis():
    '''
    Convergence Analysis
    '''
    def __init__(self,SPModel,SPDataset,init_batch_size=100):
        self.SPModel = SPModel
        self.SPModel_init = self._get_SPModel_init()
        self.SPDataset = SPDataset
        # 
        self.init_batch_size = init_batch_size
    
    def _get_SPModel_init(self):
        # Instantiate Model
        funargs = self.SPModel._funargs[0]
        funargs['settings_init']['feed_init_state'] = True
        funargs['settings_init']['init_batch_size'] = 100
        if 'self' in funargs.keys():
            del funargs['self']
        # Create Model
        SPModel_init = type(self.SPModel)(**funargs)
        # Transfer Weights
        ensure_dir('temp')
        self.SPModel._save_weights(savename='temp/weight_transfer.w',submodel=0)
        SPModel_init._load_weights(savename='temp/weight_transfer.w',submodel=0)
        # Return Model
        return SPModel_init
        
    def perform_analysis(self,idx_layers_with_states=[4],intensity=1,dataset='val',timesteps=200,shift=200):
        self.y_pred = None
        self.y_ref = None
        # Get Data
        X,Y,I = self.SPDataset.get_3D_data(dataset=dataset,timesteps=timesteps,shift=shift)
        # Cut away batches to match batch_size
        X_ = []
        cut_away = np.mod(X[0].shape[0],self.init_batch_size)
        for X_curr in X:
            X_.append(X_curr[0:-cut_away,:,:])
        Y_ = []
        cut_away = np.mod(Y[0].shape[0],self.init_batch_size)
        for Y_curr in Y:
            Y_.append(Y_curr[0:-cut_away,:,:])
        I_ = []
        cut_away = np.mod(I[0].shape[0],self.init_batch_size)
        for I_curr in I:
            I_.append(I_curr[0:-cut_away,:,:])
        # Set Initial State
        for idx in idx_layers_with_states:
            dim = self.SPModel_init.models[0].layers[idx].states[0].shape.as_list()
            hidden_states=np.random.rand(*dim) * intensity
            K.set_value(self.SPModel_init.models[0].layers[idx].states[0], hidden_states)
        # Prediction
        pred = self.SPModel_init.predict([*X_,*I_],batch_size=self.init_batch_size)
        self.y_pred = pred
        self.y_ref  = Y_
        
    def show_results(self,output_tensor=0,signal=0):
        # Calculate Residuals
        residuals = self.y_ref[0][:,:,signal] - self.y_pred[0][:,:,signal]
        res_std = np.std(residuals,axis=0)
        # Plot
        plt.figure()
        plt.plot(residuals.transpose(),color='blue',alpha=0.01)
        plt.plot(res_std,color='black')
        plt.plot(-res_std,color='black')
        print('Not implemented yet.')
        