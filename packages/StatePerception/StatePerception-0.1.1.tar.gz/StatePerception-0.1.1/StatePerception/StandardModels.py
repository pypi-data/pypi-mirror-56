"""
@author: Torben Gräber
"""

# Keras and Tensorflow Imports
from keras.layers import Input, Dense, Dropout, GRU, Multiply, Flatten, CuDNNGRU
from keras.layers import Lambda, Add, Concatenate, Reshape
from keras.layers import GaussianDropout
from keras.layers import Softmax
from keras.callbacks import ReduceLROnPlateau
from keras import regularizers
from keras.optimizers import Adam
from keras import backend as K

import numpy as np

# Custom Imports
from .Model import SPModel
from .KerasLayer import mean_squared_error_convtime100, DerivativeLayer, mse_conv100_w2, BetaFromVyVx, ConstantNormalizationLayer

#class SP_SSE_Gra18(SPModel):
#    
#    def __init__(self,n_features,n_outputs,name='SSE_Gra18',custom_objects={'mean_squared_error_convtime100':mean_squared_error_convtime100},settings={'loss':mean_squared_error_convtime100,'metrics':[mean_squared_error_convtime100],'opt':Adam,'n_dense':50,'n_gru':10,'activation':'relu','drop_in':0,'drop':0,'l1_reg':0},settings_opt={'lr':0.01}):
#        # Init Super
#        super().__init__(n_features=n_features,n_outputs=n_outputs,name=name,custom_objects=custom_objects,settings=settings,settings_opt=settings_opt,num_gpus=num_gpus)
#        # Model
#        self.model_inputs_outputs = self.build_graph(settings)
#        self.models, self.models_gpu = self.build_models()
#        
#    def build_graph(self,settings):
#        # Inputs
#        inputs_X = Input(batch_shape=(None,None,self.n_features[0]))
#        inputs_I = Input(batch_shape=(None,None,1))
#        # Keras Core Model
#        inputs_drop = Dropout(settings['drop_in'])(inputs_X)
#        l1 = Dense(settings['n_dense'],activation=settings['activation'],kernel_regularizer=regularizers.l1(settings['l1_reg']))(inputs_drop)
#        l1_drop = Dropout(settings['drop'])(l1)
#        l4 = GRU(settings['n_gru'],return_sequences=True,kernel_regularizer=regularizers.l1(settings['l1_reg']))(l1_drop)
#        l4_drop = Dropout(settings['drop'])(l4)
#        prediction = Dense(self.n_outputs[0],activation='linear',kernel_regularizer=regularizers.l1(settings['l1_reg']))(l4_drop)
#        # Multiply Invalid Data Points with Zero
#        prediction_valid = Multiply()([prediction,inputs_I])
#        # Return Tensors
#        Inputs=[inputs_X,inputs_I]
#        Outputs0=[prediction_valid]
#        Inputs1=[inputs_X]
#        Outputs1=[prediction]
#        return [[Inputs,Outputs0],[Inputs1,Outputs1]]
#
#class SP_SSE_Gra18_ActReg(SPModel):
#    
#    def __init__(self,n_features,n_outputs,name='SSE_Gra18',custom_objects={'mean_squared_error_convtime100':mean_squared_error_convtime100},settings={'loss':mean_squared_error_convtime100,'metrics':[mean_squared_error_convtime100],'opt':Adam,'n_dense':50,'n_gru':10,'activation':'relu','drop_in':0,'drop':0,'l1_reg':0,'l2_reg_activation':0.0001},settings_opt={'lr':0.01},num_gpus=None):
#        # Init Super
#        super().__init__(n_features=n_features,n_outputs=n_outputs,name=name,custom_objects=custom_objects,settings=settings,settings_opt=settings_opt,num_gpus=num_gpus)
#        # Model
#        self.model_inputs_outputs = self.build_graph(settings)
#        self.models, self.models_gpu = self.build_models()
#        
#    def build_graph(self,settings):
#        # Inputs
#        inputs_X = Input(batch_shape=(None,None,self.n_features[0]))
#        inputs_I = Input(batch_shape=(None,None,1))
#        # Keras Core Model
#        inputs_drop = Dropout(settings['drop_in'])(inputs_X)
#        l1 = Dense(settings['n_dense'],activation=settings['activation'],kernel_regularizer=regularizers.l1(settings['l1_reg']))(inputs_drop)
#        l1_drop = Dropout(settings['drop'])(l1)
#        l4 = GRU(settings['n_gru'],return_sequences=True,kernel_regularizer=regularizers.l1(settings['l1_reg']))(l1_drop)
#        l4_drop = Dropout(settings['drop'])(l4)
#        prediction = Dense(self.n_outputs[0],activation='linear',kernel_regularizer=regularizers.l1(settings['l1_reg']))(l4_drop)
#        prediction_pp = DerivativeLayer(dt=0.01,order=2,factor=settings['l2_reg_activation'])(prediction)
#        # Multiply Invalid Data Points with Zero
#        prediction_valid = Multiply()([prediction,inputs_I])
#        # Return Tensors
#        Inputs=[inputs_X,inputs_I]
#        Outputs0=[prediction_valid,prediction_pp]
#        Inputs1=[inputs_X]
#        Outputs1=[prediction]
#        return [[Inputs,Outputs0],[Inputs1,Outputs1]]
#
#class SP_SSE_Gra18_ActReg_InitState(SPModel):
#    
#    def __init__(self,n_features,n_outputs,name='SSE_Gra18',custom_objects={'mean_squared_error_convtime100':mean_squared_error_convtime100},settings={'loss':mean_squared_error_convtime100,'metrics':[mean_squared_error_convtime100],'opt':Adam,'n_dense':100,'n_gru':20,'activation':'relu','drop_in':0,'drop':0,'l1_reg':0.0001,'l2_reg_activation':0.0001},settings_opt={'lr':0.001},settings_init={'feed_init_state':False,'init_batch_size':1},num_gpus=None):
#        # Init Super
#        super().__init__(n_features=n_features,n_outputs=n_outputs,name=name,custom_objects=custom_objects,settings=settings,settings_opt=settings_opt,settings_init=settings_init,num_gpus=num_gpus)
#        # Model
#        self.model_inputs_outputs = self.build_graph()
#        self.models, self.models_gpu = self.build_models()
#        
#    def build_graph(self):
#        # Inputs
#        if self.settings_init['feed_init_state']:
#            inputs_X = Input(batch_shape=(self.settings_init['init_batch_size'],None,self.n_features[0]))
#            inputs_I = Input(batch_shape=(self.settings_init['init_batch_size'],None,1))
#        else:
#            inputs_X = Input(batch_shape=(None,None,self.n_features[0]))
#            inputs_I = Input(batch_shape=(None,None,1))
#        # Keras Core Model
#        inputs_drop = Dropout(self.settings['drop_in'])(inputs_X)
#        l1 = Dense(self.settings['n_dense'],activation=self.settings['activation'],kernel_regularizer=regularizers.l1(self.settings['l1_reg']))(inputs_drop)
#        l1_drop = Dropout(self.settings['drop'])(l1)
#        if self.num_gpus is not(None):
#            l4 = GRU(self.settings['n_gru'],return_sequences=True,kernel_regularizer=regularizers.l1(self.settings['l1_reg']),stateful=self.settings_init['feed_init_state'])(l1_drop)
#        else:
#            l4 = GRU(self.settings['n_gru'],return_sequences=True,kernel_regularizer=regularizers.l1(self.settings['l1_reg']),stateful=self.settings_init['feed_init_state'])(l1_drop)
#        l4_drop = Dropout(self.settings['drop'])(l4)
#        prediction = Dense(self.n_outputs[0],activation='linear',kernel_regularizer=regularizers.l1(self.settings['l1_reg']))(l4_drop)
#        prediction_pp = DerivativeLayer(dt=0.01,order=2,factor=self.settings['l2_reg_activation'])(prediction)
#        # Multiply Invalid Data Points with Zero
#        prediction_valid = Multiply()([prediction,inputs_I])
#        # Return Tensors
#        Inputs=[inputs_X,inputs_I]
#        Inputs1=[inputs_X]
#        Outputs0=[prediction_valid,prediction_pp]
#        Outputs1=[prediction]
#        return [[Inputs,Outputs0],[Inputs1,Outputs1]]

