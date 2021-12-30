# Audio-separation-models-checker

This code allows to check quality of audio separation models. It compares original stems with extracted stems and found average difference using [SDR metric](https://www.aicrowd.com/challenges/music-demixing-challenge-ismir-2021#evaluation-metric). 

## How to use

1) Download [MUSDB18-HQ dataset](https://zenodo.org/record/3338373#.Yc3cdbqOFaQ)
2) Put `test` folder from archive `musdb18hq.zip` in folder `./input/`
3) Process all files `./input/test/*/mixture.wav` with your audio separation software. Put results in folder `./output/` with the same directory structure as in `./input/test/`.
4) Run code: 

```
python compare.py --input ./input/test/ --output ./output/
```
 
**Note**: you can use custom dataset with same folder structure. Each folder in `test` must contain `mixture.wav`
