"""
@author: Torben Gräber
"""

# Imports
import numpy as np
import matplotlib.pyplot as plt
import GPyOpt

# Keras and Tensorflow Imports
from keras.callbacks import ModelCheckpoint

# Custom Imports
from .StatePerceptionHelperFunctions import ensure_dir, get_color_setup
from .StatePerceptionHelperFunctions import save_pickle_file, load_pickle_file

# Function and Class Definitions
class SPModelTrainer():
    '''
    Training Process
    Hyperparameter Optimization with GPyOpt
    Fit, Error and other Evaluation Plots
    '''
    def __init__(self,SPModel,SPDataset,name=None):
        self.name = name
        self.SPModel = SPModel
        self.SPDataset = SPDataset
        self.training_history = SPTrainingHistory()
        
    def save_training_history(self,savename=None):
        savename = savename if savename else self.name +'/'+ 'SPOptHist.pkl'
        savelist = [self.training_history]
        save_pickle_file(savename,savelist)
    
    def load_training_history(self,savename=None):
        savename = savename if savename else self.name +'/'+ 'SPOptHist.pkl'
        [self.training_history] = load_pickle_file(savename)
    
    def fit_model(self,timesteps=None,shift=None,batch_size=None,set_measurement_transition_invalid=False,discard_invalid=False,**fit_args):
        # Get Training Data
        X_train, Y_train, I_train = self.SPDataset.get_3D_data(dataset='train',
                                                               scaled_X=self.SPModel.request_scaled_X,
                                                               scaled_Y=self.SPModel.request_scaled_Y,
                                                               timesteps=timesteps,
                                                               shift=shift,
                                                               set_measurement_transition_invalid=set_measurement_transition_invalid,
                                                               seq2seq_prediction=self.SPModel.seq2seq_prediction,
                                                               discard_invalid=discard_invalid)
        # Get Validation Data
        validation_data = None
        if self.SPDataset.X_val is not(None):
            X_val, Y_val, I_val = self.SPDataset.get_3D_data(dataset='val',
                                                             scaled_X=self.SPModel.request_scaled_X,
                                                             scaled_Y=self.SPModel.request_scaled_Y,
                                                             timesteps=timesteps,
                                                             shift=shift,
                                                             seq2seq_prediction=self.SPModel.seq2seq_prediction,
                                                             discard_invalid=discard_invalid)
            validation_data = [[*X_val,*I_val],[*Y_val]]
        # Fit Model
        if self.SPModel.num_gpus is not(None):
            new_history = self.SPModel.models_gpu[0].fit([*X_train,*I_train],[*Y_train],
                                                         validation_data=validation_data,
                                                         batch_size=batch_size,
                                                         **self.SPModel.additional_fit_args,**fit_args).history
        else:
            new_history = self.SPModel.models[0].fit([*X_train,*I_train],[*Y_train],
                                                     validation_data=validation_data,
                                                     batch_size=batch_size,
                                                     **self.SPModel.additional_fit_args,**fit_args).history
        # Append History
        self.training_history._append_history(new_history)
    
    def fit_model_generator(self,timesteps=None,batch_size=None,set_measurement_transition_invalid=False,**fit_generator_args):
        # Get Training Generator
        spgenerator = self.SPDataset.get_timeseries_generator(timesteps,batch_size,
                                                              dataset='train',
                                                              scaled_X=self.SPModel.request_scaled_X,
                                                              scaled_Y=self.SPModel.request_scaled_Y,
                                                              seq2seq_prediction=self.SPModel.seq2seq_prediction)
        spgenerator_val = self.SPDataset.get_timeseries_generator(timesteps,
                                                                  batch_size,dataset='val',
                                                                  scaled_X=self.SPModel.request_scaled_X,
                                                                  scaled_Y=self.SPModel.request_scaled_Y,
                                                                  seq2seq_prediction=self.SPModel.seq2seq_prediction)
        # Fit Model
        if self.SPModel.num_gpus is not(None):
            new_history = self.SPModel.models_gpu[0].fit_generator(generator=spgenerator,
                                                                   validation_data=spgenerator_val,
                                                                   **self.SPModel.additional_fit_args,
                                                                   **fit_generator_args).history
        else:
            new_history = self.SPModel.models[0].fit_generator(generator=spgenerator,
                                                               validation_data=spgenerator_val,
                                                               **self.SPModel.additional_fit_args,
                                                               **fit_generator_args).history
        # Append History
        self.training_history._append_history(new_history)
    
    def _export_fit_to_mat(self,y_true,y_pred):
        print('Not implemented yet.')
    
    def show_fit(self,model=0,dataset='val',output_tensors='all',timesteps=None,downsample=1,unscale_data=False,indices=None,export_fit=False,zero_inval_Y=False):
        # Check Inputs
        matching_timesteps_for_seq2seq = timesteps or self.SPModel.seq2seq_prediction
        assert matching_timesteps_for_seq2seq
        # Get Data
        X, Y, I = self.SPDataset.get_3D_data(dataset=dataset,
                                             scaled_X=self.SPModel.request_scaled_X,
                                             scaled_Y=self.SPModel.request_scaled_Y,
                                             timesteps=timesteps,
                                             shift=1,
                                             indices=indices,
                                             seq2seq_prediction=self.SPModel.seq2seq_prediction,
                                             zero_inval_Y=zero_inval_Y)
        # Predict
        print('Predicting ...')
        if model==0:
            y_pred = self.SPModel.predict([*X,*I])
        elif model==1:
            y_pred = self.SPModel.predict([*X],submodel=model)
        else:
            raise ValueError('Only model == 1 or model == 0 supported.')
        # Unscale Prediction
        if unscale_data and self.SPModel.request_scaled_Y:
            Y = self.SPDataset._unscale_Y(Y)
            y_pred = self.SPDataset._unscale_Y(y_pred)
        # Output Tensors
        if output_tensors=='all':
            output_tensors=np.arange(0,len(y_pred))
        # Export Fit
        if export_fit:
            self._export_fit_to_mat(y_true=Y,y_pred=y_pred)
        # Plot
        print('Plotting ...')
        for i_Y in output_tensors:
            # Plot
            dt = self.SPDataset.dt
            if self.SPDataset.dt is None:
                dt = 1
            if dataset == 'train':
                n = self.SPDataset.n_train
            elif dataset == 'val':
                n = self.SPDataset.n_val
            elif dataset == 'test':
                n = self.SPDataset.n_test
            else:
                print('Invalid data set choice.')
            Y_curr = Y[i_Y]#np.concatenate([*Y],axis=2)
            y_pred_curr = y_pred[i_Y]
            Y_signal_names = []
            for name in self.SPDataset.Y_signal_names:
                Y_signal_names = Y_signal_names + name
            plt.figure()
            sp = plt.subplot(Y_curr.shape[2],1,1)
            for i in range(Y_curr.shape[2]):
                if i>0:
                    plt.subplot(Y_curr.shape[2],1,i+1,sharex=sp)
                if timesteps is None:
                    t = np.arange(0,np.int(np.ceil(n/downsample)))*dt*downsample
                    plt.plot(t,Y_curr[0,::downsample,i],label=Y_signal_names[i])
                    plt.plot(t,y_pred_curr[0,::downsample,i])
                else:
                    t = np.arange(0,np.int(np.ceil(Y_curr.shape[0]/downsample)))*dt*downsample
                    plt.plot(t,Y_curr[::downsample,-1,i],label=Y_signal_names[i])
                    plt.plot(t,y_pred_curr[::downsample,-1,i],label='estimate')
                plt.ylabel('Output')
                if self.SPDataset.Y_signal_names is not(None):
                    plt.legend()
                if self.SPDataset.dt is not(None):
                    plt.xlabel('Time t [s]')
                else:
                    plt.xlabel('Timestep k')
                plt.title('Fit Plot - Data Set: ' + dataset)
                plt.grid()
    
    def show_error_plot(self,dataset='val',output_tensors='all',timesteps=None,downsample=1,unscale_data=False,indices=None):
        # Check Inputs
        matching_timesteps_for_seq2seq = timesteps or self.SPModel.seq2seq_prediction
        assert matching_timesteps_for_seq2seq
        # Get Data
        X, Y, I = self.SPDataset.get_3D_data(dataset=dataset,
                                             scaled_X=self.SPModel.request_scaled_X,
                                             scaled_Y=self.SPModel.request_scaled_Y,
                                             timesteps=timesteps,
                                             shift=1,
                                             indices=indices,
                                             seq2seq_prediction=self.SPModel.seq2seq_prediction)
        # Predict
        print('Predicting ...')
        y_pred = self.SPModel.predict([*X,*I])
        # Unscale Prediction
        if unscale_data and self.SPModel.request_scaled_Y:
            Y = self.SPDataset._unscale_Y(Y)
            y_pred = self.SPDataset._unscale_Y(y_pred)
        # Output Tensors
        if output_tensors=='all':
            output_tensors=np.arange(0,len(y_pred))
        # Plot
        print('Plotting ...')
        for i_Y in output_tensors:
            # Plot
            dt = self.SPDataset.dt
            if self.SPDataset.dt is None:
                dt = 1
            if dataset == 'train':
                n = self.SPDataset.n_train
            elif dataset == 'val':
                n = self.SPDataset.n_val
            elif dataset == 'test':
                n = self.SPDataset.n_test
            else:
                print('Invalid data set choice.')
            Y_curr = Y[i_Y]#np.concatenate([*Y],axis=2)
            y_pred_curr = y_pred[i_Y]
            Y_signal_names = []
            for name in self.SPDataset.Y_signal_names:
                Y_signal_names = Y_signal_names + name
            plt.figure()
            sp = plt.subplot(Y_curr.shape[2],1,1)
    
    def show_training_curves(self,metric=0):
        keys = self.training_history.get_history_keys()
        if len(keys)==0:
            raise ReferenceError('No history available.')
        # Get Name of Metric
        if type(metric) is str:
            metric_name = metric
        else:
            metric_names = keys
            metric_name = metric_names[metric]
        # Prepare Plot
        plt.figure()
        axtrain=plt.subplot(1,1,1)
        plt.title('Training Curves')
        plt.ylabel('Error')
        # Plot
        axtrain.semilogy(self.training_history.history[metric_name],label='training')
        axtrain.semilogy(self.training_history.history['val_'+metric_name],label='validation')
        plt.legend()
        plt.grid()
    
    def _f_GPyOpt_construct_function_arguments(self,x):
        # Function Arguments
        model_arguments = self.SPModel._funargs[0]
        if 'self' in model_arguments.keys():
            del model_arguments['self']
        # Get Hyperparameters
        hyperparam_fixed = self.training_history.GPyOpt_fixed_param
        hyperparam_bounds = self.training_history.GPyOpt_bounds
        # Map Parameters from settings
        for hyperpar,val in hyperparam_fixed.items():
            if hyperpar in model_arguments['settings'].keys():
                 model_arguments['settings'][hyperpar] = val
            elif hyperpar in model_arguments['settings_opt'].keys():
                 model_arguments['settings_opt'][hyperpar] = val
        x_names = []
        for hyperpar,val in zip(hyperparam_bounds,x[0]):
            if hyperpar['name'] in model_arguments['settings'].keys():
                model_arguments['settings'][hyperpar['name']] = val
                x_names.append(hyperpar['name'])
            elif hyperpar['name'] in model_arguments['settings_opt'].keys():
                model_arguments['settings_opt'][hyperpar['name']] = val
                x_names.append(hyperpar['name'])
        return model_arguments, x_names
    
    def _f_GPyOpt_model_name(self,model_name,x):
        # Get Hyperparameters
        hyperparam_bounds = self.training_history.GPyOpt_bounds
        # Construct Model Names
        savename = model_name if model_name is not(None) else 'Model'
        for hyperpar,val in zip(hyperparam_bounds,x[0]):
            savename = savename + '_' + hyperpar['name'] + '{:1.5f}'.format(val)
        savename = savename.replace('.','p') + '.spm'
        return savename
    
    def _f_GPyOpt(self,x):
        # Function Arguments
        model_arguments, x_names = self._f_GPyOpt_construct_function_arguments(x)
        # Create and Initialize Model
        modelobj = type(self.SPModel)
        spmodel = modelobj(**model_arguments)
        # Get Target
        target_train = spmodel.get_metric_names()[self._GPyOpt_target]
        target_val = 'val_'+spmodel.get_metric_names()[self._GPyOpt_target]
        #self._GPyOpt_target_name_list.append(spmodel.get_metric_names()[self._GPyOpt_target])
        print('Target is {:s}'.format(target_val))
        # Create Callbacks
        savename = self._f_GPyOpt_model_name(spmodel.name,x)
        path = self.name+'/'+self._GPyOpt_savepath if self.name else self._GPyOpt_savepath
        ensure_dir(path)
        savename_full = path+'/'+savename
        callbacks=[ModelCheckpoint(savename_full, monitor=target_val, save_best_only=True)]#,save_weights_only=True)]
        # Fit Model
        sptrainer = SPModelTrainer(SPModel=spmodel,SPDataset=self.SPDataset)
        if self._fit_generator:
            sptrainer.fit_model_generator(**self._GPyOpt_fit_args,callbacks=callbacks)
        else:
            sptrainer.fit_model(**self._GPyOpt_fit_args,callbacks=callbacks)
        # Calculate Loss on Val
        minimum_val_loss = np.min(sptrainer.training_history.history[target_val])
        # Save Results
        self._GPyOpt_min_val_loss.append(minimum_val_loss)
        self.training_history._append_GPyOpt(model_arguments,
                                             history=sptrainer.training_history.history,
                                             target_train=target_train,
                                             target_val=target_val,
                                             minimum_val_loss=minimum_val_loss,
                                             savepath=path,
                                             savename=savename,
                                             x_names=x_names,
                                             x=x)
        # Return Minimum of Val Loss for Optimization
        return minimum_val_loss
        
    def hyperparam_search_init(self,hyperparam_bounds,hyperparam_fixed=None,target=0,GPyOpt_fit_args={},savepath='hyperpar_opt',initial_design_numdata=1,fit_generator=False):
        '''
        Optimizes the Hyperparameters of the SPModel for minimum validation error.
        
        # Arguments

        '''
        # Ensure Results Dir
        self._GPyOpt_savepath = savepath
        ensure_dir(savepath)
        # Get Constructer Arguments of SPModel
        self.training_history.GPyOpt_bounds = hyperparam_bounds
        self.training_history.GPyOpt_fixed_param = hyperparam_fixed
        # Fit Method Preparation
        self._GPyOpt_target = target
        self._GPyOpt_fit_args = GPyOpt_fit_args
        self._fit_generator = fit_generator
        # Summaries and other Saves
        self._GPyOpt_min_val_loss = []
        # Create GPyOpt Optimizer
        self._GPyOpt_opt = GPyOpt.methods.BayesianOptimization(f=self._f_GPyOpt, domain=hyperparam_bounds, initial_design_numdata=initial_design_numdata)
    
    def hyperparam_search_run(self,max_iter=10):
        # Run Optimization
        self._GPyOpt_opt.run_optimization(max_iter=max_iter)

    def _load_optimal_weights(self):
        for model in self.SPModel.models:
            model.load_weights(self.training_history.GPyOpt['best_run'][-1]['model'])#,by_name=True)
    
    def get_optimal_spmodel(self):
        # Load Optimal Model Weights from Checkpoint
        self._load_optimal_weights()
        return self.SPModel
        
    def show_hyperparam_training_curves(self,semilogy=True):
        '''
        Visualization of a performed hyperparam_search().
        '''
        # Color Setup
        colour_start = np.array([27, 79, 114])/256
        colour_end = np.array([235, 245, 251])/256
        num_colours = len(self.training_history.GPyOpt['runs'])
        colors = get_color_setup(colour_start,colour_end,num_colours)
        # Plot
        plt.figure()
        axtrain=plt.subplot(2,1,1)
        plt.title('Training Curves')
        plt.ylabel('Training Error')
        axval=plt.subplot(2,1,2,sharex=axtrain)
        plt.ylabel('Validation Error')
        plt.xlabel('Epochs [-]')
        for run_,color in zip(self.training_history.GPyOpt['runs'],colors):
            if semilogy:
                axtrain.semilogy(run_['history'][run_['target_train']],color=color)
                axval.semilogy(run_['history'][run_['target_val']],color=color)
            else:
                axtrain.plot(run_['history'][run_['target_train']],color=color)
                axval.plt(run_['history'][run_['target_val']],color=color)
        axtrain.legend([run_['target_train']])
        axval.legend([run_['target_val']])
        axtrain.grid()
        axval.grid()
    
    def show_2d_optimization(self):
        print('Not implemented yet.')