class SP_SSE_Gra18_ActReg_InitState_WeightedLoss(SPModel):
    
    def __init__(self,n_features,n_outputs,name='SSE_Gra18',custom_objects={'mean_squared_error_convtime100':mean_squared_error_convtime100},settings={'loss':[[mse_conv100_w2,'mse'],[mse_conv100_w2]],'metrics':[mean_squared_error_convtime100],'opt':Adam,'n_dense':100,'n_gru':20,'activation':'relu','drop_in':0,'drop':0,'l1_reg':0.00001,'l2_reg_activation':0.00001},settings_opt={'lr':0.001},settings_init={'feed_init_state':False,'init_batch_size':1},additional_fit_args={'callbacks':[ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=50, verbose=1, cooldown=100)]},num_gpus=None):
        # Init Super
        super().__init__(n_features=n_features,n_outputs=n_outputs,name=name,custom_objects=custom_objects,settings=settings,settings_opt=settings_opt,settings_init=settings_init,num_gpus=num_gpus,additional_fit_args=additional_fit_args)
        # Model
        self.model_inputs_outputs = self.build_graph()
        self.models, self.models_gpu = self.build_models()
        
    def build_graph(self):
        # Inputs
        if self.settings_init['feed_init_state']:
            inputs_X = Input(batch_shape=(self.settings_init['init_batch_size'],None,self.n_features[0]))
            inputs_I = Input(batch_shape=(self.settings_init['init_batch_size'],None,1))
        else:
            inputs_X = Input(batch_shape=(None,None,self.n_features[0]))
            inputs_I = Input(batch_shape=(None,None,1))
        # Keras Core Model
        inputs_drop = GaussianDropout(self.settings['drop_in'])(inputs_X)
        l1 = Dense(self.settings['n_dense'],activation=self.settings['activation'],kernel_regularizer=regularizers.l1(self.settings['l1_reg']))(inputs_drop)
        l1_drop = GaussianDropout(self.settings['drop'])(l1)
        if self.num_gpus is not(None):
            l4 = CuDNNGRU(self.settings['n_gru'],return_sequences=True,kernel_regularizer=regularizers.l1(self.settings['l1_reg']),stateful=self.settings_init['feed_init_state'])(l1_drop)
        else:
            l4 = GRU(self.settings['n_gru'],return_sequences=True,kernel_regularizer=regularizers.l1(self.settings['l1_reg']),stateful=self.settings_init['feed_init_state'])(l1_drop)
        l4_drop = GaussianDropout(self.settings['drop'])(l4)
        prediction = Dense(self.n_outputs[0],activation='linear',kernel_regularizer=regularizers.l1(self.settings['l1_reg']))(l4_drop)
        prediction_pp = DerivativeLayer(dt=0.01,order=2,factor=self.settings['l2_reg_activation'])(prediction)
        # Multiply Invalid Data Points with Zero
        prediction_valid = Multiply()([prediction,inputs_I])
        # Return Tensors
        Inputs=[inputs_X,inputs_I]
        Inputs1=[inputs_X]
        Outputs0=[prediction_valid,prediction_pp]
        Outputs1=[prediction]
        return [[Inputs,Outputs0],[Inputs1,Outputs1]]

