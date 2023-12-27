Oliver Lopez, Carlos Moustafa, Dylan Van Bramer, Daniel Cao.

This is our final project for CS 6784, Advanced topics in Machine Learning. We investigate different machine learning approaches to cooling data centers. 

Data centers are increasingly prevalent, and are estimated to account for around 2% of global electricity consumption. Generally, the cooling system is about 40% of the entire center's electricity usage.
Optimizing data center cooling systems is therefore critical step towards sustainable computing. We provide a novel framework to develop cooling systems, while reducing suboptimality during the training/exploration phase. 
Specifically, we utilize the newly introduced Marconi100 supercomputer dataset to pretrain a cooling policy, before finetuning on an unseen datacenter. We verify our results using thermal simulations run with EnergyPlus.

Please see our final report at "paper.pdf"


The EnergyPlus RLlib environment can be found here: https://github.com/airboxlab/rllib-energyplus
The Marconi100 dataset can be found here: https://www.nature.com/articles/s41597-023-02174-3
