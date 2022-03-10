Modified version of DILBERT to support using UMLS codes for normalization instead of just mesh terms
 ## Requirements
```bash
$ pip install -r requirements.txt
```
or 
```bash
$ conda env create -f environment.yml
```
(env name is called dilbert)
## Resources

### Pretrained Model
We use the [Huggingface](https://github.com/huggingface/transformers) version of [BioBERT v1.1](https://github.com/dmis-lab/biobert) so that the pretrained model can be run on the pytorch framework.

- [biobert v1.1 (pytorch)](https://drive.google.com/drive/folders/1nSjj-ubecQbwYPdz3NyAqiJ1-rLtguUp?usp=sharing)

 ### Datasets

We made available all [datasets](https://yadi.sk/d/lQ8bAhFMnjSvTA)

## Steps to run DILBERT with UMLS on Litcoin Data
1. Download biobert from the drive folder above and put it into ./data/pretrained_models/
2. Download the litcoin data and put it into data folder in DILBERT folder in a folder named LITCOIN (./data/LITCOIN)
3. Run the PrepareLitcoin.ipynb in litcoindata preperation
4. If successful, then you should have two folders with sets of concept files
5. To get the UMLS Graph for MSH and OMIM and the corresponding vocab for the litcoin data, please run UMLS mapping on the UAB system with corresponding credentials
6. If you do not have the credentials, email me and ill send them over
7. Things should be prepared to run finally do ./runUMLS
8. First replace /home/ksasse/code/alzhiemers/DILBERT with your corresponding directory (I do not have a fix for the module import errors right now)
9. chmod +x ./runUMLS
10.  ./runUMLS






 Citing & Authors
 ---
Miftahutdinov Z., Kadurin A., Kudrin R., Tutubalina E. Drug and Disease Interpretation Learning with Biomedical Entity Representation Transformer //Advances in  Information Retrieval. – 2021. – pp. 451-466. [paper](https://link.springer.com/chapter/10.1007/978-3-030-72113-8_30), [preprint](https://arxiv.org/pdf/2101.09311.pdf)
```
@InProceedings{10.1007/978-3-030-72113-8_30,
 author="Miftahutdinov, Zulfat and Kadurin, Artur and Kudrin, Roman and Tutubalina, Elena",
 title="Drug and Disease Interpretation Learning with Biomedical Entity Representation Transformer",
 booktitle="Advances in  Information Retrieval",
 year="2021",
 publisher="Springer International Publishing",
 address="Cham",
 pages="451--466",
 isbn="978-3-030-72113-8"
}
```
Miftahutdinov Z., Kadurin A., Kudrin R., Tutubalina E. Medical concept normalization in clinical trials with drug and disease representation learning //Bioinformatics. – 2021. – Т. 37. – №. 21. – pp. 3856-3864. [paper](https://academic.oup.com/bioinformatics/article/37/21/3856/6313159)
```
@article{10.1093/bioinformatics/btab474,
    author = {Miftahutdinov, Zulfat and Kadurin, Artur and Kudrin, Roman and Tutubalina, Elena},
    title = "{Medical concept normalization in clinical trials with drug and disease representation learning}",
    journal = {Bioinformatics},
    volume = {37},
    number = {21},
    pages = {3856-3864},
    year = {2021},
    month = {07},
    issn = {1367-4803},
    doi = {10.1093/bioinformatics/btab474},
    url = {https://doi.org/10.1093/bioinformatics/btab474},
    eprint = {https://academic.oup.com/bioinformatics/article-pdf/37/21/3856/41091512/btab474.pdf},
}
```

Tutubalina E., Kadurin A., Miftahutdinov Z. Fair evaluation in concept normalization: a large-scale comparative analysis for BERT-based models //Proceedings of the 28th International Conference on Computational Linguistics. – 2020. – pp. 6710-6716. [paper](https://www.aclweb.org/anthology/2020.coling-main.588.pdf), [git](https://github.com/insilicomedicine/Fair-Evaluation-BERT)
```
@inproceedings{tutubalina2020fair,
  title={Fair evaluation in concept normalization: a large-scale comparative analysis for BERT-based models},
  author={Tutubalina, Elena and Kadurin, Artur and Miftahutdinov, Zulfat},
  booktitle={Proceedings of the 28th International Conference on Computational Linguistics},
  pages={6710--6716},
  year={2020}
}
```