class SP_SSE_Gra18_ActReg_InitState_WeightedLoss_AddOutputBeta(SPModel):
    
    def __init__(self,n_features,n_outputs,request_scaled_data=False,name='SSE_Gra18',custom_objects={'mean_squared_error_convtime100':mean_squared_error_convtime100},settings={'loss':[[mse_conv100_w2,mean_squared_error_convtime100,'mse'],[mse_conv100_w2,mean_squared_error_convtime100]],'metrics':[mean_squared_error_convtime100],'opt':Adam,'n_dense':100,'n_gru':20,'activation':'relu','drop_in':0,'drop':0,'l1_reg':0.00001,'l2_reg_activation':0.00001},settings_opt={'lr':0.00001},settings_init={'feed_init_state':False,'init_batch_size':1},additional_fit_args={'callbacks':[]},num_gpus=None):
        # Init Super
        super().__init__(n_features=n_features,n_outputs=n_outputs,request_scaled_data=request_scaled_data,name=name,custom_objects=custom_objects,settings=settings,settings_opt=settings_opt,settings_init=settings_init,num_gpus=num_gpus,additional_fit_args=additional_fit_args)
        # Model
        self.model_inputs_outputs = self.build_graph()
        self.models, self.models_gpu = self.build_models()
        
    def build_graph(self):
        # Inputs
        if self.settings_init['feed_init_state']:
            inputs_X = Input(batch_shape=(self.settings_init['init_batch_size'],None,self.n_features[0]))
            inputs_I = Input(batch_shape=(self.settings_init['init_batch_size'],None,1))
        else:
            inputs_X = Input(batch_shape=(None,None,self.n_features[0]))
            inputs_I = Input(batch_shape=(None,None,1))
        # Keras Core Model
        inputs_drop = GaussianDropout(self.settings['drop_in'])(inputs_X)
        l1 = Dense(self.settings['n_dense'],activation=self.settings['activation'],kernel_regularizer=regularizers.l1(self.settings['l1_reg']))(inputs_drop)
        l1_drop = GaussianDropout(self.settings['drop'])(l1)
        if self.num_gpus is not(None):
            l4 = CuDNNGRU(self.settings['n_gru'],return_sequences=True,kernel_regularizer=regularizers.l1(self.settings['l1_reg']),stateful=self.settings_init['feed_init_state'])(l1_drop)
        else:
            l4 = GRU(self.settings['n_gru'],return_sequences=True,kernel_regularizer=regularizers.l1(self.settings['l1_reg']),stateful=self.settings_init['feed_init_state'])(l1_drop)
        l4_drop = GaussianDropout(self.settings['drop'])(l4)
        # Predictinos
        prediction_pre = Dense(self.n_outputs[0],activation='linear',kernel_regularizer=regularizers.l1(self.settings['l1_reg']))(l4_drop)
        prediction_pre = ConstantNormalizationLayer(scale=np.array([1,2.5]),position='output')(prediction_pre)