class SPTrainingHistory():
    
    def __init__(self):
        self.history = {}
        self.GPyOpt = {'hyperparam_bounds':[],'hyperparam_fixed':[],'summaries':[], 'runs':[], 'best_run':[], 'savepath':[]}
        print(' ')
    
    def get_history_keys(self):
        return list(self.history.keys())
    
    def _append_history(self,new_history):
        # Assert Matching History Keys
        nhkeys = new_history.keys()
        ohkeys = self.get_history_keys()
        assert len(nhkeys)==len(ohkeys) or not(ohkeys)
        if ohkeys:
            for nhk in nhkeys:
                assert nhk in ohkeys
        # Append history
        for key in new_history.keys():
            self.history[key] = new_history[key] if self.history is not(None) else self.history[key] + new_history[key]
    
    def _append_GPyOpt(self,model_arguments,history,target_train,target_val,minimum_val_loss,savepath,savename,x_names,x):
        # Save Results
        self.GPyOpt['runs'].append({'target_train':target_train,
                                     'target_val':target_val,
                                     'minimum_val_loss':minimum_val_loss,
                                     'model':savepath+'/'+savename,
                                     'x_opt':x,
                                     'x_opt_names':x_names,
                                     'history':history,
                                     'model_arguments':model_arguments})
        # Document Best Model
        first_run = len(self.GPyOpt['best_run'])==0
        new_model_better = self.GPyOpt['best_run'][-1]['minimum_val_loss'] > minimum_val_loss if not(first_run) else True
        if new_model_better:
            self.GPyOpt['best_run'].append(self.GPyOpt['runs'][-1])
    
    @property
    def GPyOpt_target(self):
        return self.GPyOpt['target']
    
    @GPyOpt_target.setter
    def GPyOpt_target(self,target):
        self.GPyOpt['target'] = target
    
    @property
    def GPyOpt_bounds(self):
        return self.GPyOpt['hyperparam_bounds']
    
    @GPyOpt_bounds.setter
    def GPyOpt_bounds(self,bounds):
        self.GPyOpt['hyperparam_bounds'] = bounds
        
    @property
    def GPyOpt_fixed_param(self):
        return self.GPyOpt['hyperparam_fixed']

    @GPyOpt_fixed_param.setter
    def GPyOpt_fixed_param(self,param):
        self.GPyOpt['hyperparam_fixed'] = param
        