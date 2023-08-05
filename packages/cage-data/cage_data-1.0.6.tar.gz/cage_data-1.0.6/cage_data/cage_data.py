import numpy as np
import _pickle as pickle
import time
import h5py
import getpass
from .load_intan_rhd_format import read_data
from scipy import stats, signal
from .intanutil.notch_filter import notch_filter
from .brpylib import NevFile 

memo1 = """Since Blackrock Python codes (brpy) are too slow when reading .nev files, we use MATLAB version of .nev files instead."""
memo2 = """Please make sure MATLAB version of .nev files are in your target directory. """
class cage_data:
    def __init__(self):
        self.meta = dict()
        self.meta['Processes by'] = getpass.getuser()
        self.meta['Processes at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print('An empty cage_data object has been created.')
        print(memo1)
        print(memo2)
        
    def create(self, path, nev_mat_file, rhd_file, empty_channels, do_notch = 0):
        """
        'nev_mat_file' is the neural data file,
        'rhd_file' is the EMG data file
        """
        if path[-1] == '/':
            self.nev_mat_file = ''.join((path, nev_mat_file))
            self.rhd_file = ''.join((path, rhd_file))
        else:
            self.nev_mat_file = ''.join((path, '/', nev_mat_file))
            self.rhd_file = ''.join((path, '/', rhd_file))
        self.parse_nev_mat_file(self.nev_mat_file, empty_channels)
        try:
            self.date_num = int(rhd_file[:8])
            self.date_num = 0
        except ValueError:
            print('Check the file name of the .rhd file!')
        else:
            pass
        self.EMG_names, self.EMG_diff, self.EMG_timeframe = self.parse_rhd_file(self.rhd_file, do_notch)
        self.file_length = self.EMG_timeframe[-1]
        print(self.EMG_names)
        self.is_cortical_cleaned = False
        self.is_EMG_filtered = False
        self.is_data_binned = False
        self.is_spike_smoothed = False
        self.binned = {}
        self.pre_processing_summary()
        
    def pre_processing_summary(self):
        print('EMG filtered? -- %s' %(self.is_EMG_filtered))
        print('Cortical data cleaned? -- %s' %(self.is_cortical_cleaned))
        if hasattr(self, 'is_data_binned'):
            print('Data binned? -- %s' %(self.is_data_binned))
        if hasattr(self, 'is_spike_smoothed'):
            print('Spikes smoothed? -- %s' %(self.is_spike_smoothed))
    
    def parse_nev_mat_file(self, filename, empty_channels = []):
        """
        Parse MATLAB version of .nev files
        """
        s = time.clock()
        nev_file = h5py.File(filename)['NEV']
        ch_lbl = list(np.asarray(nev_file['elec_labels']).T)
        for i in range(len(ch_lbl)):
            ch_lbl[i] = ''.join(chr(x) for x in ch_lbl[i]).strip(b'\x00'.decode())
        elec_id = list(nev_file['elec_id'][0])
        electrode_meta = dict()
        electrode_meta['elec_pin'] = list(np.asarray(nev_file['elec_pin'][0]).T)
        electrode_meta['elec_bank'] = list(np.asarray(nev_file['elec_bank']).T)
        for i in range(len(electrode_meta['elec_bank'])):
            electrode_meta['elec_bank'][i] = chr(electrode_meta['elec_bank'][i])
        thresholds = list(np.asarray(nev_file['elec_threshold'][0]).T)
        # ----------- Delete empty electrode channels, they are often used as reference ---------- #
        empty_str = []
        for each in empty_channels:
            empty_str.append(''.join(('elec', str(each))))
        bad_num = []
        for each in empty_str:
            bad_num.append(ch_lbl.index(each))
        for idx in sorted(bad_num, reverse=True):
            del(ch_lbl[idx])
            del(elec_id[idx])
            del(electrode_meta['elec_pin'][idx])
            del(electrode_meta['elec_bank'][idx])
            del(thresholds[idx])
        # ---------- Deal with actual spike data ---------- #
        time_stamp = np.asarray(nev_file['data']['spikes']['TimeStamp'])
        electrode = np.asarray(nev_file['data']['spikes']['Electrode'])
        waveform = np.asarray(nev_file['data']['spikes']['Waveform'])
        s_spikes = []
        s_waveforms = []
        for each in elec_id:
            idx = np.where(electrode == each)[0]
            s_spikes.append(time_stamp[idx])
            s_waveforms.append(waveform[idx,:])

        self.nev_fs = nev_file['fs'][0][0]
        self.nev_duration = nev_file['duration'][0][0]
        self.electrode_meta = electrode_meta
        self.thresholds = thresholds
        self.spikes = s_spikes
        self.waveforms = s_waveforms
        self.ch_lbl = ch_lbl
        e = time.clock()
        print("%.3f s for parsing the nev-mat file" %(e-s))
        
    def parse_rhd_file(self, filename, notch):
        rhd_data = read_data(filename)
        if self.date_num < 20190701:
            self.EMG_fs = 2011.148
        else:
            self.EMG_fs = rhd_data['frequency_parameters']['amplifier_sample_rate']
        EMG_single = rhd_data['amplifier_data']
        if notch == 1:
           for i in range(np.size(EMG_single, 0)): 
               EMG_single[i,:] = notch_filter(EMG_single[i,:], self.EMG_fs, 60, 10)
        else:
            pass
        EMG_names_single = []
        for i in range(len(rhd_data['amplifier_channels'])):
            EMG_names_single.append(rhd_data['amplifier_channels'][i]['custom_channel_name'])
        # ---------- To get paired EMG channels for software diffrence ---------- #
        EMG_names = []
        EMG_index1 = []
        EMG_index2 = []
        for i in range(len(EMG_names_single)):
            temp_str = EMG_names_single[i][:-2]
            if (temp_str in EMG_names) == True:
                continue
            else:
                for j in range(i+1, len(EMG_names_single)):
                    temp_str2 = EMG_names_single[j]
                    if temp_str2.find(temp_str) != -1:
                        if (temp_str2 in EMG_names) == True:
                            EMG_names.append(''.join(temp_str, '_3'))
                        else:
                            EMG_names.append(temp_str)
                        EMG_index1.append(EMG_names_single.index(EMG_names_single[i]))
                        EMG_index2.append(EMG_names_single.index(EMG_names_single[j]))
        EMG_diff = []
        for i in range(len(EMG_index1)):
            EMG_diff.append(EMG_single[EMG_index1[i], :] - EMG_single[EMG_index2[i], :])
        EMG_diff = np.asarray(EMG_diff)
        sync_line0 = rhd_data['board_dig_in_data'][0]
        sync_line1 = rhd_data['board_dig_in_data'][1]
        d0 = np.where(sync_line0 == True)[0]
        d1 = np.where(sync_line1 == True)[0]
        ds = int(d1[0] - int((d1[0]-d0[0])*0.2))
        de = int(d1[-1] + int((d0[-1]-d1[-1])*0.2))
        rhd_timeframe = np.arange(de-ds+1)/self.EMG_fs
        return EMG_names, list(EMG_diff[:, ds:de]), rhd_timeframe
    
    def clean_cortical_data(self, K1 = 8, K2 = 7):
        # ---------- K1 and K2 sets a threshold for high amplitude noise cancelling ----------#
        if hasattr(self, 'thresholds'):
            for i in range(len(self.waveforms)):
                bad_waveform_ind = []
                thr = abs(self.thresholds[i])
                for j in range(np.size(self.waveforms[i], 0)):
                    if max(abs( self.waveforms[i][j,:] )) > K1*thr:
                        bad_waveform_ind.append(j)
                    if abs(self.waveforms[i][j, 0]) > K2*thr:
                        bad_waveform_ind.append(j)
                self.waveforms[i] = np.delete(self.waveforms[i], bad_waveform_ind, axis = 0)
                self.spikes[i] = np.delete(self.spikes[i], bad_waveform_ind)
                self.is_cortical_cleaned = True
        else:
            print('This function may not be applied to this data version.')

    def EMG_filtering(self, f_Hz):
        fs = self.EMG_fs
        raw_EMG_data = self.EMG_diff
        filtered_EMG = []    
        bhigh, ahigh = signal.butter(4,50/(fs/2), 'high')
        blow, alow = signal.butter(4,f_Hz/(fs/2), 'low')
        for each in raw_EMG_data:
            temp = signal.filtfilt(bhigh, ahigh, each)
            f_abs_emg = signal.filtfilt(blow ,alow, np.abs(temp))
            filtered_EMG.append(f_abs_emg)   
        self.filtered_EMG = filtered_EMG
        print('All EMG channels have been filtered.')
        self.is_EMG_filtered = True
            
    def bin_spikes(self, bin_size, mode = 'center'):
        print('Binning spikes with %.4f s' % (bin_size))
        binned_spikes = []
        if mode == 'center':
            bins = np.arange(bin_size - bin_size/2, 
                             self.EMG_timeframe[-1] + bin_size/2, bin_size)
        elif mode == 'left':
            bins = np.arange(self.EMG_timeframe[0], self.EMG_timeframe[-1], bin_size)
        bins = bins.reshape((len(bins),))
        for each in self.spikes:
            each = each/self.nev_fs
            each = each.reshape((len(each),))
            out, _ = np.histogram(each, bins)
            binned_spikes.append(out)
        bins = np.arange(self.EMG_timeframe[0], self.EMG_timeframe[-1], bin_size)
        return bins[1:], binned_spikes        
      
    def EMG_downsample(self, new_fs):
        if hasattr(self, 'filtered_EMG'):
            down_sampled = []
            n = self.EMG_fs/new_fs
            length = int(np.floor(np.size(self.filtered_EMG[0])/n)+1)
            for each in self.filtered_EMG:
                temp = []
                for i in range( 1, length ):
                    temp.append(each[int(np.floor(i*n))])
                temp = np.asarray(temp)
                down_sampled.append(temp)
            print('Filtered EMGs have been downsampled')
            return down_sampled
        else:
            print('Filter EMG first!')
            return 0
        
    def bin_data(self, bin_size, mode = 'center'):
        if not hasattr(self, 'binned'):
            self.binned = {}
        self.binned['timeframe'], self.binned['spikes'] = self.bin_spikes(bin_size, mode)
        self.binned['filtered_EMG'] = self.EMG_downsample(1/bin_size)
        truncated_len = min(len(self.binned['filtered_EMG'][0]), len(self.binned['spikes'][0]))
        for (i, each) in enumerate(self.binned['spikes']):
            self.binned['spikes'][i] = each[:truncated_len]
        for (i, each) in enumerate(self.binned['filtered_EMG']):
            self.binned['filtered_EMG'][i] = each[:truncated_len]
        self.binned['timeframe'] = self.binned['timeframe'][:truncated_len]
        self.is_data_binned = True
        print('Data have been binned.')
    
    def smooth_binned_spikes(self, kernel_type, kernel_SD, sqrt = 0):
        smoothed = []
        if self.binned:
            if sqrt == 1:
               for (i, each) in enumerate(self.binned['spikes']):
                   self.binned['spikes'][i] = np.sqrt(each)
            bin_size = self.binned['timeframe'][1] - self.binned['timeframe'][0]
            kernel_hl = np.ceil( 3 * kernel_SD / bin_size )
            normalDistribution = stats.norm(0, kernel_SD)
            x = np.arange(-kernel_hl*bin_size, (kernel_hl+1)*bin_size, bin_size)
            kernel = normalDistribution.pdf(x)
            if kernel_type == 'gaussian':
                pass
            elif kernel_type == 'half_gaussian':
               for i in range(0, int(kernel_hl)):
                    kernel[i] = 0
            n_sample = np.size(self.binned['spikes'][0])
            nm = np.convolve(kernel, np.ones((n_sample))).T[int(kernel_hl):n_sample + int(kernel_hl)] 
            for each in self.binned['spikes']:
                temp1 = np.convolve(kernel,each)
                temp2 = temp1[int(kernel_hl):n_sample + int(kernel_hl)]/nm
                smoothed.append(temp2)
            print('The binned spikes have been smoothed.')
            self.binned['spikes'] = smoothed
            self.is_spike_smoothed = True
        else:
            print('Bin spikes first!')
            
    def save_to_pickle(self, save_path, file_name):
        if save_path[-1] == '/':
            save_name = ''.join((save_path, file_name, '.pkl'))
        else:
            save_name = ''.join((save_path, '/', file_name, '.pkl'))
        with open (save_name, 'wb') as fp:
            pickle.dump(self, fp)
        print('Save to %s successfully' %(save_name))