#        prediction_pre_unscaled = ConstantNormalizationLayer(scale=self.vxy_scale,mean=self.vxy_mean,position='output')(prediction_pre)
        # Add Mean Wheel Speeds to v_x prediction
        dvx = Lambda(lambda x: K.expand_dims(x[:,:,0],axis=2))(prediction_pre)
        vy  = Lambda(lambda x: K.expand_dims(x[:,:,1],axis=2))(prediction_pre)
        mean_wheelspeeds = Lambda(lambda x: K.expand_dims(K.mean(x[:,:,4:8],axis=2),axis=2))(inputs_X)
        vx = Add()([mean_wheelspeeds,dvx])
        prediction = Concatenate(name='vxy')([vx,vy])
        # Calculate Side Slip Angle
        beta = BetaFromVyVx(name='beta')(prediction)
        # Derivative of Prediction
        prediction_pp = DerivativeLayer(dt=0.01,order=2,factor=self.settings['l2_reg_activation'],name='vxypp')(prediction)
        # Multiply Invalid Data Points with Zero
        prediction_valid = Multiply(name='vxy_v')([prediction,inputs_I])
        beta_valid = Multiply(name='beta_v')([beta,inputs_I])
        # Return Tensors
        Inputs0=[inputs_X,inputs_I]
        Inputs1=[inputs_X]
        Outputs0=[prediction_valid,beta_valid,prediction_pp]
        Outputs1=[prediction,beta]
        return [[Inputs0,Outputs0],[Inputs1,Outputs1]]

#class SP_SSE_Gra18_2X_2Y(SPModel):
#    
#    def __init__(self,n_features,n_outputs,name='SSE_Gra18',custom_objects={'mean_squared_error_convtime100':mean_squared_error_convtime100},settings={'loss':mean_squared_error_convtime100,'metrics':[mean_squared_error_convtime100],'opt':Adam,'lr':0.01,'n_dense':50,'n_gru':10,'activation':'relu','drop_in':0,'drop':0,'l1_reg':0}):
#        # Init Super
#        super().__init__(n_features=n_features,n_outputs=n_outputs,name=name,custom_objects=custom_objects,settings=settings)
#        # Model
#        self.model_inputs_outputs = self.build_graph(settings)
#        self.models, self.models_gpu = self.build_models()
#        
#    def build_graph(self,settings):
#        # Inputs
#        inputs_X1 = Input(batch_shape=(None,None,self.n_features[0]))
#        inputs_X2 = Input(batch_shape=(None,None,self.n_features[1]))
#        inputs_X = Concatenate()([inputs_X1,inputs_X2])
#        inputs_I = Input(batch_shape=(None,None,1))
#        # Keras Core Model
#        inputs_drop = Dropout(settings['drop_in'])(inputs_X)
#        l1 = Dense(settings['n_dense'],activation=settings['activation'],kernel_regularizer=regularizers.l1(settings['l1_reg']))(inputs_drop)
#        l1_drop = Dropout(settings['drop'])(l1)
#        l4 = GRU(settings['n_gru'],return_sequences=True,kernel_regularizer=regularizers.l1(settings['l1_reg']))(l1_drop)
#        l4_drop = Dropout(settings['drop'])(l4)
#        prediction1 = Dense(self.n_outputs[0],activation='linear',kernel_regularizer=regularizers.l1(settings['l1_reg']))(l4_drop)
#        prediction2 = Dense(self.n_outputs[1],activation='linear',kernel_regularizer=regularizers.l1(settings['l1_reg']))(l4_drop)
#        # Multiply Invalid Data Points with Zero
#        prediction_valid1 = Multiply()([prediction1,inputs_I])
#        prediction_valid2 = Multiply()([prediction2,inputs_I])
#        # Return Tensors
#        Inputs=[inputs_X1,inputs_X2,inputs_I]
#        Outputs0=[prediction_valid1,prediction_valid2]
#        Inputs1=[inputs_X1,inputs_X2]
#        Outputs1=[prediction1,prediction2]
#        return [[Inputs,Outputs0],[Inputs1,Outputs1]]

class SP_WindowedFeedForward(SPModel):
    
    def __init__(self,n_features,n_outputs,name='SSE_WindowedFF',request_scaled_X=True,request_scaled_Y=True,seq2seq_prediction=False,settings={'loss':['mse'],'metrics':['mse'],'opt':Adam,'window_length':100,'n_dense':50,'activation':'relu','drop_in':0,'drop':0,'l1_reg':0.0001},settings_opt={'lr':0.001},settings_init=None,additional_fit_args={},custom_objects=None,num_gpus=None):
        # Init Super
        super().__init__(n_features=n_features,n_outputs=n_outputs,request_scaled_X=request_scaled_X,request_scaled_Y=request_scaled_Y,seq2seq_prediction=seq2seq_prediction,name=name,custom_objects=custom_objects,settings=settings,settings_opt=settings_opt,settings_init=settings_init,num_gpus=num_gpus,additional_fit_args=additional_fit_args)
        # Model
        self.model_inputs_outputs = self.build_graph(settings)
        self.models, self.models_gpu = self.build_models()
        
    def build_graph(self,settings):
        # Inputs
        inputs_X = Input(batch_shape=(None,self.settings['window_length'],self.n_features[0]))
        inputs_I = Input(batch_shape=(None,1,1))
        # Keras Core Model
        inputs_flat = Flatten()(inputs_X)
        inputs_drop = Dropout(settings['drop_in'])(inputs_flat)
        l = Dense(settings['n_dense'],activation=settings['activation'],kernel_regularizer=regularizers.l1(settings['l1_reg']))(inputs_drop)
        l_drop = Dropout(settings['drop'])(l)
        prediction = Dense(self.n_outputs[0],activation='linear',kernel_regularizer=regularizers.l1(settings['l1_reg']))(l_drop)
        # Multiply Invalid Data Points with Zero
        prediction_valid = Multiply()([prediction,inputs_I])
        # Return Tensors
        Inputs0=[inputs_X,inputs_I]
        Outputs0=[prediction_valid]
        Inputs1=[inputs_X]
        Outputs1=[prediction]
        return [[Inputs0,Outputs0],[Inputs1,Outputs1]]

class SP_WindowedFeedForward_Classifier(SPModel):
    
    def __init__(self,n_features,n_outputs,name='SSE_WindowedFF_Class',request_scaled_X=False,request_scaled_Y=False,seq2seq_prediction=False,settings={'loss':['categorical_crossentropy'],'metrics':['categorical_crossentropy'],'opt':Adam,'window_length':100,'n_dense':[50],'activation':'relu','drop_in':0,'drop':0,'l1_reg':0.0001},settings_opt={'lr':0.001},settings_init=None,additional_fit_args={},custom_objects=None,num_gpus=None):
        # Init Super
        super().__init__(n_features=n_features,n_outputs=n_outputs,request_scaled_X=request_scaled_X,request_scaled_Y=request_scaled_Y,seq2seq_prediction=seq2seq_prediction,name=name,custom_objects=custom_objects,settings=settings,settings_opt=settings_opt,settings_init=settings_init,num_gpus=num_gpus,additional_fit_args=additional_fit_args)
        # Model
        self.model_inputs_outputs = self.build_graph(settings)
        self.models, self.models_gpu = self.build_models()
        
    def build_graph(self,settings):
        # Inputs
        inputs_X = Input(batch_shape=(None,self.settings['window_length'],self.n_features[0]))
        inputs_I = Input(batch_shape=(None,1,1))
        # Keras Core Model
        inputs_flat = Flatten()(inputs_X)
        l_drop = Dropout(settings['drop_in'])(inputs_flat)
        for n_dense in settings['n_dense']:
            l = Dense(n_dense,activation=settings['activation'],kernel_regularizer=regularizers.l1(settings['l1_reg']))(l_drop)
            l_drop = Dropout(settings['drop'])(l)
        prediction = Dense(self.n_outputs[0],activation='linear',kernel_regularizer=regularizers.l1(settings['l1_reg']))(l_drop)
        prediction = Softmax()(prediction)
        # Multiply Invalid Data Points with Zero
        #inputs_I = Flatten()(inputs_I)
        prediction_valid = Multiply()([prediction,inputs_I])
        # Return Tensors
        Inputs0=[inputs_X,inputs_I]
        Outputs0=[prediction_valid]
        Inputs1=[inputs_X]
        Outputs1=[prediction]
        return [[Inputs0,Outputs0],[Inputs1,Outputs1]]